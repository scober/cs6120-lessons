import sys

def f(m, n):
    return not min(n + 5, -1 * (-1 + 42 * m)) - (-1 + -11 * m) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))