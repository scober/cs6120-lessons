import utilities as ut

import copy
import json
import pprint
import collections
import sys

import click


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
    blocks = ut.parse_into_blocks(prog)
    successors = ut.construct_cfg(blocks)
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
        reversed(l_and_b for func in blocks.values() for l_and_b in func)
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
        l_and_b for func in blocks.values() for l_and_b in func
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


def print_set_analysis(analysis):
    longest_label = max(len(label) for label in analysis)
    longest_in = max(len(", ".join(analysis[label]["in"])) for label in analysis)
    for label in analysis:
        ins = ", ".join(sorted(analysis[label]["in"]))
        outs = ", ".join(sorted(analysis[label]["out"]))
        print(
            f'{label} {" "*(longest_label-len(label))} ::  in - {{{ins}}} {" "*(longest_in-len(ins))}  //   out - {{{outs}}}'
        )


@click.group
def main():
    pass


@main.command(name="live")
def live_variables():
    prog = json.load(sys.stdin)

    def live_variables_transfer(live_out, block):
        live_in = copy.deepcopy(live_out)
        for instr in reversed(block):
            if "dest" in instr:
                live_in.discard(instr["dest"])
            uses = (
                instr.get("args", [])
                # + instr.get("values", [])
                # + ([instr["value"]] if "value" in instr else [])
            )
            for var in uses:
                live_in.add(var)
        return live_in

    analysis = backward_data_flow_analysis(
        prog, set, set, lambda sets: set().union(*sets), live_variables_transfer
    )

    print_set_analysis(analysis)


if __name__ == "__main__":
    main()
