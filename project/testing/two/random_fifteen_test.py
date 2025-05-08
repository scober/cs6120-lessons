import sys


def f(m, n):
    return all((i < n - (21 + i) or (21 * (m + m) != -29 and i <= n) for i in range(37, n + -32 - n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
