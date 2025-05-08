import sys


def f(n):
    return any((-25 <= n - -16 * (-5 * (30 * i)) for i in range(11 + 14)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
