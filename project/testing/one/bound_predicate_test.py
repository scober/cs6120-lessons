import sys


def f(n):
    return all(not i <= -27 * n for i in range(-27, n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
