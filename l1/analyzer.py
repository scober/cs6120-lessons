import click

import json
import sys


def parse_into_blocks(prog):
    blocks = []
    label_number = -1
    for f in prog["functions"]:
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
    return blocks


def format_instruction(instruction):
    formatted = "  "

    tp = ""
    if "type" in instruction:
        if "ptr" in instruction["type"]:
            tp = f"ptr<{instruction['type']['ptr']}>"
        else:
            tp = instruction["type"]

    args = " ".join(instruction["args"]) if "args" in instruction else ""

    value = instruction["value"] if "value" in instruction else ""

    if "label" in instruction:
        return f"{instruction['label']}:"
    elif instruction["op"] == "br":
        formatted += f"br {args} {' '.join(instruction['labels'])}"
    elif instruction["op"] == "jmp":
        formatted += f"jmp {' '.join(instruction['labels'])}"
    elif instruction["op"] in ("load", "store"):
        formatted += f"{instruction['op']} {args}"
    elif instruction["op"] == "call":
        if "dest" in instruction:
            formatted += f"{instruction['dest']}: {tp} = "
        # TODO: funcs is a list, is it allowed to have multiple elements?
        formatted += f"@call {instruction['funcs'][0]} {args}"
    else:
        formatted += f"{instruction['dest']}: {tp} = {instruction['op']} {args}{value}"
    return formatted + ";"


def print_blocks(labels_and_blocks):
    for label, block in labels_and_blocks:
        print(f"{label}:")
        for i in block:
            # print(f"  {i}")
            print(f"  {format_instruction(i)}")


@click.group
def main():
    pass


@main.command
def cfg():
    pass


@main.command
def blocks():
    print_blocks(parse_into_blocks(json.load(sys.stdin)))


@main.command
def stats():
    pass


if __name__ == "__main__":
    main()
