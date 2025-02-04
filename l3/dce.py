import json
import sys

import click

import utilities as ut


@ut.global_optimization
def global_simple_dead_code_elimination(func):
    used = set()
    for instr in func["instrs"]:
        if "args" in instr:
            used.update(instr["args"])
    out = []
    for instr in func["instrs"]:
        if "dest" not in instr or instr["dest"] in used:
            out.append(instr)
    return {"name": func["name"], "instrs": out}


@click.group
def main():
    pass


@main.command(name="global")
def global_dce():
    print(json.dumps(global_simple_dead_code_elimination(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
