import ast
import copy


def conjunctivize(tree):
    if type(tree) == ast.UnaryOp and type(tree.op) == ast.Not:
        dnf = disjunctivize(tree.operand)
        if type(dnf) == ast.BoolOp and type(dnf.op) == ast.And:
            tree = ast.BoolOp(
                ast.Or(),
                [
                    ast.UnaryOp(ast.Not(), copy.deepcopy(conjunct))
                    for conjunct in dnf.values
                ],
            )
        elif type(dnf) == ast.BoolOp and type(dnf.op) == ast.Or:
            tree = ast.BoolOp(
                ast.And(),
                [
                    ast.UnaryOp(ast.Not(), copy.deepcopy(disjunct))
                    for disjunct in dnf.values
                ],
            )
    elif type(tree) == ast.BoolOp and type(tree.op) == ast.Or:
        pass
    elif type(tree) == ast.BoolOp and type(tree.op) == ast.And:
        # distributive law:
        # p and (q or r) == (p and q) or (p and r)
        left = conjunctivize(tree.values[0])
        if len(tree.values) > 2:
            right = conjunctivize(ast.BoolOp(ast.And(), copy.deepcopy(tree.values[1:])))
        else:
            right = conjunctivize(tree.values[1])

        if type(right) == ast.BoolOp and type(right.op) == ast.Or:
            tree = ast.BoolOp(
                ast.Or(),
                [
                    ast.BoolOp(
                        ast.And(), [copy.deepcopy(left)] + [copy.deepcopy(disjunct)]
                    )
                    for disjunct in right.values
                ],
            )
        elif type(left) == ast.BoolOp and type(left.op) == ast.Or:
            tree = ast.BoolOp(
                ast.Or(),
                [
                    ast.BoolOp(
                        ast.And(), [copy.deepcopy(disjunct)] + [copy.deepcopy(right)]
                    )
                    for disjunct in left.values
                ],
            )
    if isinstance(tree, ast.AST):
        for name, value in ast.iter_fields(tree):
            if type(value) == list:
                setattr(tree, name, list(map(conjunctivize, value)))
            else:
                setattr(tree, name, conjunctivize(value))

    return tree


def disjunctivize(tree):
    if type(tree) == ast.UnaryOp and type(tree.op) == ast.Not:
        cnf = conjunctivize(tree.operand)
        if type(cnf) == ast.BoolOp and type(cnf.op) == ast.Or:
            tree = ast.BoolOp(
                ast.And(),
                [
                    ast.UnaryOp(ast.Not(), copy.deepcopy(disjunct))
                    for disjunct in cnf.values
                ],
            )
        elif type(cnf) == ast.BoolOp and type(cnf.op) == ast.And:
            tree = ast.BoolOp(
                ast.Or(),
                [
                    ast.UnaryOp(ast.Not(), copy.deepcopy(conjunct))
                    for conjunct in cnf.values
                ],
            )
    elif type(tree) == ast.BoolOp and type(tree.op) == ast.Or:
        # distributive law:
        # p or (q and r) == (p or q) and (p or r)
        left = disjunctivize(tree.values[0])
        if len(tree.values) > 2:
            right = disjunctivize(ast.BoolOp(ast.Or(), copy.deepcopy(tree.values[1:])))
        else:
            right = disjunctivize(tree.values[1])

        if type(right) == ast.BoolOp and type(right.op) == ast.And:
            tree = ast.BoolOp(
                ast.And(),
                [
                    ast.BoolOp(
                        ast.Or(), [copy.deepcopy(left)] + [copy.deepcopy(conjunct)]
                    )
                    for conjunct in right.values
                ],
            )
        elif type(left) == ast.BoolOp and type(left.op) == ast.And:
            tree = ast.BoolOp(
                ast.And(),
                [
                    ast.BoolOp(
                        ast.Or(), [copy.deepcopy(conjunct)] + [copy.deepcopy(right)]
                    )
                    for conjunct in left.values
                ],
            )
    elif type(tree) == ast.BoolOp and type(tree.op) == ast.And:
        pass

    if isinstance(tree, ast.AST):
        for name, value in ast.iter_fields(tree):
            if type(value) == list:
                setattr(tree, name, list(map(disjunctivize, value)))
            else:
                setattr(tree, name, disjunctivize(value))

    return tree
