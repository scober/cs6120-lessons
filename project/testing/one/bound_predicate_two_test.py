import sys


def f(n):
    return all(i <= n for i in range(0, -1 * (n - 1)))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
