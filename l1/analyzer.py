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
    elif op in ("br", "jmp", "load", "store"):
        formatted += f"{op} {args_and_labels}"
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
            print(f"  {label}:")
            for i in block:
                print(f"    {format_instruction(i)}")


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
def print_cfg(cfg):
    print("digraph cfg {")
    for label in cfg.keys():
        print(f'"{label}"')
    print()
    for label, dests in cfg.items():
        for dest in dests:
            print(f'"{label}" -> "{dest}"')
    print("}")


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
def cfg():
    """
    Construct control flow graph of a bril program, labelled by labels from block command (printed out in graphviz dot language)
    """
    print_cfg(construct_cfg(parse_into_blocks(json.load(sys.stdin))))


@main.command
def stats():
    """
    Calculate and print various statistics about a bril program
    """
    pass


if __name__ == "__main__":
    main()
