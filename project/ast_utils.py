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
