import sys


def f(m, n):
    return any((n + -28 - -17 != -35 for i in range(31)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
