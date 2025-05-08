import sys

def f(m, n):
    return not (min(1 + 27 * n, 1380 + -46 * n) + 28 > 1 or (0 < -21 + -1 * n and min(-46 * n + 1380, 1380 + -46 * n) - max(-28, -28) > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))