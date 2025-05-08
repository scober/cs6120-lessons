import sys

def f(n):
    return n < n and n + 28 > 1 or (-48 < n and 43 == 25 * n - 1050 and (n + 28 > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))