import sys

def f(m, n):
    return not (0 == -29 + -42 * m and (min(-64, -64) - max(72, -22 + n, 72) > 2 or 0 < min(-64, -64) % 2 < max(72, -22 + n, 72) % 2) or (-64 - max(72, 2 * n, -22 + n) > 2 or 0 < -64 % 2 < max(72, 2 * n, -22 + n) % 2))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))