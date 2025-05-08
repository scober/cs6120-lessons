import sys

def f(n):
    return not ((min(34 * n, 20) + 1 > 1 or 34 * n - max(20, -1) > 1) or 34 * n + 1 > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))