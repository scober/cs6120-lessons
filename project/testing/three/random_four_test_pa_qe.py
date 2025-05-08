import sys

def f(l, m, n):
    return not (0 == -14 * n + 450 * l + 297 + -29 * m and min(m, m) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))