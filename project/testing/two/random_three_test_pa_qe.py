import sys

def f(n, m):
    return not (0 > -1 * m + -8 and min(-6, -6) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))