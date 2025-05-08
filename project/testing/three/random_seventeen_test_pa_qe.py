import sys

def f(l, m, n):
    return not (0 < 13 * m + 14 and min(42, 42) - max(-1, -1) > 1 or (0 > 13 * m + 14 and min(42, 42) - max(-1, -1) > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))