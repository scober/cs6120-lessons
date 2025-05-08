import sys

def f(n):
    return not (n == 37 and n + 1 > 1 or (32 * n - max(-1 * (-32 * n), -32) > 32 or 32 * n % 32 < max(-1 * (-32 * n), -32) % 32))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))