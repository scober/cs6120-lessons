import sys

def f(n):
    return -77 + 2 * n - max(-1 * (-1 * n), -1 + n) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))