import sys


def f(l, m, n):
    return all((not not m >= m for i in range(n, 40)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
