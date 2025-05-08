import sys

def f(m, n):
    return not (21 * m + 21 * m == -29 and (-64 - max(72, -22 + n) > 2 or -64 % 2 < max(72, -22 + n) % 2) or (-64 - max(72, -22 + n, 2 * n) > 2 or -64 % 2 < max(72, -22 + n, 2 * n) % 2))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))