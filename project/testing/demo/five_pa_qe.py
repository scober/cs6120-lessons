import sys

def f(z):
    return z - max(-1, 2500) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))