import ast
import copy
import itertools
import math

import ast_utils
import cnf


# this isn't finding actual presburger expressions, just the subset of
#   presburger expressions that I am currently capable of doing quantifier
#   elimination on
def is_presburger_expression(node):
    node_type = type(node)

    # a few things we want to treat as base cases (i.e. not recurse even though
    #   the nodes have children
    if node_type in [ast.Name, ast.Load, ast.Store]:
        return True
    if node_type == ast.Constant:
        return type(node.value) == int or type(node.value) == bool

    if not all(is_presburger_expression(child) for child in ast.iter_child_nodes(node)):
        return False

    if node_type in [ast.UnaryOp, ast.Not, ast.USub]:
        return True
    if node_type in [ast.BoolOp, ast.And, ast.Or]:
        return True
    if node_type in [ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE]:
        return True
    if node_type == ast.BinOp and type(node.op) == ast.Mult:
        return type(node.left) == ast.Constant or type(node.right) == ast.Constant
    if node_type in [ast.BinOp, ast.Add, ast.Sub, ast.Mult]:
        return True
    if node_type in [ast.GeneratorExp, ast.comprehension]:
        return True
    if node_type == ast.Call and type(node.func) == ast.Name:
        return node.func.id in ["any", "all"] or (
            node.func.id == "range" and len(node.args) <= 2
        )

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


@ast_utils.modify_and_recurse
def push_down_nots(node):
    if type(node) == ast.UnaryOp and type(node.operand) in [
        ast.BoolOp,
        ast.Compare,
        ast.UnaryOp,
        ast.Constant,
    ]:
        assert type(node.op) == ast.Not, type(node.op)

        if type(node.operand) == ast.BoolOp:
            node = demorganize(node.operand)
        elif type(node.operand) == ast.Compare:
            node = invert_comparison(node.operand)
        elif type(node.operand) == ast.UnaryOp:
            assert type(node.operand.op) == ast.Not, type(node.operand.op)
            node = node.operand.operand
        elif type(node.operand) == ast.Constant:
            node = ast.Constant(not node.operand.value)
    return node


@ast_utils.modify_and_recurse
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


def var_in_predicate(var, node):
    return any(type(child) == ast.Name and child.id == var for child in ast.walk(node))


def remove_independent_predicates(node):
    qv = get_qvar(node)
    independents = []

    if type(node.args[0].elt) == ast.Constant:
        return node if node.args[0].elt.value else ast.Constant(False)

    @ast_utils.modify_and_recurse
    def remove_independent_conjuncts(node):
        if type(node) == ast.Compare and not var_in_predicate(qv, node):
            independents.append(node)
            return ast.Constant(True)
        if type(node) == ast.Constant and type(node.value) == bool:
            independents.append(node)
            return ast.Constant(True)
        return node

    node = ast_utils.simplify(remove_independent_conjuncts(node))

    return ast.BoolOp(ast.And(), independents + [node]) if independents else node


def get_bounds(node):
    range_args = node.args[0].generators[0].iter.args
    lower_bound = ast.Constant(0) if len(range_args) == 1 else range_args[0]
    upper_bound = range_args[-1]
    return lower_bound, upper_bound


def insert_bounds(node):
    qv = get_qvar(node)
    lower_bound, upper_bound = get_bounds(node)
    predicate = node.args[0].elt
    predicate = ast.BoolOp(
        ast.And(),
        [
            ast.Compare(ast.Name(qv, ast.Load()), [ast.GtE()], [lower_bound]),
            ast.Compare(ast.Name(qv, ast.Load()), [ast.Lt()], [upper_bound]),
            predicate,
        ],
    )
    node.args[0].elt = predicate
    return node


@ast_utils.modify_and_recurse
def remove_or_equals(node):
    if type(node) == ast.Compare and type(node.ops[0]) in [ast.LtE, ast.GtE]:
        new_op = ast.Lt() if node.ops[0] == ast.LtE else ast.Gt()
        adjustment = ast.Add() if node.ops[0] == ast.LtE else ast.Sub()
        node = ast.Compare(
            node.left,
            [new_op],
            [ast.BinOp(node.comparators[0], adjustment, ast.Constant(1))],
        )
    return node


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
    ast_utils.modify_and_recurse(lambda n: separate_qvar(n, qv))(node)
    return node


@ast_utils.recurse_and_modify
def push_down_multiplies(node):
    if type(node) == ast.BinOp and type(node.op) == ast.Mult:
        if type(node.left) == ast.BinOp:
            assert type(node.right) == ast.Constant
            return ast.BinOp(
                ast.BinOp(node.right, ast.Mult(), node.left.left),
                node.left.op,
                ast.BinOp(node.right, ast.Mult(), node.left.right),
            )
        elif type(node.right) == ast.BinOp:
            assert type(node.left) == ast.Constant
            return ast.BinOp(
                ast.BinOp(node.left, ast.Mult(), node.right.left),
                node.right.op,
                ast.BinOp(node.left, ast.Mult(), node.right.right),
            )
    return node


