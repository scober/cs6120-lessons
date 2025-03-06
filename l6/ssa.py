import utilities as ut

import collections
import copy
import functools
import json
import pprint
import sys

import click


def is_defined(var, block):
    return any(instr.get("dest", "") == var for instr in block)


def phis(block):
    for instr in block:
        if instr.get("op", "") == "get":
            yield instr


def upsilons(block):
    for instr in block:
        if instr.get("op", "") == "set":
            yield instr


def already_phied(var, block):
    return any(phi["dest"] == var for phi in phis(block))


def grab_type(var, block):
    for instr in block:
        if instr.get("dest", "") == var:
            return instr["type"]


def add_undefs(all_vars_with_types, entry):
    for var, tipe in all_vars_with_types:
        ut.prepend_to_block({"op": "undef", "type": tipe, "dest": var}, entry)


def phiify(labels_to_blocks, succs, preds, all_vars, frontiers):
    for var in all_vars:
        definitions = [
            l_and_b
            for l_and_b in labels_to_blocks.items()
            if is_defined(var, l_and_b[1])
        ]
        i = 0
        while i < len(definitions):
            label, block = definitions[i]
            tipe = grab_type(var, block)
            for l in frontiers[label]:
                dominated = labels_to_blocks[l]
                if not already_phied(var, dominated):
                    dominated.insert(1, {"op": "get", "type": tipe, "dest": var})
                    for pred in preds[l]:
                        ut.append_to_block(
                            {"op": "set", "args": [var, var]}, labels_to_blocks[pred]
                        )
                    if (l, dominated) not in definitions:
                        definitions.append((l, dominated))
            i += 1


def rename_vars(var_stack, var_ids, labels_to_blocks, succs, preds, dom_tree, label):
    old_var_stack = copy.deepcopy(var_stack)
    block = labels_to_blocks[label]

    for instr in block:
        if "args" in instr:
            if instr.get("op", "") == "set":
                arg = instr["args"][1]
                instr["args"] = instr["args"][:1] + [var_stack[arg]]
            else:
                instr["args"] = [var_stack[arg] for arg in instr["args"]]
        if "dest" in instr:
            dest = instr["dest"]
            var_ids[dest] += 1
            var_stack[dest] = f"{dest}.{var_ids[dest]}"
            instr["dest"] = var_stack[dest]
            # update predecessors' upsilon nodes
            # if two of a block's successors both want me to set the same value,
            #   I will have two identical set instructions but I only want to
            #   update the shadow destination of one per successor
            if instr.get("op", "") == "get":
                for pred in preds[label]:
                    patched_upsilons = set()
                    for pi in upsilons(labels_to_blocks[pred]):
                        if pi["args"][0] == dest and dest not in patched_upsilons:
                            patched_upsilons.add(dest)
                            pi["args"] = [var_stack[dest]] + pi["args"][1:]

    for dominated in dom_tree[label]:
        rename_vars(
            var_stack, var_ids, labels_to_blocks, succs, preds, dom_tree, dominated
        )
    # I am never sure what Python's pass-by-reference semantics are...
    #
    # ...this seems safe though
    for var in var_stack:
        var_stack[var] = old_var_stack[var]


def prune_cfg(instrs):
    prog = {"functions": [{"instrs": instrs, "name": "dummy"}]}
    blocks, succs, preds, labels_to_blocks, entry_blocks = ut.the_stuff(prog)

    old_num_blocks = 0
    while len(blocks["dummy"]) != old_num_blocks:
        old_num_blocks = len(blocks["dummy"])
        blocks["dummy"] = [
            (l, b) for l, b in blocks["dummy"] if preds[l] or l in entry_blocks
        ]

    return functools.reduce(lambda acc, tup: acc + tup[1], blocks["dummy"], [])


@ut.global_optimization
def to_ssa_form(instrs, function_args):
    instrs = prune_cfg(instrs)

    prog = {"functions": [{"instrs": instrs, "name": "dummy"}]}
    if function_args:
        prog["functions"][0]["args"] = function_args

    # if the first block can be jumped to, it has explicit entry points from
    #   those jumps and an implicit entry point from the start of the function
    #   -- let's just make that entry point explicit
    if "label" in instrs[0]:
        labels = set(instr.get("label", "") for instr in instrs)
        label_id = 0
        while f"b.{label_id}" in labels:
            label_id += 1
        prog["functions"][0]["instrs"].insert(0, {"label": f"dummy.{label_id}"})

    blocks, succs, preds, labels_to_blocks, entry_blocks = ut.the_stuff(prog)

    assert len(entry_blocks) == 1, str(entry_blocks)
    entry_block = entry_blocks[0]

    doms = ut.dominators(prog)
    frontiers = ut.dominator_frontiers(doms, preds)
    dom_tree = ut.dominator_tree(doms)

    all_vars = ut.all_vars_in_prog(prog)

    add_undefs(
        ut.all_vars_in_prog_with_types(prog)[1].items(),
        labels_to_blocks[entry_block],
    )

    phiify(labels_to_blocks, succs, preds, all_vars, frontiers)

    rename_vars(
        {var: var for var in all_vars},
        {var: 0 for var in all_vars},
        labels_to_blocks,
        succs,
        preds,
        dom_tree,
        entry_block,
    )

    # I wish Python just had a function called fold
    return functools.reduce(lambda acc, tup: acc + tup[1], blocks["dummy"], [])


@ut.global_optimization
def phi_to_id(instrs, function_args):
    return instrs


@click.group
def main():
    pass


@main.command(name="in")
def into_ssa_command():
    """
    Convert input program into SSA form (input is assumed to be in non-SSA form)
    """
    print(json.dumps(to_ssa_form(json.load(sys.stdin))))


@main.command(name="out")
def out_of_ssa_command():
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    print(json.dumps(phi_to_id(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
