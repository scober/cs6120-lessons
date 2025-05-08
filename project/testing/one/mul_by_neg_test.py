import sys


def f(n):
    return all(-2 * i > n for i in range(0, n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
