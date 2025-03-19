import utilities as ut

import collections
import copy
import functools
import json
import pprint
import sys

import click


@ut.global_optimization
def loop_invariant_code_motion(instrs):
    return instrs


@click.group
def main():
    pass


@main.command(name="nl")
def natural_loops_command():
    """
    Discover and print out all natural loops in a program
    """
    pprint.pprint(ut.natural_loops((json.load(sys.stdin))))


@main.command(name="licm")
def out_of_ssa_command():
    """
    Perform loop-invariant code motion on input program
    """
    print(json.dumps(loop_invariant_code_motion(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
