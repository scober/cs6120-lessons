import sys

def f(n):
    return not (0 < -1 * n + 23 and min(-34, -34) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))