import sys

def f(m, n):
    return not 50 + -1 * n - max(47 + -1 * n, -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))