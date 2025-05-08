import sys

def f(l, m, n):
    return not ((0 > -899 * l + -925 + -1 * n and 0 < -899 * l + -923 + -1 * n and (min(-1 * (-1 * n), -7 + -1 * n, -7 + -1 * n) - max(-1, -1) > 1) or (0 < 48 + m and min(-1 * (-1 * n), -7 + -1 * n, -7 + -1 * n) - max(-1, -1) > 1)) or (0 > m + -1 * n and min(-7 + -1 * n, -7 + -1 * n, -1 * (-1 * n)) - max(-1, -1) > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))