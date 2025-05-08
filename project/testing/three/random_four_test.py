import sys


def f(l, m, n):
    return all((-19 * m - (-15 * (-21 - (31 * l - l)) - 18) != -48 * m - 14 * n for i in range(m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
