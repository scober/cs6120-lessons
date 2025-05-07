import sys


def f(n, m):
    return all((-25 == -42 for i in range(32)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
