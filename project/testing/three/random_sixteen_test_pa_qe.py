import sys

def f(l, m, n):
    return 0 == m + -1 * n and min(m, m) - max(-1, -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))