import ast


# this could be sped up by storing a parent mapping on the first call and just
#   referring back to it on future calls
def find_parent(node, tree):
    for parent in ast.walk(tree):
        if any(node == child for child in ast.iter_child_nodes(parent)):
            return parent
    assert False
    return None


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


def recurse_and_modify(f):
    def recursive(node):
        if isinstance(node, ast.AST):
            for name, value in ast.iter_fields(node):
                if type(value) == list:
                    setattr(node, name, [recursive(child) for child in value])
                else:
                    setattr(node, name, recursive(value))

        node = f(node)

        return node

    return recursive


# this is why languages (including this one) have pattern matching
#   I didn't intend for this function to be so big, but here we are
#   I suppose this is a lesson in just using the right tool for the job from the
#     beginning
@recurse_and_modify
def simplify(node):
    if (
        type(node) == ast.Compare
        and type(node.left) == ast.Constant
        and type(node.comparators[0]) == ast.Constant
    ):
        op_type = type(node.ops[0])
        l = node.left.value
        r = node.comparators[0].value
        if op_type == ast.Lt:
            return ast.Constant(l < r)
        if op_type == ast.Gt:
            return ast.Constant(l > r)
        if op_type == ast.LtE:
            return ast.Constant(l <= r)
        if op_type == ast.GtE:
            return ast.Constant(l >= r)
        if op_type == ast.Eq:
            return ast.Constant(l == r)
        if op_type == ast.NotEq:
            return ast.Constant(l != r)

    if type(node) == ast.UnaryOp:
        if type(node.op) == ast.Not and type(node.operand) == ast.Constant:
            return ast.Constant(not node.operand.value)
        if type(node.op) == ast.USub:
            if type(node.operand) == ast.Constant:
                return ast.Constant(-1 * node.operand.value)

    if type(node) == ast.BoolOp:
        if type(node.op) == ast.Or:
            if any(type(v) == ast.Constant and v.value == True for v in node.values):
                return ast.Constant(True)
            node.values = list(filter(lambda v: type(v) != ast.Constant, node.values))
            return (
                node
                if len(node.values) > 1
                else node.values[0] if len(node.values) == 1 else ast.Constant(False)
            )
        elif type(node.op) == ast.And:
            if any(type(v) == ast.Constant and v.value == False for v in node.values):
                return ast.Constant(False)
            node.values = list(filter(lambda v: type(v) != ast.Constant, node.values))
            return (
                node
                if len(node.values) > 1
                else node.values[0] if len(node.values) == 1 else ast.Constant(True)
            )

    if type(node) == ast.BinOp:
        if (
            type(node.op) == ast.Mod
            and type(node.right) == ast.Constant
            and node.right.value == 1
        ):
            return ast.Constant(0)
        if (
            type(node.op) == ast.Sub
            and type(node.right) == ast.Constant
            and node.right.value < 0
        ):
            return ast.BinOp(node.left, ast.Add(), ast.Constant(-1 * node.right.value))

        if type(node.left) == ast.Constant and type(node.right) == ast.Constant:
            if type(node.op) == ast.Add:
                return ast.Constant(node.left.value + node.right.value)
            elif type(node.op) == ast.Sub:
                return ast.Constant(node.left.value - node.right.value)
            elif type(node.op) == ast.Mult:
                return ast.Constant(node.left.value * node.right.value)
        elif type(node.left) == ast.Constant:
            if (type(node.op) == ast.Add and node.left.value == 0) or (
                type(node.op) == ast.Mult and node.left.value == 1
            ):
                return node.right
            if type(node.op) == ast.Mult and node.left.value == 0:
                return ast.Constant(0)
        elif type(node.right) == ast.Constant:
            if (type(node.op) == ast.Add and node.right.value == 0) or (
                type(node.op) == ast.Mult and node.right.value == 1
            ):
                return node.left
            if type(node.op) == ast.Mult and node.right.value == 0:
                return ast.Constant(0)

    return node
