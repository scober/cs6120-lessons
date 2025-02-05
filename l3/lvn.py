import copy
import json
import sys

import click

import utilities as ut


def all_vars_in_block(block):
    all_vars = set()
    for instr in block:
        all_vars.add(instr.get("dest", None))
        all_vars |= set(instr.get("args", []))
    return all_vars


def canonicalize(value, table):
    return value


def construct_value(instr, environment, value_table, live_ins):
    if instr["op"] == "id" and not any(
        arg in live_ins
        for arg in instr.get("args", [])
        + instr.get("values", [])
        + ([instr["value"]] if "value" in instr else [])
    ):
        return value_table[environment[instr["args"][0]]]
    value = (
        ([instr["type"]] if "type" in instr else [])
        + [instr["op"]]
        + [environment[arg] for arg in instr.get("args", [])]
        + ([instr["value"]] if "value" in instr else [])
    )
    return tuple(canonicalize(value, value_table))


def copy_value(instr, value, var_home):
    if len(value) > 2 and value[1] == "const":
        return {
            "op": "const",
            "dest": instr["dest"],
            "type": instr["type"],
            "value": value[-1],
        }
    else:
        return {
            "op": "id",
            "dest": instr["dest"],
            "type": instr["type"],
            "args": [var_home],
        }


def freshen_var(var_name, rest_of_block, all_vars):
    fresh_var = var_name

    if any(
        future_instr.get("dest", None) == var_name for future_instr in rest_of_block
    ):
        appendage = 0
        while fresh_var in all_vars:
            fresh_var = var_name + f"_{appendage}"
            appendage += 1
        all_vars.add(fresh_var)

    return fresh_var


def local_value_number_instruction(instr, dest, value_home, environment):
    oi = copy.deepcopy(instr)
    if ut.has_side_effects(instr):
        return oi
    if "dest" in oi:
        oi["dest"] = dest
    if "args" in oi:
        oi["args"] = [value_home[environment[arg]] for arg in oi["args"]]
    return oi


@ut.local_optimization
def local_value_numbering(block):
    out = []

    value_table = []
    value_home = []
    environment = {}
    live_ins = set()

    all_vars = all_vars_in_block(block)

    for pos, instr in enumerate(block):
        if "label" in instr:
            out.append(copy.deepcopy(instr))
            continue
        for arg in instr.get("args", []):
            if arg not in environment:
                live_ins.add(arg)
                environment[arg] = len(value_table)
                value_table.append(arg)
                value_home.append(arg)

        value = construct_value(instr, environment, value_table, live_ins)

        dest = None
        if value in value_table:
            row_num = value_table.index(value)
            out.append(copy_value(instr, value_table[row_num], value_home[row_num]))
            dest = instr["dest"]
        else:
            if "dest" in instr and not ut.has_side_effects(instr):
                dest = instr["dest"]

                dest = freshen_var(dest, block[pos + 1 :], all_vars)

                row_num = len(value_table)
                value_table.append(value)
                value_home.append(dest)

            out.append(
                local_value_number_instruction(instr, dest, value_home, environment)
            )

        if not ut.has_side_effects(instr):
            if dest:
                environment[dest] = row_num
            if "dest" in instr:
                environment[instr["dest"]] = row_num

    return out


@click.group
def main():
    pass


@main.command
def lvn():
    print(json.dumps(local_value_numbering(json.load(sys.stdin))))


if __name__ == "__main__":
    main()
