import json
import pprint
import subprocess

import click
from colored import Fore, Back, Style

import utilities as ut


def args_are_for_bril(args):
    # in case we want to switch back to a block list
    # bad_args = ["tdce", "dkp"]
    bril_args = ["true", "false"]
    return all(
        arg.lstrip("-").isnumeric() or arg in bril_args for arg in args.split(" ")
    )


def run_bril(filename, optimizer):
    assert filename.endswith(".bril"), f"{filename} does not end with .bril"

    args = ""
    with open(filename, "r") as f:
        for line in f:
            if "ARGS" in line:
                args = line.split(":")[-1].strip()
                if not args_are_for_bril(args):
                    args = ""

    pipeline = f"bril2json < {filename} | {optimizer} | brili -p {args}"
    output = subprocess.getoutput(pipeline).splitlines()
    dynamic_instructions = (
        output[-1].split(" ")[-1] if output[-1].startswith("total_dyn_inst:") else -1
    )

    return output[:-1], dynamic_instructions


def count_static_instructions(filename, optimizer):
    count = 0
    prog = json.loads(subprocess.getoutput(f"bril2json < {filename} | {optimizer}"))
    for func in prog["functions"]:
        for instr in func["instrs"]:
            if "label" not in instr:
                count += 1

    return count


def check_output(bril, optimizer):
    unoptimized_output, _ = run_bril(bril, "cat")
    optimized_output, _ = run_bril(bril, optimizer)

    assert (
        unoptimized_output == optimized_output
    ), f"optimization {optimizer} broke file {bril}, turned {unoptimized_output} into {optimized_output}"


def check_static_instructions(bril, optimizer):
    unoptimized_static = count_static_instructions(bril, "cat")
    optimized_static = count_static_instructions(bril, optimizer)

    assert (
        unoptimized_static >= optimized_static
    ), f"optimization {optimizer} increased the number of static instructions in {bril}, from {unoptimized_static} to {optimized_static}"


def check_dynamic_instructions(bril, optimizer):
    _, unoptimized_dynamic = run_bril(bril, "cat")
    _, optimized_dynamic = run_bril(bril, optimizer)

    assert (
        unoptimized_dynamic >= optimized_dynamic
    ), f"optimization {optimizer} increased the number of dynamic instructions in {bril}, from {unoptimized_dynamic} to {optimized_dynamic}"


def progress():
    print(f"{Fore.green}.{Style.reset}", end="", flush=True)


@click.group
def main():
    pass


@main.command
@click.argument("optimizer", nargs=1)
@click.argument("brils", nargs=-1)
def static(optimizer, brils):
    """
    Ensure that the optimization has not increased the number of static static instructions
    """
    for bril in brils:
        check_output(bril, optimizer)
        check_static_instructions(bril, optimizer)
        progress()
    print()


@main.command
@click.argument("optimizer", nargs=1)
@click.argument("brils", nargs=-1)
def dynamic(optimizer, brils):
    """
    Ensure that the optimization has not increased the number of dynamic instructions
    """
    for bril in brils:
        check_output(bril, optimizer)
        check_dynamic_instructions(bril, optimizer)
        progress()
    print()


@main.command
@click.argument("optimizer", nargs=1)
@click.argument("brils", nargs=-1)
def none(optimizer, brils):
    """
    Ensure that the optimization has not increased the number of dynamic instructions
    """
    for bril in brils:
        check_output(bril, optimizer)
        progress()
    print()


if __name__ == "__main__":
    main()
