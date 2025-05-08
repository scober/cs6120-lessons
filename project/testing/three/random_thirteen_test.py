import sys


def f(l, m, n):
    return all((not (not not (-11 <= m or l == m) and (m > -25 or not m > n + -7 * (17 * (34 * m)))) for i in range(l)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
