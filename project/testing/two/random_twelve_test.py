import sys


def f(m, n):
    return any((not -21 < i for i in range(-47, m - n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
