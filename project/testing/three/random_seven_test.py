import sys


def f(l, m, n):
    return any((n > n for i in range(11)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
