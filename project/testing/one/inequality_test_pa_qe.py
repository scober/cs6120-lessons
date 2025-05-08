import sys

def f(n):
    return ((min(2 * (2 * n), 22) + 2 > 2 or -2 % 2 < min(2 * (2 * n), 22) % 2) or (2 * (2 * n) - max(-2, 22) > 2 or max(-2, 22) % 2 < 2 * (2 * n) % 2)) or (min(2 * n, 3) + 1 > 1 or 2 * n - max(-1, 3) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))