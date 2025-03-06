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


# did I get post-order backwards?
# yes, this function is not post-order traversal
def post_order(succs):
    # because this is a generator, we don't want to be sensitive to
    #   changes to the input during our runtime
    s = copy.deepcopy(succs)
    frontier = [
        block for block in s.keys() if all(block not in succs for succs in s.values())
    ]
    unvisited = [block for block in s.keys()]
    while len(frontier):
        block = frontier.pop(0)
        unvisited.remove(block) if block in unvisited else None
        frontier += [
            succ for succ in succs[block] if succ not in frontier and succ in unvisited
        ]
        if all(block not in s[f] for f in unvisited):
            yield block
        else:
            frontier.append(block)


# this is not really worth putting in a function, but one could hypothetically
#   calculate this more efficiently by doing it directly via the preds
#   graph and putting this in its own function is my nod to that fact -- maybe
#   one day I will do it that way
def reverse_post_order(succs):
    return reversed(list(post_order(succs)))


def data_flow_analysis(
    ret,
    worklist,
    succs,
    preds,
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

        ins = tuple(ret[inpt][i] for inpt in succs[label])
        ret[label][o] = merge(ins)

        in_before = ret[label][i]
        in_after = transfer(copy.deepcopy(ret[label][o]), copy.deepcopy(block))
        ret[label][i] = in_after
        if in_before != in_after:
            for pred in preds[label]:
                worklist.append((pred, labels_to_blocks[pred]))

    return ret


def predecessors(succs):
    preds = {label: [] for label in succs.keys()}
    for pred, sucs in succs.items():
        for suc in sucs:
            preds[suc].append(pred)
    return preds


def the_stuff(prog):
    blocks = parse_into_blocks(prog)
    succs = construct_cfg(blocks)
    preds = predecessors(succs)
    labels_to_blocks = {
        label: block for l_and_b in blocks.values() for label, block in l_and_b
    }
    entry_blocks = [func[0][0] for func in blocks.values()]

    return blocks, succs, preds, labels_to_blocks, entry_blocks


def data_flow_prerequisites(prog, entry_init, general_init):
    blocks, succs, preds, labels_to_blocks, entry_blocks = the_stuff(prog)

    ret = {
        label: {"in": general_init(), "out": general_init()}
        for l_and_b in blocks.values()
        for label, _ in l_and_b
    }
    for entry_label in entry_blocks:
        ret[entry_label]["in"] = entry_init()

    return blocks, succs, preds, labels_to_blocks, ret


def forward_data_flow_analysis(prog, entry_init, general_init, merge, transfer):
    blocks, succs, preds, labels_to_blocks, ret = data_flow_prerequisites(
        prog, entry_init, general_init
    )

    worklist = collections.deque(
        (l, labels_to_blocks[l]) for l in reverse_post_order(succs)
    )

    return data_flow_analysis(
        ret,
        worklist,
        preds,
        succs,
        labels_to_blocks,
        "out",
        "in",
        merge,
        transfer,
    )


def backward_data_flow_analysis(prog, entry_init, general_init, merge, transfer):
    blocks, succs, preds, labels_to_blocks, ret = data_flow_prerequisites(
        prog, entry_init, general_init
    )
    worklist = collections.deque((l, labels_to_blocks[l]) for l in post_order(succs))

    return data_flow_analysis(
        ret,
        worklist,
        succs,
        preds,
        labels_to_blocks,
        "in",
        "out",
        merge,
        transfer,
    )


def dominators(prog):
    blocks, succs, preds, labels_to_blocks, entry_blocks = the_stuff(prog)

    doms_after = {
        label: set(l for l in labels_to_blocks.keys())
        for label in labels_to_blocks.keys()
    }
    doms = {}

    while doms != doms_after:
        doms = doms_after
        doms_after = copy.deepcopy(doms)
        for label in reverse_post_order(succs):
            if label in entry_blocks:
                doms_after[label] = set([label])
            else:
                pred_doms = set(l for l in labels_to_blocks.keys())
                for p in preds[label]:
                    pred_doms &= doms_after[p]
                doms_after[label] = set([label]).union(pred_doms)

    return doms


def dominator_tree(doms):
    d = collections.OrderedDict(doms)
    tree = {entry: [] for entry in doms}

    while len(d):
        label, dominators = d.popitem(last=False)
        if dominators == set([label]):
            for dtee, dtors in d.items():
                if dtors == set((label, dtee)):
                    tree[label].append(dtee)
                d[dtee] = set(dom for dom in dtors if dom != label)
        else:
            d[label] = dominators

    return tree


def dominator_frontiers(doms, preds):
    # turn this into strict dominators
    sd = {
        dominatee: set(dom for dom in dominators if dom != dominatee)
        for dominatee, dominators in doms.items()
    }
    return {
        label: [
            l
            for l in doms.keys()
            if label not in sd[l] and any(label in doms[pred] for pred in preds[l])
        ]
        for label in doms.keys()
    }


# this is a fold, maybe write it that way?
def all_vars_in_block(block):
    all_vars = set()
    for instr in block:
        all_vars.add(instr.get("dest", None))
        all_vars |= set(instr.get("args", []))
    all_vars.discard(None)
    return all_vars


# this is also a fold
def all_vars_in_prog(prog):
    all_vars = set()
    _, _, _, labels_to_blocks, _ = the_stuff(prog)
    for block in labels_to_blocks.values():
        all_vars |= all_vars_in_block(block)
    return all_vars


def all_vars_in_prog_with_types(prog):
    all_dests = {}
    function_args = {
        arg["name"]: arg["type"]
        for function in prog["functions"]
        for arg in function.get("args", [])
    }
    _, _, _, labels_to_blocks, _ = the_stuff(prog)
    for block in labels_to_blocks.values():
        old_dests = copy.deepcopy(all_dests)
        all_dests |= all_dests_in_block_with_types(block)
        assert all(
            d in all_dests for d in old_dests
        ), "Don't use this in a context where you might have conflicting variable names!"

    for name, tipe in function_args.items():
        if name in all_dests:
            assert all_dests[name] == function_args[name]
            all_dests.pop(name)
    return function_args, all_dests


def append_to_block(instr, block):
    index = len(block)
    if block and block[-1].get("op", "") in ["jmp", "br"]:
        index -= 1
    block.insert(index, instr)


def prepend_to_block(instr, block):
    index = 0
    if block and "label" in block[0]:
        index += 1
    block.insert(index, instr)
