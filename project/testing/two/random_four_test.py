import sys


def f(n, m):
    return any((12 >= -18 and -27 > -37 for i in range(47)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
