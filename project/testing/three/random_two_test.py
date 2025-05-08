import sys


def f(l, m, n):
    return any((26 >= m or not i <= i + (m - l - m) + l - m for i in range(-7 * (46 + -49), n - m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
