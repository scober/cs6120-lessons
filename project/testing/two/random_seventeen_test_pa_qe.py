import sys

def f(m, n):
    return not min(-1 * (-1 + 42 * m), 5 + n) - (-1 + -11 * m) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))