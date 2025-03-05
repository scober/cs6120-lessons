import utilities as ut

import copy
import json
import pprint
import collections
import sys

import click


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
    print(json.dumps(variable_renaming(phi_nodes(json.load(sys.stdin)))))


@main.command(name="out")
def out_of_ssa_command():
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    print(json.dumps(phi_to_id(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
