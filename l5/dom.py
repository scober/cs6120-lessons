import utilities as ut

import copy
import json
import pprint
import collections
import sys

import click


def print_dominators(dominators):
    def fmt(labels):
        return ", ".join(sorted(labels))

    longest_label = max(len(label) for label in dominators)
    longest_in = max(len(fmt(dominators[label])) for label in dominators)

    for label in sorted(dominators):
        doms = fmt(dominators[label])
        print(f'{label} {" "*(longest_label-len(label))} ::  dominated by - {{{doms}}}')


def dominators(prog):
    blocks, succs, preds, labels_to_blocks, _ = ut.data_flow_prerequisites(
        prog, lambda: None, lambda: None
    )
    entries = [func[0][0] for func in blocks.values()]

    doms_after = {
        label: set(l for l in labels_to_blocks.keys())
        for label in labels_to_blocks.keys()
    }
    doms = {}

    while doms != doms_after:
        doms = doms_after
        doms_after = copy.deepcopy(doms)
        for label in ut.reverse_post_order(succs):
            if label in entries:
                doms_after[label] = set([label])
            else:
                pred_doms = set(l for l in labels_to_blocks.keys())
                for p in preds[label]:
                    pred_doms &= doms_after[p]
                doms_after[label] = set([label]).union(pred_doms)

    return doms


@click.group
def main():
    pass


@main.command(name="sets")
@click.option(
    "--validate",
    is_flag=True,
    help="run (expensive) validation on generated dominator sets",
)
def dominator_sets(validate):
    """
    Compute dominator sets of basic blocks of bril program passed via stdin
    """
    prog = json.load(sys.stdin)

    doms = dominators(prog)

    # pprint.pprint(doms)
    print_dominators(doms)


@main.command(name="tree")
@click.option(
    "--dot", is_flag=True, help="print out dominator tree in graphviz dot language"
)
@click.option(
    "--validate",
    is_flag=True,
    help="run (expensive) validation on generated dominator tree",
)
def dominator_tree(dot, validate):
    """
    Compute dominator tree of bril program passed via stdin
    """
    prog = json.load(sys.stdin)


if __name__ == "__main__":
    main()
