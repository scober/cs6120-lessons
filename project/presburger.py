import ast
import copy

import cnf


# this isn't finding actual presburger expressions, just the subset of
#   presburger expressions that I am currently capable of doing quantifier
#   elimination on
def is_presburger_expression(node):
    node_type = type(node)

    # a few things we want to treat as base cases (i.e. not recurse even though
    #   the nodes have children
    if node_type == ast.Name:
        return True
    if node_type == ast.Constant:
        return type(node.value) == int

    if not all(is_presburger_expression(child) for child in ast.iter_child_nodes(node)):
        return False

    if node_type in [ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not]:
        return True
    if node_type in [ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE]:
        return True
    if node_type == ast.BinOp:
        if type(node.op) == ast.Mult:
            return type(node.left) == ast.Constant or type(node.right) == ast.Constant
        else:
            return True
    if node_type in [ast.BinOp, ast.Add, ast.Sub, ast.Mult]:
        return True
    if node_type in [ast.GeneratorExp, ast.comprehension]:
        return True
    if node_type == ast.Call:
        return type(node.func) == ast.Name and node.func.id in ["any", "all", "range"]

    return False


def remove_all(node):
    # DeMorgan's Law:
    # all(p for ...) === not any(not p for ...)
    if node.func.id == "all":
        node = ast.UnaryOp(
            ast.Not(),
            ast.Call(
                ast.Name("any", ast.Load()),
                node.args,
                [],
            ),
        )
        generator = node.operand.args[0]
        predicate = generator.elt
        generator.elt = ast.UnaryOp(ast.Not(), predicate)

    return node


# this is called with an implicit "not" above the bool_op node
def demorganize(bool_op):
    assert type(bool_op) == ast.BoolOp

    predicates = [ast.UnaryOp(ast.Not(), predicate) for predicate in bool_op.values]

    if type(bool_op.op) == ast.And:
        return ast.BoolOp(ast.Or(), predicates)
    elif type(bool_op.op) == ast.Or:
        return ast.BoolOp(ast.And(), predicates)

    assert False, "unreachable"


# this is also called with an implicit "not" above the compare node
def invert_comparison(compare):
    assert type(compare) == ast.Compare
    # let's not deal with long strings of comparisons yet
    assert len(compare.comparators) == 1

    left = compare.left
    right = compare.comparators[0]
    comparison_type = type(compare.ops[0])

    swap = {
        ast.Eq: ast.NotEq,
        ast.NotEq: ast.Eq,
        ast.Lt: ast.GtE,
        ast.GtE: ast.Lt,
        ast.Gt: ast.LtE,
        ast.LtE: ast.Gt,
    }

    return ast.Compare(left, [swap[comparison_type]()], [right])


def modify_and_recurse(f):
    def recursive(node):
        node = f(node)

        if isinstance(node, ast.AST):
            for name, value in ast.iter_fields(node):
                if type(value) == list:
                    setattr(node, name, [recursive(child) for child in value])
                else:
                    setattr(node, name, recursive(value))

        return node

    return recursive


@modify_and_recurse
def push_down_nots(node):
    if type(node) == ast.UnaryOp and type(node.operand) in [
        ast.BoolOp,
        ast.Compare,
        ast.UnaryOp,
    ]:
        assert type(node.op) == ast.Not, type(node.op)

        if type(node.operand) == ast.BoolOp:
            node = demorganize(node.operand)
        elif type(node.operand) == ast.Compare:
            node = invert_comparison(node.operand)
        elif type(node.operand) == ast.UnaryOp:
            assert type(node.operand.op) == ast.Not, type(node.operand.op)
            node = node.operand.operand
    return node


