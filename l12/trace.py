import utilities as ut

import collections
import copy
import functools
import json
import pprint
import sys

import click

state_transitions = {
    "begin": "func",
    "func": "name",
    "name": "args",
    "args": "instrs",
    "instrs": "instrs",
    "instrs_after_side_effect": "instrs_after_side_effect",
}


def rewrite_variable(var, call_stack):
    return "_".join(call_stack) + "_" + var


def rewrite_instr(instr, call_stack):
    if "dest" in instr:
        instr["dest"] = rewrite_variable(instr["dest"], call_stack)
    if "args" in instr:
        instr["args"] = list(
            map(lambda var: rewrite_variable(var, call_stack), instr["args"])
        )

    return instr


# TODO: return value stack
def parse_trace_line(line, env):
    if not env:
        assert line == "function start", line
        env["args"] = []
        env["argtypes"] = []
        env["state"] = "func"
        env["funcs"] = []
        env["return_vars"] = []
        env["prev_state"] = "instrs"
        return [{"op": "speculate"}]
    if not line:
        env["state"] = state_transitions[env["state"]]
        return []
    if line == "function start":
        env["state"] = "func"
    if env["state"] == "name":
        env["funcs"].append(line)
    if env["state"] == "args":
        tokens = line.split(" ")
        arg_name = tokens[0]
        arg_type = tokens[1]
        arg_value = tokens[2]
        if arg_type == "int":
            arg_value = int(arg_value)
        elif arg_type == "bool":
            arg_value = bool(arg_value)
        elif arg_type == "float":
            arg_value = float(arg_value)
        env["args"].append(arg_name)
        env["argtypes"].append(arg_type)
        if env["funcs"] != ["main"]:
            return [
                {
                    "op": "const",
                    "dest": rewrite_variable(arg_name, env["funcs"]),
                    "type": arg_type,
                    "value": arg_value,
                }
            ]
        if env["funcs"] == ["main"]:
            if arg_name in env["args"]:
                ind = env["args"].index(arg_name)
                arg_type = env["argtypes"][ind]
                return [
                    {
                        "dest": arg_name + "_tracevalue",
                        "op": "const",
                        "type": arg_type,
                        "value": arg_value,
                    },
                    {
                        "dest": arg_name + "_traceguard",
                        "op": "eq",
                        "type": "bool",
                        "args": [arg_name, arg_name + "_tracevalue"],
                    },
                    {
                        "op": "guard",
                        "args": [arg_name + "_traceguard"],
                        "labels": ["tracebail"],
                    },
                    {
                        "op": "id",
                        "args": [arg_name],
                        "type": arg_type,
                        "dest": rewrite_variable(arg_name, env["funcs"]),
                    },
                ]
    if env["state"] == "branch_guard":
        assert line in ["true", "false"], line
        env["state"] = env["prev_state"]
        guard = []
        if line == "false":
            guard_var = "traceguard_not_" + env["guard_on"]
            guard.append({"op": "not", "args": [env["guard_on"]], "dest": guard_var})
            env["guard_on"] = guard_var
        guard.append(
            {"op": "guard", "args": [env["guard_on"]], "labels": ["tracebail"]}
        )
        return guard

    if env["state"].startswith("instrs"):
        if not line.startswith("{"):
            return []
        instr = json.loads(line)
        if instr["op"] == "call":
            env["return_vars"].append(instr["dest"])
        if instr["op"] == "ret":
            return_var = env["return_vars"].pop()
            # get arg variable name before popping the call stack
            arg = rewrite_variable(instr["args"][0], env["funcs"])
            env["funcs"].pop()
            # get dest variable name after popping the call stack
            dest = rewrite_variable(return_var, env["funcs"])
            return [
                {
                    "op": "id",
                    "dest": dest,
                    "args": [arg],
                }
            ]
        if instr["op"] in ["call", "ret", "jmp"]:
            return []
        if instr["op"] == "print":
            env["state"] = "instrs_after_side_effect"
        if instr["op"] == "br":
            env["prev_state"] = env["state"]
            env["state"] = "branch_guard"
            env["guard_on"] = rewrite_variable(instr["args"][0], env["funcs"])
            if env["state"] == "instrs_after_side_effect":
                raise ValueError("can't generate a trace, guard after a side-effect")
            return []

        return [rewrite_instr(instr, env["funcs"])]

    return []


def trace_to_block(trace):
    env = {}
    block = []
    for line in trace:
        block.extend(parse_trace_line(line.rstrip("\n"), env))

    block.append({"op": "commit"})
    block.append({"op": "ret"})
    return block


def inject_trace(prog, trace):
    trace_block = trace_to_block(trace)
    for func in prog["functions"]:
        if func["name"] != "main":
            continue
        func["instrs"].insert(0, {"label": "tracebail"})
        func["instrs"] = trace_block + func["instrs"]
    return prog


@click.group
def main():
    pass


@main.command(name="trace2block")
def trace_to_block_command():
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    pprint.pprint(trace_to_block(sys.stdin))


@main.command(name="traceinject")
@click.argument("tracefile")
def trace_inject_command(tracefile):
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    prog = json.load(sys.stdin)
    trace = open(tracefile, "r").readlines()
    print(json.dumps(inject_trace(prog, trace)))


if __name__ == "__main__":
    main()
