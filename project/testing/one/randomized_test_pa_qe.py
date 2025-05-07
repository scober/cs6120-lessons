import sys

def f(n):
    return any((-154 * (193 * n) - n == 34 for i in range(-94 * (-240 - -243))))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))