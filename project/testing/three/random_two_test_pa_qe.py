import sys

def f(l, m, n):
    return 0 > -27 + m and min(-1 * m + n, -1 * m + n) - max(20, 20) > 1 or (0 > -1 * m and min(-1 * m + n, -1 * m + n) - max(20, 20) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))