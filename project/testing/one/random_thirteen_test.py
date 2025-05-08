import sys


def f(n):
    return any((n < i for i in range(n, n - -1 - -14 + -34 + (n - 10 + -48))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
