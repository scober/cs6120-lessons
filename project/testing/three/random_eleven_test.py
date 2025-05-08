import sys


def f(l, m, n):
    return any((not 50 == -35 + m - n for i in range(42 * (6 * l))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
