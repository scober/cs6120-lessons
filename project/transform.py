from pathlib import Path

import ast
import copy

import click

import cnf


# this could be sped up by storing a parent mapping on the first call and just
#   referring back to it on future calls
def find_parent(node, tree):
    for parent in ast.walk(tree):
        if any(node == child for child in ast.iter_child_nodes(parent)):
            return parent
    assert False
    return None


# this is named a little misleadingly, but it does its best
# this sort of test is actually not possible in general because Python variables
#   don't have types associated with them
def is_pa(node):
    if type(node) == ast.Constant and type(node.value) == int:
        return True
    if type(node) in [ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE]:
        return True
    if type(node) in [ast.UnaryOp, ast.Not]:
        return True
    if type(node) in [ast.BinOp, ast.Add, ast.Sub, ast.Mod]:
        return True
    if type(node) in [ast.BoolOp, ast.And, ast.Or]:
        return True
    if type(node) in [ast.Name, ast.Load, ast.Store]:
        return True
    if type(node) == ast.Call:
        return type(node.func) == ast.Name and node.func.id in ["any", "all", "range"]
    if type(node) in [ast.comprehension, ast.GeneratorExp]:
        return True
    return False


def is_quantifier(node):
    return (
        type(node) == ast.Call
        and type(node.func) == ast.Name
        and node.func.id in ["any", "all"]
    )


def is_candidate(node):
    return is_quantifier(node) or (
        type(node) == ast.UnaryOp
        and type(node.op) == ast.Not
        and is_quantifier(node.operand)
    )


# I really want this algorithm to run starting at the leaves and recursing up
#   but AST nodes don't seem to store any information about their parents
#
# I guess if I wanted to preserve this algorithm design but make it faster I
#   could build a set of backedges in one pass and then write the algorithm I
#   wanted?
#
# But I think this inefficient version works for now
def pa_expressions(tree):
    expressions = None

    new_expressions = set()
    while expressions != new_expressions:
        expressions = new_expressions
        new_expressions = set()
        for node in ast.walk(tree):
            if is_pa(node) and all(
                child in expressions for child in ast.iter_child_nodes(node)
            ):
                new_expressions.add(node)

    return [
        expression
        for expression in expressions
        if find_parent(expression, tree) not in expressions
    ]


def presburger_elimination_possibilities(tree):
    yield from (
        expression for expression in pa_expressions(tree) if is_candidate(expression)
    )


def replace_subtree(tree, root, transform):
    parent = find_parent(root, tree)
    attr = None
    for name, value in ast.iter_fields(parent):
        if value == root:
            attr = name
    assert attr

    transformed = transform(root)
    setattr(parent, attr, transformed)
    return transformed


def remove_alls_from_subtree(tree, root):
    new_root = root
    for node in ast.iter_child_nodes(root):
        remove_alls_from_subtree(tree, node)
    if is_quantifier(root) and root.func.id == "all":

        def demorganize(node):
            # DeMorgan's Law:
            # all(predicate) == not any(not predicate)
            predicate = node.args[0]
            return ast.UnaryOp(
                ast.Not(),
                ast.Call(
                    ast.Name("any", ast.Load()),
                    [ast.UnaryOp(ast.Not(), predicate)],
                    [],
                ),
            )

        new_root = replace_subtree(tree, root, demorganize)
    return tree, new_root


def remove_alls(tree, roots):
    new_roots = set()
    for root in roots:
        tree, new_root = remove_alls_from_subtree(tree, root)
        new_roots.add(new_root)

    return tree, new_roots


def conjunctive_normal_form(tree, roots):
    new_roots = set()
    for root in roots:
        new_root = replace_subtree(tree, root, cnf.conjunctivize)
        new_roots.add(new_root)

    return tree, new_roots


def swap_any_with_or(any_node):
    generator_node = any_node.args[0]
    assert type(generator_node) == ast.GeneratorExp
    or_node = generator_node.elt
    if type(or_node) != ast.BoolOp or type(or_node.op) != ast.Or:
        return any_node
    left = copy.deepcopy(generator_node)
    right = copy.deepcopy(generator_node)
    anys = [
        ast.Call(
            ast.Name("any", ast.Load()),
            [copy.deepcopy(generator_node)],
            [],
        )
        for disjunct in or_node.values
    ]
    for a, d in zip(anys, or_node.values):
        a.args[0].elt = d

    return ast.BoolOp(ast.Or(), anys)


# any(p or q) == any(p) or any(q)
def push_down_anys(tree, roots):
    # we need to do this in bottom-up order -- the spec does not promise that
    #   ast.walk will iterate in that order, but it does
    # so this is a little brittle but probably fine for this project
    for root in roots:
        for node in ast.walk(root):
            if is_quantifier(node):
                # there should be no more calls to all() left
                replace_subtree(tree, node, swap_any_with_or)
    return tree, roots


def eliminate_quantifiers(tree, roots):
    return tree, roots


def do_presburger_elimination(tree):
    candidates = presburger_elimination_possibilities(tree)

    # removing instances of all regularizes the tree
    tree, roots = remove_alls(tree, candidates)
    # as does putting each predicate into conjunctive normal form
    tree, roots = conjunctive_normal_form(tree, roots)
    tree, roots = push_down_anys(tree, roots)
    tree, roots = eliminate_quantifiers(tree, roots)

    return tree


@click.group
def cli():
    pass


@cli.command(name="pass")
@click.argument("filename", type=str)
def transformation_pass_command(filename):
    path = Path(filename)
    with open(path, "r") as file:
        # print(ast.dump(ast.parse(file.read()), indent=2))
        transformed = do_presburger_elimination(ast.parse(file.read()))
        transformed_path = path.with_stem(str(path.stem) + "_pa_qe")
        with open(transformed_path, "w") as transformed_file:
            transformed_file.write(ast.unparse(transformed))


@cli.command(name="dry")
@click.argument("filename", type=str)
def dry_run_command(filename):
    print()
    with open(filename, "r") as file:
        possibilities = presburger_elimination_possibilities(ast.parse(file.read()))
        for expression in possibilities:
            if hasattr(expression, "lineno"):
                print(f"beginning on line {expression.lineno}:")
            else:
                print(f"beginning on unknown line:")
            print("  ", end="")
            print(ast.unparse(expression))
            print()


if __name__ == "__main__":
    cli()
