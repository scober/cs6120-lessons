import collections
import copy
import json
import pprint
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


def post_order(successors):
    # because this is a generator, we don't want to be sensitive to
    #   changes to the input during our runtime
    s = copy.deepcopy(successors)
    frontier = [
        block for block in s.keys() if all(block not in succs for succs in s.values())
    ]
    unvisited = [block for block in s.keys()]
    while len(frontier):
        block = frontier.pop(0)
        unvisited.remove(block) if block in unvisited else None
        frontier += [
            succ
            for succ in successors[block]
            if succ not in frontier and succ in unvisited
        ]
        if all(block not in s[f] for f in unvisited):
            yield block
        else:
            frontier.append(block)


# this is not really worth putting in a function, but one could hypothetically
#   calculate this more efficiently by doing it directly via the predecessors
#   graph and putting this in its own function is my nod to that fact -- maybe
#   one day I will do it that way
def reverse_post_order(successors):
    return reversed(list(post_order(successors)))


def data_flow_analysis(
    ret,
    worklist,
    successors,
    predecessors,
    labels_to_blocks,
    i,
    o,
    merge,
    transfer,
):
    # this function is written as if it is a backward pass,
    #   but it should work just as well for a forward pass
    while len(worklist):
        label, block = worklist.popleft()

        ins = tuple(ret[inpt][i] for inpt in successors[label])
        ret[label][o] = merge(ins)

        in_before = ret[label][i]
        in_after = transfer(copy.deepcopy(ret[label][o]), copy.deepcopy(block))
        ret[label][i] = in_after
        if in_before != in_after:
            for pred in predecessors[label]:
                worklist.append((pred, labels_to_blocks[pred]))

    return ret


def data_flow_prerequisites(prog, entry_init, general_init):
    blocks = parse_into_blocks(prog)
    successors = construct_cfg(blocks)
    predecessors = {label: [] for label in successors.keys()}
    for pred, succs in successors.items():
        for succ in succs:
            predecessors[succ].append(pred)
    labels_to_blocks = {
        label: block for l_and_b in blocks.values() for label, block in l_and_b
    }

    ret = {
        label: {"in": general_init(), "out": general_init()}
        for l_and_b in blocks.values()
        for label, _ in l_and_b
    }
    for label in ret:
        if not predecessors[label]:
            ret[label]["in"] = entry_init()

    return blocks, successors, predecessors, labels_to_blocks, ret


def forward_data_flow_analysis(prog, entry_init, general_init, merge, transfer):
    blocks, successors, predecessors, labels_to_blocks, ret = data_flow_prerequisites(
        prog, entry_init, general_init
    )

    worklist = collections.deque(
        (l, labels_to_blocks[l]) for l in post_order(successors)
    )

    return data_flow_analysis(
        ret,
        worklist,
        predecessors,
        successors,
        labels_to_blocks,
        "out",
        "in",
        merge,
        transfer,
    )


def backward_data_flow_analysis(prog, entry_init, general_init, merge, transfer):
    blocks, successors, predecessors, labels_to_blocks, ret = data_flow_prerequisites(
        prog, entry_init, general_init
    )
    worklist = collections.deque(
        (l, labels_to_blocks[l]) for l in reverse_post_order(successors)
    )

    return data_flow_analysis(
        ret,
        worklist,
        successors,
        predecessors,
        labels_to_blocks,
        "in",
        "out",
        merge,
        transfer,
    )
