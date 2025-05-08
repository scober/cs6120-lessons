import sys

def f(n):
    return not (min(-511 * (-1 * n), 511 * (n + -41), -1 * (40 * n + 42)) - max(-1 * (40 * n + 42), -511 * (-1 * n), 117019) > 511 or min(-511 * (-1 * n), 511 * (n + -41), -1 * (40 * n + 42)) % 511 < max(-1 * (40 * n + 42), -511 * (-1 * n), 117019) % 511)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))