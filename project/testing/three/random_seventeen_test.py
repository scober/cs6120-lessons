import sys


def f(l, m, n):
    return all((-14 == 13 * m for i in range(42)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
