import sys

def f(n):
    return all((38 == n for i in range(-33, -46)))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))