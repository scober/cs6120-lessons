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
    "args": "values",
    "values": "instrs",
    "instrs": "instrs_after_side_effect",
}


def parse_trace_line(line, env):
    if not env:
        assert line == "function start"
        env["args"] = []
        env["argtypes"] = []
        env["state"] = "func"
        return [{"op": "speculate"}]
    if not line:
        env["state"] = state_transitions[env["state"]]
    if env["state"] == "args" and line:
        tokens = line.split(" ")
        arg_name = tokens[0]
        arg_type = tokens[1]
        env["args"].append(arg_name)
        env["argtypes"].append(arg_type)
    if env["state"] == "values" and line:
        tokens = line.split(" ")
        arg_name = tokens[0]
        arg_value = tokens[1]
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
                    "labels": [".tracebail"],
                },
            ]
    if env["state"] == "branch_guard":
        assert line in ["true", "false"], line
        env["state"] = env["prev_state"]
        guard = []
        if line == "false":
            guard_var = "traceguard_not_" + env["guard_on"]
            guard.append({"op": "not", "args": env["guard_on"], "dest": guard_var})
            env["guard_on"] = guard_var
        guard.append(
            {"op": "guard", "args": [env["guard_on"]], "labels": [".tracebail"]}
        )
        return guard

    if env["state"].startswith("instrs"):
        if not line.startswith("{"):
            return []
        instr = json.loads(line)
        if instr["op"] in ["call", "ret", "jmp"]:
            return []
        if instr["op"] == "print":
            env["state"] = "instrs_after_side_effect"
        if instr["op"] == "br":
            env["prev_state"] = env["state"]
            env["state"] = "branch_guard"
            env["guard_on"] = instr["args"][0]
            if env["state"] == "instrs_after_side_effect":
                raise ValueError("can't generate a trace, guard after a side-effect")
            return []

        return [instr]

    return []


def trace_to_block(trace):
    env = {}
    block = []
    for line in trace:
        block.extend(parse_trace_line(line.rstrip("\n"), env))

    return block


@click.group
def main():
    pass


@main.command(name="trace2block")
def trace_to_block_command():
    """
    Convert input program out of SSA form (input is assumed to be in SSA form)
    """
    pprint.pprint(trace_to_block(sys.stdin))


if __name__ == "__main__":
    main()
