import sys


def f(l, m, n):
    return any((n > 50 * (m + l) for i in range(n + 19, l - m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