@modify_and_recurse
def remove_inequality_checks(node):
    # because everything is an integer we have the following property:
    # a != b === (a < b) or (a > b)
    if type(node) == ast.Compare and type(node.ops[0]) == ast.NotEq:
        assert len(node.ops) == 1

        left = node.left
        right = node.comparators[0]

        node = ast.BoolOp(
            ast.Or(),
            [
                ast.Compare(left, [ast.Lt()], [right]),
                ast.Compare(left, [ast.Gt()], [right]),
            ],
        )
    return node


# any(p or q for ...) === any(p for ...) or any(q for ...)
def push_down_any(node):
    assert type(node) == ast.Call, type(node)
    generator = node.args[0]
    or_op = generator.elt
    if type(or_op) == ast.BoolOp and type(or_op.op) == ast.Or:
        anys = [
            ast.Call(
                ast.Name("any", ast.Load()),
                [copy.deepcopy(generator)],
                [],
            )
            for disjunct in or_op.values
        ]
        for a, disjunct in zip(anys, or_op.values):
            a.args[0].elt = disjunct
        return ast.BoolOp(ast.Or(), anys)
    return node


def get_qvar(node):
    return node.args[0].generators[0].target.id


ONE_STRING = "XXX one YYY"


def var_multiplicities(node, mults, multiplicity):
    if type(node) == ast.Name and type(node.ctx) == ast.Load:
        mults[node.id] = mults.get(node.id, 0) + multiplicity
    elif type(node) == ast.Constant:
        mults[ONE_STRING] = mults.get(ONE_STRING, 0) + multiplicity * node.value
    elif type(node) == ast.BinOp and type(node.op) == ast.Mult:
        const = node.left if type(node.left) == ast.Constant else node.right
        other = node.right if type(node.left) == ast.Constant else node.left
        var_multiplicities(other, mults, multiplicity * const.value)
    elif type(node) == ast.BinOp and type(node.op) in [ast.Add, ast.Sub]:
        var_multiplicities(node.left, mults, multiplicity)
        if type(node.op) == ast.Sub:
            multiplicity *= -1
        var_multiplicities(node.right, mults, multiplicity)
    else:
        for child in ast.iter_child_nodes(node):
            var_multiplicities(child, mults, multiplicity)


def separate_qvar(compare, qv):
    if type(compare) != ast.Compare:
        return compare

    assert len(compare.comparators) == 1, compare.comparators

    left_mults = {}
    var_multiplicities(compare.left, left_mults, 1)
    right_mults = {}
    var_multiplicities(compare.comparators[0], right_mults, 1)

    qv_mult = left_mults.pop(qv, 0) - right_mults.pop(qv, 0)
    left = ast.BinOp(ast.Constant(qv_mult), ast.Mult(), ast.Name(qv, ast.Load()))

    right = ast.Constant(0)
    allvars = set(left_mults.keys()).union(set(right_mults.keys()))
    for var in allvars:
        mult = right_mults.pop(var, 0) - left_mults.pop(var, 0)
        var_expression = (
            ast.Constant(mult)
            if var == ONE_STRING
            else ast.BinOp(ast.Constant(mult), ast.Mult(), ast.Name(var, ast.Load()))
        )
        right = ast.BinOp(right, ast.Add(), var_expression)

    return ast.Compare(left, [compare.ops[0]], [right])


# put all of our quanitifier variables on the left sides of our comparsions
def separate_all_qvars(node):
    qv = get_qvar(node)
    modify_and_recurse(lambda n: separate_qvar(n, qv))(node)
    return node


def eliminate_quantifiers(root):
    return_negation = False

    root = remove_all(root)
    if type(root) == ast.UnaryOp:
        assert type(root.op) == ast.Not, type(root.op)
        root = root.operand
        return_negation = True

    root = push_down_nots(root)
    root = remove_inequality_checks(root)
    root = cnf.conjunctivize(root)

    root = push_down_any(root)
    if type(root) != ast.Call:
        return ast.UnaryOp(ast.Not(), root) if return_negation else root

    root = separate_all_qvars(root)

    return ast.UnaryOp(ast.Not(), root) if return_negation else root
