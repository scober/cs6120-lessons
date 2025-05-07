import sys

def f(n):
    return 3 * n - max(n, -1 + 2 * n) > 1 or max(n, -1 + 2 * n) % 1 < 3 * n % 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))