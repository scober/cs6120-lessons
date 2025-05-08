import sys

def f(n):
    return not ((0 < 1 + -1 * n and 0 < 1 + -1 * n and (0 == n + -1) and (min(n, n) - max(-1, -1) > 1) or (0 > 1 + -1 * n and 0 < 1 + -1 * n and (0 == n + -1) and (min(n, n) - max(-1, -1) > 1))) or (0 < 1 + -1 * n and 0 > 1 + -1 * n and (0 == n + -1) and (min(n, n) - max(-1, -1) > 1) or (0 > 1 + -1 * n and 0 > 1 + -1 * n and (0 == n + -1) and (min(n, n) - max(-1, -1) > 1))))
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))