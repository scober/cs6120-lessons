import sys

def f(n):
    return not (min(1 + -4 * n, 2 * n) + 2 > 2 or 0 < min(1 + -4 * n, 2 * n) % 2 < -2 % 2)
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))