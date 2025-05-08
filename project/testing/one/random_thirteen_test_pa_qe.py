import sys

def f(n):
    return 2 * n + -77 - max(-1 * (-1 * n), n + -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))