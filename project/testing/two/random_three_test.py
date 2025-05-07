import sys


def f(n, m):
    return all((m <= 4 * -2 for i in range(-6)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
