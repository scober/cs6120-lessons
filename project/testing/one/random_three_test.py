import sys


def f(n):
    return any((-9 * n < n for i in range(n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
