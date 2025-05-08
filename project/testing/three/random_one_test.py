import sys


def f(l, m, n):
    return any(((i < n or ((l >= n or (m >= n or m > n)) and (n == i or not (((-45 != n and (m > -15 and 21 + (33 + n + 37) >= n + 2)) and n == 37 * (-20 * (i - -22)) + n or n < n) and (-3 != -42 * 3 and (not i >= m)))))) or (16 <= i or ((-9 - l < i + 23 * 42 or (-19 * m < -3 and n <= -40)) or 23 * n >= 21)) for i in range(m - (l + 15 + (l - l)), l)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
