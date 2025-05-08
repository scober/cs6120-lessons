import sys

def f(n):
    return not (min(-1 * (40 * n + 42), -511 * (-1 * n), 511 * (n + -41)) - max(117019, -1 * (40 * n + 42), -511 * (-1 * n)) > 511 or 0 < min(-1 * (40 * n + 42), -511 * (-1 * n), 511 * (n + -41)) % 511 < max(117019, -1 * (40 * n + 42), -511 * (-1 * n)) % 511)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))