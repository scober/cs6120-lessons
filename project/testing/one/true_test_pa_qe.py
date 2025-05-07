import sys

def f(n):
    return min(3 * n, 1000000) - (-1 + 2 * n) > 1 or (-1 + 2 * n) % 1 < min(3 * n, 1000000) % 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))