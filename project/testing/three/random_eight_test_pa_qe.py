import sys

def f(l, m, n):
    return not (0 < 2 * n + -43 and min(m + -33, m + -33) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))