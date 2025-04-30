# def single_any(n):
#    return any(n % i == 0 for i in range(n))
#
#
# def single_all(n):
#    return all(n % i == 0 for i in range(n))
#
#
# def nested_all_all(n):
#    return all(all(j % i == 0 for j in range(n)) for i in range(n))
#
#
# def nested_any_any(n):
#    return any(any(j % i == 0 for j in range(n)) for i in range(n))
#
#
# def nested_any_all(n):
#    return any(all(j % i == 0 for j in range(n)) for i in range(n))
#
#
# def nested_all_any(n):
#    return all(any(j % i == 0 for j in range(n)) for i in range(n))
#
#
# def non_eliminatable(n):
#    return any(n * n % i == 0 for i in range(n))
#
#
# def disjunction_one(n):
#    return any(n % i == 0 or n % i == 1 or n % i == 2 for i in range(n + n))
#
#
# def disjunctive_normal_form(n):
#    return any(
#        (n % i == 0 or n + n % i == 0) and (n % i == 1 or n + n % i == 1)
#        for i in range(n + n)
#    )


def negated_disjunctive_normal_form(n):
    return any(
        not ((n % i == 0 or n + n % i == 0) and (n % i == 1 or n + n % i == 1))
        for i in range(n + n)
    )


def main():
    pass


if __name__ == "__main__":
    main()
