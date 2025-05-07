import sys

def f(n):
    return 3 * n - max(1000000, 2 * n + -1) > 1 or max(1000000, 2 * n + -1) % 1 < 3 * n % 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))