def unify_coefficients(node):
    qv = get_qvar(node)
    coefficients = set()
    for child in ast.walk(node):
        if (
            type(child) == ast.BinOp
            and type(child.right) == ast.Name
            and child.right.id == qv
        ):
            assert type(child.left) == ast.Constant, type(child.left)
            coefficients.add(child.left.value)
    lcm = math.lcm(*coefficients)

    @ast_utils.modify_and_recurse
    def unify(node):
        if type(node) == ast.Compare:
            if type(node.left) == ast.BinOp:
                assert type(node.left) == ast.BinOp, ast.dump(node, indent=2)
                assert type(node.left.op) == ast.Mult
                assert type(node.left.left) == ast.Constant

                current = node.left.left.value
            elif type(node.left) == ast.Name:
                assert node.left.id == qv
                current = 1

            adjustment = lcm // current
            assert current * adjustment == lcm

            if type(node.left) == ast.BinOp:
                node.left.left.value = lcm
            elif type(node.left) == ast.Name:
                node.left = ast.BinOp(ast.Constant(adjustment), ast.Mult(), node.left)
            node.comparators = [
                ast.BinOp(ast.Constant(adjustment), ast.Mult(), node.comparators[0])
            ]
            if adjustment < 0:
                if type(node.ops[0]) == ast.Lt:
                    node.ops[0] = ast.Gt()
                elif type(node.ops[0]) == ast.Gt:
                    node.ops[0] = ast.Lt()
        return node

    return unify(node)


# the intuition here is simple:
# (y == x) and (x < z) === y < z
def handle_equality(node):
    equality_value = None
    for child in ast.walk(node):
        if type(child) == ast.Compare and type(child.ops[0]) == ast.Eq:
            equality_value = child.comparators[0]
    if equality_value:

        @ast_utils.modify_and_recurse
        def insert_equality_value(node):
            if type(node) == ast.Compare:
                if node.comparators[0] == equality_value:
                    return ast.Constant(True)
                node.left = equality_value
            return node

        insert_equality_value(node)
        node = node.args[0].elt

    return node


# high level idea:
# our big predicate has two kinds of comparisons:
#   my < t_i(x)
#   and
#   my > t_j(x)
# where "x" is standing in here for the full set of free variables in our big
#   predicate
# for any given x, there will be a least t_i and a greatest t_j and the range
#   defined by those values will be the only thing we have to check m*y against
# it is possible to statically unroll the search for the least t_i and greatest
#   t_j in pure predicate logic:
#     do a disjunction over every unique t_i, t_j pair where
#     every disjunct checks whether there is a m*y value in the range (t_j, t_i)
#     and also asserts that t_j and t_i are maximal/minimal
#     (i.e. t_i < other_t_i and t_i < other_other_t_i and ... etc.)
#     then only the disjunct for the actual maximal/minimal pair will ever be
#     true and the truth value of the whole predicate will boil down to the
#     truth value of the m*y check
# HOWEVER!
# in an imperative programming language we don't need to do the full unrolling,
#   we can just dynamically find the least and greatest element and do the check!
# Finally, we can do the actual "m*y check" by checking if there is some value
#   in the range (t_j, t_i) that is divisible my m
# there are a handful of ways to do that check:
#   1. The "proper first order logic Presburger Arithmetic" way is to statically
#      unroll a loop that checks the first m values after t_j:
#      ((t_j + 1 % m == 0) and (t_j + 1 < t_i)) or ((t_j + 2 % m == 0) and ...
#   2. Ironically, in Python a natural way would be to add in a new
#      "quantifier":
#      any(x % m == 0 for x in range(t_j+1, t_i))
#   3. But I think the cheapest option is the following:
#      (t_i - t_j > m) or (t_i % m < t_j % m)
#      i.e. if there are m or more numbers in the range then one of them must be
#      divisible by m and if not, we just need to check for a "wrap-around"
#      between the beginning and end of the range
#
def handle_inequality(node):
    less_thans = set()
    greater_thans = set()
    m = None
    qv = get_qvar(node)
    for child in ast.walk(node):
        if type(child) == ast.Compare:
            if type(child.ops[0]) == ast.Lt:
                less_thans.add(child.comparators[0])
            elif type(child.ops[0]) == ast.Gt:
                greater_thans.add(child.comparators[0])
            else:
                assert False, ast.dump(child, indent=2)
        elif (
            type(child) == ast.BinOp
            and type(child.op) == ast.Mult
            and type(child.right) == ast.Name
            and child.right.id == qv
        ):
            m = child.left

    if not m:
        return node

    assert less_thans
    assert greater_thans

    least_lt = (
        less_thans.pop()
        if len(less_thans) == 1
        else ast.Call(ast.Name("min", ast.Load()), list(less_thans), [])
    )
    greatest_gt = (
        greater_thans.pop()
        if len(greater_thans) == 1
        else ast.Call(ast.Name("max", ast.Load()), list(greater_thans), [])
    )

    range_check = ast.Compare(
        ast.BinOp(least_lt, ast.Sub(), greatest_gt), [ast.Gt()], [m]
    )
    wraparound_check = ast.Compare(
        ast.BinOp(greatest_gt, ast.Mod(), m),
        [ast.Lt()],
        [ast.BinOp(least_lt, ast.Mod(), m)],
    )

    return ast.BoolOp(ast.Or(), [range_check, wraparound_check])


def eliminate_quantifiers(root):
    return_negation = False

    root = push_down_multiplies(root)
    root = ast_utils.simplify(root)

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

    root = remove_independent_predicates(root)
    if type(root) != ast.Call:
        return ast.UnaryOp(ast.Not(), root) if return_negation else root

    root = insert_bounds(root)
    root = remove_or_equals(root)
    root = separate_all_qvars(root)

    root = ast_utils.simplify(root)
    root = unify_coefficients(root)

    root = handle_equality(root)
    if type(root) != ast.Call:
        return ast.UnaryOp(ast.Not(), root) if return_negation else root

    root = handle_inequality(root)

    return ast.UnaryOp(ast.Not(), root) if return_negation else root
