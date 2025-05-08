import sys


def f(n):
    return all((31 == i for i in range(-8 * n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
