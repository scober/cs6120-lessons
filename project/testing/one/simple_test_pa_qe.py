import sys

def f(n):
    return 3 * n - max(-1 + 2 * n, n) > 1 or max(-1 + 2 * n, n) % 1 < 3 * n % 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))