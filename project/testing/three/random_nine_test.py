import sys


def f(l, m, n):
    return all((m > i - i for i in range(-35)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
