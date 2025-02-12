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


# TODO: should I create a unique exit block if one does not exist?
def construct_cfg(labels_and_blocks):
    cfg = {}
    for func, l_and_b in labels_and_blocks.items():
        for i, (label, block) in enumerate(l_and_b):
            cfg[label] = []
            term = block[-1]
            if term.get("op", "") in ("jmp", "br"):
                for dest in term["labels"]:
                    cfg[label].append(dest)
            elif term.get("op", "") == "ret":
                # ret indicates the end of a block
                pass
            elif i < len(l_and_b) - 1:
                cfg[label].append(l_and_b[i + 1][0])
    return cfg


def has_side_effects(instr):
    side_effective = ["store", "print", "call"]
    return "op" in instr and instr["op"] in side_effective


def global_optimization(optimization_pass):
    def outer(prog):
        out = {"functions": []}
        for func in prog["functions"]:
            out_func = copy.deepcopy(func)
            out_func["instrs"] = optimization_pass(copy.deepcopy(out_func["instrs"]))
            out["functions"].append(out_func)
        return out

    return outer


def local_optimization(optimization_pass):
    def outer(prog):
        out = {"functions": []}
        blocks = parse_into_blocks(prog)
        for func in prog["functions"]:
            out_func = copy.deepcopy(func)
            instrs = []
            for _, block in blocks[func["name"]]:
                instrs += optimization_pass(copy.deepcopy(block))
            out_func["instrs"] = instrs
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
