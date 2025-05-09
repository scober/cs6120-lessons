import sys

def f(z):
    return z - max(0, -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))