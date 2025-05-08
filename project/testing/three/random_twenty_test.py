import sys


def f(l, m, n):
    return any((not not not (m - 5 < m or n < 46) for i in range(l, -31 * (-7 * m))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
