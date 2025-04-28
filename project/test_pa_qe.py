def single_any(n):
    return any((n % i == 0 for i in range(n)))

def single_all(n):
    return not any(not (n % i == 0 for i in range(n)))

def nested_all_all(n):
    return not any(not (not any(not (j % i == 0 for j in range(n))) for i in range(n)))

def nested_any_any(n):
    return any((any((j % i == 0 for j in range(n))) for i in range(n)))

def nested_any_all(n):
    return any((not any(not (j % i == 0 for j in range(n))) for i in range(n)))

def nested_all_any(n):
    return not any(not (any((j % i == 0 for j in range(n))) for i in range(n)))

def non_eliminatable(n):
    return any((n * n % i == 0 for i in range(n)))

def main():
    print(single_any(6))
    print(single_all(6))
    print(nested_all_all(6))
    print(nested_any_any(6))
    print(nested_any_all(6))
    print(nested_all_any(6))
    print(non_eliminatable(6))
if __name__ == '__main__':
    main()