import utilities as ut

import copy
import json
import pprint
import collections
import sys

import click


@ut.local_optimization
def variable_renaming(block):
    return block


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
def into_ssa_command(validate):
    """
    Convert input program into SSA form (input is assumed to be in non-SSA form)
    """
    print(json.dumps(variable_renaming(phi_nodes(json.load(sys.stdin)))))


@main.command(name="out")
def out_of_ssa_command(validate):
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    print(json.dumps(phi_to_id(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
