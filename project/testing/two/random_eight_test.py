import sys


def f(n, m):
    return any(((-20 < -33 + m or -46 <= m) or -33 > 43 * -41 + -28 * m for i in range(47, -41)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
