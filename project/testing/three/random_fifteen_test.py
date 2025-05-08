import sys


def f(l, m, n):
    return all((not ((13 <= 29 and (not l == 3)) and (-20 == m and (not ((not (-20 == n and -46 * -33 <= -5 * i) and 4 + -19 * i != m or n == 47 * (5 - -22 * l)) or ((-25 * n < i and -19 * i <= l) and (not 49 == n)))))) for i in range(l, n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
