import sys

def f(n):
    return not (n == 37 and n + 1 > 1 or min(n, -32 * n) + 1 > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))