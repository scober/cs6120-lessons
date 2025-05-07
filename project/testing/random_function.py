import ast
import itertools
import random

import click


def test_file(function_body):
    file = []

    file.append("import sys")
    file.append("")
    file.append("")
    file.append(ast.unparse(function_body))
    file.append("")
    file.append("")
    file.append("if __name__ == '__main__':")
    file.append("    for line in sys.stdin:")
    file.append("        inputs = list(map(int, line.split(' ')))")
    file.append("        print(f(*inputs))")

    return "\n".join(file)


def constant():
    return ast.Constant(random.randint(-50, 50))


def arithmetic_expression(free_vars):
    # make constants more common to avoid super deep expressions
    #   (super deep expressions result in large numbers take forever to run)
    op = random.choice(
        ([ast.Constant] * 2) + ([ast.Name] * 4) + [ast.Mult, ast.Add, ast.Sub]
    )
    if op == ast.Constant:
        return constant()
    elif op == ast.Name:
        return ast.Name(random.choice(free_vars), ast.Load())
    elif op == ast.Mult:
        return ast.BinOp(constant(), ast.Mult(), arithmetic_expression(free_vars))
    else:
        return ast.BinOp(
            arithmetic_expression(free_vars), op(), arithmetic_expression(free_vars)
        )


def boolean_predicate(free_vars):
    op = random.choice([ast.Not, ast.And, ast.Or] + ([ast.Compare] * 3))
    if op == ast.Compare:
        c = random.choice([ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE])
        return ast.Compare(
            arithmetic_expression(free_vars), [c()], [arithmetic_expression(free_vars)]
        )
    elif op == ast.Not:
        return ast.UnaryOp(ast.Not(), boolean_predicate(free_vars))
    else:
        return ast.BoolOp(
            op(), [boolean_predicate(free_vars), boolean_predicate(free_vars)]
        )


def range_call(free_vars):
    return ast.Call(
        ast.Name("range", ast.Load()),
        [arithmetic_expression(free_vars) for _ in range(random.randint(1, 2))],
        [],
    )


def generator_expression(free_vars):
    return ast.GeneratorExp(
        boolean_predicate(free_vars + ["i"]),
        [ast.comprehension(ast.Name("i", ast.Store()), range_call(free_vars), [], 0)],
    )


def quantifier_expression(free_vars):
    return ast.Call(
        ast.Name(random.choice(["any", "all"]), ast.Load()),
        [generator_expression(free_vars)],
        [],
    )


def f_function(arg_names):
    func_body = ast.Return(quantifier_expression(arg_names))
    f = ast.FunctionDef(
        name="f",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg=a) for a in arg_names],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[func_body],
        decorator_list=[],
        type_params=[],
    )
    f.lineno = 4
    return f


@click.group
def cli():
    pass


@cli.command
def one():
    print(test_file(f_function(["n"])))


@cli.command
def two():
    print(test_file(f_function(["m", "n"])))


@cli.command
def three():
    print(test_file(f_function(["l", "m", "n"])))


if __name__ == "__main__":
    cli()
