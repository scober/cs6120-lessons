import ast
import inspect


def ast_test(f):
    ast.parse(inspect.getsource(f))
    return f


@ast_test
def test_func():
    print("testing!")


test_func()
