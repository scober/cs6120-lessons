import sys


def f(l, m, n):
    return any((not (not not -29 > m and (i == 9 and n != -31 * i - 44)) or n > -24 * l for i in range(l)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
