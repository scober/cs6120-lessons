import utilities as ut

import collections
import copy
import functools
import json
import pprint
import sys

import click


def reaching_definitions(prog):
    def transfer(reaching_in, block, label):
        reaching_out = reaching_in
        for instr in block:
            if "dest" in instr:
                reaching_out[instr["dest"]] = [label]
        return reaching_out

    def merge(dicts):
        out = {}
        for d in dicts:
            for k, v in d.items():
                if k not in out:
                    out[k] = []
                for thing in v:
                    if thing not in out[k]:
                        out[k].append(thing)
        return out

    # this is only correct for a single function, I really should have designed
    #   this framework to work on single functions, not whole programs
    return ut.forward_data_flow_analysis(
        prog,
        lambda: {arg["name"]: "arg" for arg in prog["functions"][0]["args"]},
        dict,
        merge,
        transfer,
    )


def identify_lii(loop, labels_to_blocks, reaching_defs):
    # because we aren't working in ssa, we need to identify instructions by
    #   block label, index pairs
    invariant_instrs = set()
    old_ii = set("dummy")
    while old_ii != invariant_instrs:
        old_ii = copy.deepcopy(invariant_instrs)
        for label in loop:
            reaching = reaching_defs[label]["out"]
            for index, instr in enumerate(labels_to_blocks[label]):
                if all(
                    not any(lb in reaching[arg] for lb in loop)
                    for arg in instr.get("args", [])
                ):
                    invariant_instrs.add((label, index))

    return invariant_instrs


def safe_to_move(loop, labels_to_blocks, succs, doms, instrs):
    def get_instr(instr_tuple):
        return labels_to_blocks[instr_tuple[0]][instr_tuple[1]]

    def has_no_side_effects(instr):
        return get_instr(instr).get("op", "") not in [
            "print",
            "store",
            "load",
            "call",
            "div",
        ]

    def does_not_modify_control_flow(instr):
        return "label" not in get_instr(instr) and "labels" not in get_instr(instr)

    def def_dominates_uses(instr):
        assert "dest" in get_instr(instr), f"instr: {get_instr(instr)}"
        dest = get_instr(instr)["dest"]
        # this should check that this definition dominates all uses in the loop,
        #   but not necessarily that it dominates all uses ever
        for block in loop:
            if block == instr[0]:
                if any(
                    dest in bi.get("args", []) and index < instr[1]
                    for index, bi in enumerate(labels_to_blocks[block])
                ):
                    return False
            elif instr[0] not in doms[block] and any(
                dest in bi.get("args", []) for bi in labels_to_blocks[block]
            ):
                return False
        return True

    def no_other_defs_in_loop(instr):
        assert "dest" in get_instr(instr), f"instr: {get_instr(instr)}"
        dest = get_instr(instr)["dest"]
        return all(
            all(
                (block, index) == instr or i.get("dest", "") != dest
                for index, i in enumerate(labels_to_blocks[block])
            )
            for block in loop
        )

    def dominates_loop_exits(instr):
        # all loop block are either
        #   1. not loop exits
        #   or
        #   2. dominated by this instruction
        return all(
            all(succ in loop for succ in succs[label]) or instr[0] in doms[label]
            for label in loop
        )

    return set(
        filter(
            dominates_loop_exits,
            filter(
                no_other_defs_in_loop,
                filter(
                    def_dominates_uses,
                    filter(
                        does_not_modify_control_flow,
                        filter(has_no_side_effects, instrs),
                    ),
                ),
            ),
        )
    )


# @ut.iterate_to_convergence
@ut.global_optimization
def loop_invariant_code_motion(instrs, args):
    prog = {"functions": [{"instrs": instrs, "name": "dummy", "args": args}]}
    blocks, succs, preds, labels_to_blocks, entry_blocks = ut.the_stuff(prog)
    loops = ut.natural_loops(prog)
    reaching_defs = reaching_definitions(prog)
    doms = ut.dominators(prog)
    for loop in loops:
        invariant_instrs = identify_lii(loop, labels_to_blocks, reaching_defs)
        moveable_instrs = safe_to_move(
            loop, labels_to_blocks, succs, doms, invariant_instrs
        )
        preheaders = [pred for pred in preds[loop[0]] if pred not in loop]
        for instr_tuple in reversed(sorted(moveable_instrs, key=lambda tup: tup[1])):
            label, index = instr_tuple
            instr = labels_to_blocks[label][index]
            labels_to_blocks[label].pop(index)
            if len(preheaders):
                for preheader in preheaders:
                    ut.append_to_block(instr, labels_to_blocks[preheader])
            else:
                blocks["dummy"].insert(0, ("simon_magic_entry", []))
                ut.append_to_block(instr, blocks["dummy"][0][1])

    return functools.reduce(lambda acc, tup: acc + tup[1], blocks["dummy"], [])


@click.group
def main():
    pass


@main.command(name="nl")
def natural_loops_command():
    """
    Discover and print out all natural loops in a program
    """
    pprint.pprint(ut.natural_loops(json.load(sys.stdin)))


@main.command(name="licm")
def out_of_ssa_command():
    """
    Perform loop-invariant code motion on input program
    """
    print(json.dumps(loop_invariant_code_motion(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
