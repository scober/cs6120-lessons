import json
import sys

import click

import utilities as ut


@ut.global_optimization
@ut.iterate_to_convergence
def global_simple_dead_code_elimination(instrs, function_args):
    used = set()
    for instr in instrs:
        if "args" in instr:
            used.update(instr["args"])
    out = []
    for instr in instrs:
        if "dest" not in instr or instr["dest"] in used or ut.has_side_effects(instr):
            out.append(instr)
    return out


@ut.local_optimization
@ut.iterate_to_convergence
def local_simple_dead_code_elimination(block):
    out = []
    assigned_before_next_use = set()
    for instr in reversed(block):
        if (
            "dest" in instr
            and instr["dest"] in assigned_before_next_use
            and not ut.has_side_effects(instr)
        ):
            continue
        out.insert(0, instr)
        if "dest" in instr:
            assigned_before_next_use.add(instr["dest"])
        if "args" in instr:
            for arg in instr["args"]:
                assigned_before_next_use.discard(arg)
    return out


@click.group
def main():
    pass


@main.command(name="global")
def global_dce():
    print(json.dumps(global_simple_dead_code_elimination(json.load(sys.stdin))))


@main.command(name="local")
def local_dce():
    print(json.dumps(local_simple_dead_code_elimination(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
