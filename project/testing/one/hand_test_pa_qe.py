import sys

def f(n):
    return not (min(-4 * n + 1, 2 * n) + 2 > 2 or min(-4 * n + 1, 2 * n) % 2 < -2 % 2)
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))