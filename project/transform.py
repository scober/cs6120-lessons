from pathlib import Path

import ast
import copy
import os

import click

import ast_utils
import cnf
import presburger


def replace_subtree(tree, root, transform):
    parent = ast_utils.find_parent(root, tree)
    transformed = None
    for name, value in ast.iter_fields(parent):
        if value == root:
            transformed = transform(root)
            setattr(parent, name, transformed)
        elif type(value) == list and root in value:
            index = value.index(root)
            transformed = transform(root)
            value[index] = transformed
    assert transformed
    return transformed


def unnested_presburger_quantifiers(tree):
    return filter(
        lambda node: all(
            descendent == node or not ast_utils.is_quantifier(descendent)
            for descendent in ast.walk(node)
        ),
        filter(
            ast_utils.is_quantifier,
            filter(presburger.is_presburger_expression, ast.walk(tree)),
        ),
    )


def do_presburger_elimination(tree):
    # we don't want to lazily evaluate this generator because we are going to be
    #   modifying the tree in place
    roots = list(unnested_presburger_quantifiers(tree))
    while roots:
        for root in roots:
            replace_subtree(tree, root, presburger.eliminate_quantifiers)
        roots = list(unnested_presburger_quantifiers(tree))

    return tree


@click.group
def cli():
    pass


@cli.command(name="pass")
@click.argument("filename", type=str)
def transformation_pass_command(filename):
    path = Path(filename)
    with open(path, "r") as file:
        transformed = do_presburger_elimination(ast.parse(file.read()))
        transformed = ast_utils.simplify(transformed)
        transformed_path = path.with_stem(str(path.stem) + "_pa_qe")
        with open(transformed_path, "w") as transformed_file:
            transformed_file.write(ast.unparse(transformed))


def print_possibilities(filename):
    print(filename)
    with open(filename, "r") as file:
        possibilities = unnested_presburger_quantifiers(ast.parse(file.read()))
        for expression in possibilities:
            if hasattr(expression, "lineno"):
                print(f"  beginning on line {expression.lineno}:")
            else:
                print(f"  beginning on unknown line:")
            print("    ", end="")
            print(ast.unparse(expression))
            print()


@cli.command(name="dry")
@click.argument("file_or_dir", type=str)
def dry_run_command(file_or_dir):
    print()
    if os.path.isfile(file_or_dir):
        print_possibilities(file_or_dir)
    else:
        for root, _, files in os.walk(file_or_dir):
            for file in files:
                if file.endswith(".py"):
                    print_possibilities(os.path.join(root, file))


if __name__ == "__main__":
    cli()
