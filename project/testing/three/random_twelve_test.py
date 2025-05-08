import sys


def f(l, m, n):
    return all((not -2 >= 43 for i in range(17 * m + l)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
