import sys


def f(z):
    return any(x > 0 for x in range(z))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
