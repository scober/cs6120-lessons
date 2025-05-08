import sys


def f(m, n):
    return all((-42 * m < i for i in range(-11 * m, n + 5)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
