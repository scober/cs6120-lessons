import sys

def f(l, m, n):
    return not ((0 < 12 + m and 0 > -25 + -1 * m and (min(l, l) - max(-1, -1) > 1) or (0 == -1 * l + m and 0 > -25 + -1 * m and (min(l, l) - max(-1, -1) > 1))) or (0 < 12 + m and 0 < 1 + n + -4047 * m and (min(l, l) - max(-1, -1) > 1) or (0 == -1 * l + m and 0 < 1 + n + -4047 * m and (min(l, l) - max(-1, -1) > 1))))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))