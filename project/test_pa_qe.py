def simple_one(n):
    return any((i + i < 22 for i in range(n + n)))


def simple_two(n):
    return not any((i + i >= 22 for i in range(n + n)))


def nested(n):
    return all((any((i + i < 22 for i in range(n + j))) for j in range(n + n)))


def disjunctive_normal_form(n):
    return (
        any((i > 0 and i < n for i in range(n + n)))
        or any((i + i < 34 and i < n for i in range(n + n)))
    ) or (
        any((i > 0 and i + i > n for i in range(n + n)))
        or any((i + i < 34 and i + i > n for i in range(n + n)))
    )


def negation(n):
    return any((i + i >= 22 and i <= 3 for i in range(n + n)))


def inequality(n):
    return (
        any((i + i < 22 for i in range(n + n)))
        or any((i + i > 22 for i in range(n + n)))
    ) or (any((i < 3 for i in range(n + n))) or any((i > 3 for i in range(n + n))))


def main():
    pass


if __name__ == "__main__":
    main()
