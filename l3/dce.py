import json
import sys

import click

import utilities as ut


@ut.global_optimization
def global_simple_dead_code_elimination(instrs):
    used = set()
    for instr in instrs:
        if "args" in instr:
            used.update(instr["args"])
    out = []
    for instr in instrs:
        if "dest" not in instr or instr["dest"] in used:
            out.append(instr)
    return out


@click.group
def main():
    pass


@main.command(name="global")
def global_dce():
    print(json.dumps(global_simple_dead_code_elimination(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
