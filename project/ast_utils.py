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


# my qe pass generates a lot of dumb stuff, so remove the dumbest stuff
# other things that would be nice to have:
#   more robust constant folding, specifically for expressions like
#     <constant> * (<constant> * <var>)
#   constant folding for boolean comparison operators
@recurse_and_modify
def simplify(node):
    if type(node) == ast.BoolOp:
        if type(node.op) == ast.Or:
            if any(type(v) == ast.Constant and v.value == True for v in node.values):
                return ast.Constant(True)
            node.values = list(filter(lambda v: type(v) != ast.Constant, node.values))
            return node
        elif type(node.op) == ast.And:
            if any(type(v) == ast.Constant and v.value == False for v in node.values):
                return ast.Constant(False)
            node.values = list(filter(lambda v: type(v) != ast.Constant, node.values))
            return node

    if type(node) == ast.BinOp:
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
        elif type(node.right) == ast.Constant:
            if (type(node.op) == ast.Add and node.right.value == 0) or (
                type(node.op) == ast.Mult and node.right.value == 1
            ):
                return node.left
    return node
