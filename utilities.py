import copy
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


def coalesce_blocks(blocks):
    json_dict = {"functions": []}
    for func in blocks:
        func_dict = {"name": func}
        instrs = []
        for _, block in blocks[func]:
            instrs += block
        func_dict[instrs] = instrs
        json_dict["functions"].append(func_dict)
    return json_dict


def global_optimization(optimization):
    def outer(prog):
        out = {"functions": []}
        for func in prog["functions"]:
            out_func = copy.deepcopy(func)
            out_func["instrs"] = optimization(out_func["instrs"])
            out["functions"].append(out_func)
        return out

    return outer


def iterate_to_convergence(optimization_pass):
    def outer(instrs):
        old = None
        new = instrs
        while old != new:
            old = new
            new = optimization_pass(old)
        return new

    return outer
