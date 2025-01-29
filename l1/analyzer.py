import click

import json
import sys


def parse_into_blocks(prog):
    all_blocks = {}
    label_number = -1
    for f in prog["functions"]:
        blocks = []
        label_number += 1
        label = f"b{label_number}"
        cur = []
        for i in f["instrs"]:
            if "label" in i:
                if len(cur) != 0:
                    blocks.append((label, cur))
                cur = [i]
                label = i["label"]
            elif i["op"] in ("jmp", "br", "ret"):
                cur.append(i)
                blocks.append((label, cur))
                cur = []
                label_number += 1
                label = f"b{label_number}"
            else:
                cur.append(i)
        if len(cur) != 0:
            blocks.append((label, cur))
        all_blocks[f["name"]] = blocks
    return all_blocks


def format_instruction(instruction):
    formatted = "  "

    tp = ""
    if "type" in instruction:
        if "ptr" in instruction["type"]:
            tp = f"ptr<{instruction['type']['ptr']}>"
        else:
            tp = instruction["type"]

    args_and_labels = " ".join(
        instruction.get("args", []) + instruction.get("labels", [])
    )
    value = instruction.get("value", "")
    op = instruction.get("op", "")
    dest = instruction.get("dest", "")

    if "label" in instruction:
        return f"{instruction['label']}:"
    elif op in ("br", "jmp", "load", "store", "free", "print", "ret"):
        formatted += f"{op}{' ' if args_and_labels else ''}{args_and_labels}"
    elif op == "call":
        if "dest" in instruction:
            formatted += f"{dest}: {tp} = "
        # TODO: funcs is a list, is it allowed to have multiple elements?
        formatted += f"@call {instruction['funcs'][0]} {args_and_labels}"
    else:
        formatted += f"{dest}: {tp} = {op} {args_and_labels}{value}"
    return formatted + ";"


def print_blocks(labels_and_blocks):
    for func, l_and_b in labels_and_blocks.items():
        print(f"@{func}")
        for label, block in l_and_b:
            print(f"  --{label}--")
            for i in block:
                if "label" not in i:
                    print(f"  {format_instruction(i)}")


# TODO: should I create a unique exit block if one does not exist?
def construct_cfg(labels_and_blocks):
    cfg = {}
    for func, l_and_b in labels_and_blocks.items():
        for i, (label, block) in enumerate(l_and_b):
            cfg[label] = []
            term = block[-1]
            if "op" in term and term["op"] in ("jmp", "br"):
                for dest in term["labels"]:
                    cfg[label].append(dest)
            elif i < len(l_and_b) - 1:
                cfg[label].append(l_and_b[i + 1][0])
    return cfg


# TODO: we could produce a graphviz data structure in Python and skip the text
def print_cfg_in_dot(cfg, labels_and_blocks):
    cluster_number = 0

    print("digraph cfg {")

    for func, l_and_b in labels_and_blocks.items():
        print(f"  subgraph cluster{cluster_number} {{")
        print("    style = filled;")
        print("    color = lightgrey;")
        print("    node [style=filled,color=white];")
        print(f'    label = "@{func}";')
        for label, block in l_and_b:
            print(f'    "{label}";')
        print("  }")
        print()
        cluster_number += 1

    for label, dests in cfg.items():
        for dest in dests:
            print(f'  "{label}" -> "{dest}";')

    print("}")


def print_cfg(cfg):
    for label in cfg.keys():
        print(f"{label}")

    print()

    for label, dests in cfg.items():
        for dest in dests:
            print(f"{label} -> {dest}")


def print_toplevel_counts(prog):
    print(f"Number of functions: {len(prog['functions'])}")
    label_count = 0
    call_count = 0
    for func in prog["functions"]:
        for instr in func["instrs"]:
            if "label" in instr:
                label_count += 1
            elif instr["op"] == "call":
                call_count += 1
    print(f"Number of labels: {label_count}")
    print(f"Number of function call sites: {call_count}")


def print_opcode_breakdown(prog):
    opcodes = {}
    for func in prog["functions"]:
        for instr in func["instrs"]:
            if "op" in instr:
                if instr["op"] not in opcodes:
                    opcodes[instr["op"]] = 0
                opcodes[instr["op"]] += 1
    total = sum(opcodes.values())

    indent = 1 + max(map(len, opcodes.keys()))
    print("Breakdown of instructions by opcode:")
    for opcode, count in opcodes.items():
        print(f"  {opcode}:{' '*(indent-len(opcode))}{round(count/total*100)}%")


@click.group
def main():
    pass


@main.command
def blocks():
    """
    Split a bril program into labelled basic blocks
    """
    print_blocks(parse_into_blocks(json.load(sys.stdin)))


@main.command
@click.option("--dot", is_flag=True, help="print out cfg in graphviz dot language")
def cfg(dot):
    """
    Construct control flow graph of a bril program, labelled by labels from block command
    """
    labels_and_blocks = parse_into_blocks(json.load(sys.stdin))
    cfg = construct_cfg(labels_and_blocks)
    if dot:
        print_cfg_in_dot(cfg, labels_and_blocks)
    else:
        print_cfg(cfg)


@main.command
@click.option("--dot", is_flag=True, help="print out cfg in graphviz dot language")
def fcg():
    """
    Construct function call graph of a bril program
    """
    print("TODO")


@main.command
def stats():
    """
    Calculate and print various statistics about a bril program
    """
    prog = json.load(sys.stdin)
    print_toplevel_counts(prog)
    print_opcode_breakdown(prog)


if __name__ == "__main__":
    main()
