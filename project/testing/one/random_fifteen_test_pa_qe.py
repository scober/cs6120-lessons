import sys

def f(n):
    return min(26 + n, 60000) + 2400 > 2400 or 0 < min(26 + n, 60000) % 2400 < -2400 % 2400
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))