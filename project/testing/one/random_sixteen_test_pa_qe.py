import sys

def f(n):
    return n < n and -19 * n - (n + -1) > 1 or (n > n and -19 * n - (n + -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))