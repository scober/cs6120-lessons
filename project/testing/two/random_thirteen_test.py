import sys


def f(m, n):
    return all((i - i >= 39 + -11 * (i + m - -36 * n) - m for i in range(n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
