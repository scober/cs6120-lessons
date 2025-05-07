import sys

def f(n, m):
    return all((-5 >= -13 for i in range(m, 17)))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))