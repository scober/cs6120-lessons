def simple_one(n):
    return min(2 * (2 * n), 22) - -2 > 2 or -2 % 2 < min(2 * (2 * n), 22) % 2


def simple_two(n):
    return not (2 * (2 * n) - max(-2, 21) > 2 or max(-2, 21) % 2 < 2 * (2 * n) % 2)


def nested(n):
    return all(
        (
            min(22, 2 * (n + j)) - -2 > 2 or -2 % 2 < min(22, 2 * (n + j)) % 2
            for j in range(n + n)
        )
    )


def disjunctive_normal_form(n):
    return (
        (min(2 * n, n) - max(-1, 0) > 1 or max(-1, 0) % 1 < min(2 * n, n) % 1)
        or (
            min(2 * (2 * n), 2 * n, 34) - -2 > 2
            or -2 % 2 < min(2 * (2 * n), 2 * n, 34) % 2
        )
    ) or (
        (2 * (2 * n) - max(n, -2, 0) > 2 or max(n, -2, 0) % 2 < 2 * (2 * n) % 2)
        or (
            min(2 * (2 * n), 34) - max(n, -2) > 2
            or max(n, -2) % 2 < min(2 * (2 * n), 34) % 2
        )
    )


def negation(n):
    return 2 * (2 * n) - max(21, 4, -2) > 2 or max(21, 4, -2) % 2 < 2 * (2 * n) % 2


def equality(n):
    return 22 < 2 * (2 * n)


def inequality(n):
    return (
        (min(22, 2 * (2 * n)) - -2 > 2 or -2 % 2 < min(22, 2 * (2 * n)) % 2)
        or (2 * (2 * n) - max(22, -2) > 2 or max(22, -2) % 2 < 2 * (2 * n) % 2)
    ) or (
        (min(3, 2 * n) - -1 > 1 or -1 % 1 < min(3, 2 * n) % 1)
        or (2 * n - max(-1, 3) > 1 or max(-1, 3) % 1 < 2 * n % 1)
    )


def vars_on_both_sides(n):
    return (
        min(3 * (2 * n), 12) - max(2 * n, -3) > 3
        or max(2 * n, -3) % 3 < min(3 * (2 * n), 12) % 3
    )


def main():
    pass


if __name__ == "__main__":
    main()
