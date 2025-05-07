import sys


def f(n, m):
    return all((10 <= 36 - -14 for i in range(m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
