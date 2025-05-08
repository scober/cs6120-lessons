import sys

def f(n):
    return not (2 * n - max(-1 * (n + 1), -2) > 2 or 0 < 2 * n % 2 < max(-1 * (n + 1), -2) % 2)
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))