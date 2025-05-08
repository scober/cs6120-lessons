import sys

def f(n):
    return not (-8 * n - max(-1, 31) > 1 or min(-8 * n, 31) + 1 > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))