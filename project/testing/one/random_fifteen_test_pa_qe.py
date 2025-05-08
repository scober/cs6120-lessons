import sys

def f(n):
    return 60000 - max(n + 24, -2400) > 2400 or max(n + 24, -2400) % 2400 < 60000 % 2400
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))