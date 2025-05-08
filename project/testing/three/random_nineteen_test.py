import sys


def f(l, m, n):
    return all((not (l - m <= l or (not ((not i <= l or (not (n == 32 * (-1 * (l + n)) and ((not (not n >= l or 13 * m == m) or (-37 * -14 < -7 - -48 and -34 > l)) or (l < -36 + (m + m) and ((-35 < i or (i >= m + l or not i == 22 - -39)) and i != l)))) or ((not 38 * m >= 39 + i - n and 12 > 25 - n) and (not -29 < l)))) and (not n <= l + l)) or -43 - m != i + -26 * n)) for i in range(-40 + (11 + n) + -19, n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
