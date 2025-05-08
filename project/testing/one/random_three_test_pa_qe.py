import sys

def f(n):
    return 0 < 10 * n and min(n, n) - max(-1, -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))