import utilities as ut

import copy
import json
import pprint
import collections
import sys

import click


def enumerate_paths(succs, entries, target):
    partial_paths = [[entry] for entry in entries]

    while len(partial_paths):
        path = partial_paths.pop(0)
        term = path[-1]
        if term == target:
            yield path
        else:
            for succ in succs[term]:
                if path.count(term) <= 1:
                    partial_paths.append(path + [succ])


def validate_dominators(prog, doms):
    _, succs, _, _, entry_blocks = ut.the_stuff(prog)

    for label in doms:
        return all(
            all(dom in path for path in enumerate_paths(succs, entry_blocks, label))
            for dom in doms[label]
        )


def print_dominators(dominators):
    def fmt(labels):
        return ", ".join(sorted(labels))

    longest_label = max(len(label) for label in dominators)
    longest_in = max(len(fmt(dominators[label])) for label in dominators)

    for label in sorted(dominators):
        doms = fmt(dominators[label])
        print(f'{label} {" "*(longest_label-len(label))} ::  dominated by - {{{doms}}}')


def print_dominator_tree_text(tree):
    def fmt(children):
        return ", ".join(sorted(children))

    longest_label = max(len(label) for label in tree)
    longest_children = max(len(fmt(tree[label])) for label in tree)

    for label in sorted(tree):
        children = fmt(tree[label])
        print(
            f'{label} {" "*(longest_label-len(label))} ::  strictly dominates - {{{children}}}'
        )


def print_dominator_tree_dot(tree):
    print("digraph dominator_tree {")
    for label, children in tree.items():
        for child in children:
            print(f'  "{label}" -> "{child}";')
    print("}")


def dominators(prog):
    blocks, succs, preds, labels_to_blocks, entry_blocks = ut.the_stuff(prog)

    doms_after = {
        label: set(l for l in labels_to_blocks.keys())
        for label in labels_to_blocks.keys()
    }
    doms = {}

    while doms != doms_after:
        doms = doms_after
        doms_after = copy.deepcopy(doms)
        for label in ut.reverse_post_order(succs):
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


@click.group
def main():
    pass


@main.command(name="sets")
@click.option(
    "--validate",
    is_flag=True,
    help="run (expensive) validation on generated dominator sets",
)
def dominator_sets_command(validate):
    """
    Compute dominator sets of basic blocks of bril program passed via stdin
    """
    prog = json.load(sys.stdin)

    doms = dominators(prog)

    if validate and not validate_dominators(prog, doms):
        print(f"VALIDATION FAILED")
        exit(1)

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
def dominator_tree_command(dot, validate):
    """
    Compute dominator tree of bril program passed via stdin
    """
    prog = json.load(sys.stdin)

    doms = dominators(prog)

    if validate and not validate_dominators(prog, doms):
        print(f"VALIDATION FAILED")
        exit(1)

    dom_tree = dominator_tree(doms)

    print_dominator_tree_dot(dom_tree) if dot else print_dominator_tree_text(dom_tree)


if __name__ == "__main__":
    main()
