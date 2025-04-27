# This is not great, but the compile call seems to fail without it
from ast import *
import inspect
import types


def ast_test(f):
    source = inspect.getsource(f)
    lines = source.split("\n")
    # I can't explain exactly why this is necessary, but it makes a little sense
    #   I think
    if lines[0] == "@ast_test":
        source = "\n".join(lines[1:])

    parsed = parse(source, inspect.getsourcefile(f))
    compiled = compile(parsed, inspect.getsourcefile(f), "exec")
    return types.FunctionType(compiled, globals())


@ast_test
def test_func():
    print("testing!")


# the first call to the decorated function doesn't seem to do anything but all
#   the subsequent calls look normal
test_func()
test_func()
test_func()
test_func()
