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


def canonicalize(value):
    if len(value) > 1 and value[1] in ["mul", "add", "eq", "and", "or"]:
        assert len(value) == 4
        value = value[:2] + sorted(value[2:])

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
    return tuple(canonicalize(value))


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


def fold_constants_into_instruction(instr, environment, value_table):
    op = instr["op"]
    if op == "ret":
        # you can't return a constant value
        return
    instr["op"] = "const"

    left = value_table[environment[instr["args"][0]]][-1] if "args" in instr else None
    right = (
        value_table[environment[instr["args"][1]]][-1]
        if ("args" in instr and len(instr["args"]) > 1)
        else None
    )

    # in a real compiler you might want your compiler to tell you were trying to
    #   divide by zero
    # here, to simplify testing, we will leave divides by zero in place
    if op == "div" and right == 0:
        instr["op"] = op
        return

    instr.pop("args", None)

    # we should make sure these computations match the semantics of bril,
    #   but let's just be sloppy for now
    if op == "const":
        pass
    elif op == "add":
        instr["value"] = left + right
    elif op == "sub":
        instr["value"] = left - right
    elif op == "mul":
        instr["value"] = left * right
    elif op == "div":
        instr["value"] = left / right
    elif op == "jmp":
        instr["op"] = "jmp"
    elif op == "br":
        instr["op"] = "jmp"
        instr["labels"] = [instr["labels"][0]] if left else [instr["labels"][1]]
    elif op == "eq":
        instr["value"] = left == right
    elif op == "lt":
        instr["value"] = left < right
    elif op == "gt":
        instr["value"] = left > right
    elif op == "le":
        instr["value"] = left <= right
    elif op == "ge":
        instr["value"] = left >= right
    elif op == "and":
        instr["value"] = left and right
    elif op == "or":
        instr["value"] = left or right
    elif op == "not":
        instr["value"] = not left
    else:
        print(f"unsupported operation {op}")


def fold_comparisons(instr):
    instr.pop("args", None)
    instr["value"] = instr["op"] in ["eq", "le", "ge"]
    instr["op"] = "const"


def local_value_number_instruction(
    instr, dest, row_num, value_home, value_table, environment
):
    oi = copy.deepcopy(instr)
    if ut.has_side_effects(instr):
        return oi

    if (
        len(instr.get("args", [])) == 2
        and instr["args"][0] == instr["args"][1]
        and instr.get("op", "") in ["eq", "le", "ge", "lt", "gt"]
    ):
        fold_comparisons(oi)
    elif all("const" in value_table[environment[arg]] for arg in instr.get("args", [])):
        fold_constants_into_instruction(oi, environment, value_table)
    # if one of the folding optimizations ran, put the new const op in the table
    if not row_num is None and oi["op"] == "const":
        value_table[row_num] = construct_value(oi, {}, value_table, {})

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
        row_num = None
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
                local_value_number_instruction(
                    instr, dest, row_num, value_home, value_table, environment
                )
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
