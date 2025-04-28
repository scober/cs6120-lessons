import ast
import click


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


def is_candidate(node):
    return (
        type(node) == ast.Call
        and type(node.func) == ast.Name
        and node.func.id in ["any", "all"]
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
        if not any(expression in ast.iter_child_nodes(node) for node in expressions)
    ]


def presburger_elimination_possibilities(file_contents):
    parsed = ast.parse(file_contents)
    expressions = pa_expressions(parsed)
    return [expression for expression in expressions if is_candidate(expression)]


@click.group
def cli():
    pass


@cli.command(name="dry")
@click.argument("filename", type=str)
def dry_run_command(filename):
    print()
    with open(filename, "r") as file:
        possibilities = presburger_elimination_possibilities(file.read())
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
