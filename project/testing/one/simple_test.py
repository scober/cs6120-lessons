import sys


def f(n):
    return any(2 * i > n + i for i in range(2 * n, 3 * n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
