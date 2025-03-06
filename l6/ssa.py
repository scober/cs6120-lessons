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
            instr["args"] = [
                f"{arg}{'.' + str(var_stack[arg]) if var_stack[arg] else ''}"
                for arg in instr["args"]
            ]
        if "dest" in instr:
            dest = instr["dest"]
            var_stack[dest] += 1
            instr["dest"] = f"{dest}.{var_stack[dest]}"
        for sl in succs[label]:
            succ = labels_to_blocks[sl]
            for phi in phis(succ):
                # TODO
                pass


@ut.global_optimization
def to_ssa_form(instrs):
    prog = {"functions": [{"instrs": instrs, "name": "dummy"}]}
    blocks, succs, preds, labels_to_blocks, entry_blocks = ut.the_stuff(prog)
    frontiers = ut.dominator_frontiers(ut.dominators(prog), preds)
    all_vars = ut.all_vars_in_prog(prog)

    phiify(labels_to_blocks, succs, all_vars, frontiers)

    assert len(entry_blocks) == 1, str(entry_blocks)
    rename_vars({var: 0 for var in all_vars}, labels_to_blocks, succs, entry_blocks[0])

    # I wish Python just had a function called fold
    return functools.reduce(lambda acc, tup: acc + tup[1], blocks["dummy"], [])


@ut.local_optimization
def variable_renaming(instrs):
    out = []
    most_recent_name = {}
    for instr in instrs:
        new_instr = copy.deepcopy(instr)
        if "args" in new_instr:
            new_instr["args"] = [
                (
                    arg + "." + str(most_recent_name[arg])
                    if arg in most_recent_name
                    else arg
                )
                for arg in new_instr["args"]
            ]
        if "dest" in new_instr:
            dest = new_instr["dest"]
            if dest not in most_recent_name:
                most_recent_name[dest] = 0
            most_recent_name[dest] += 1
            new_instr["dest"] = dest + "." + str(most_recent_name[dest])

        out.append(new_instr)

    return out


@ut.global_optimization
def phi_nodes(instrs):
    return instrs


@ut.global_optimization
def phi_to_id(instrs):
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
