import ast


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
