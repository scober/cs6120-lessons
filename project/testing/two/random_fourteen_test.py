import sys


def f(m, n):
    return all((m < -25 * (-17 * i) for i in range(m, -32)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
