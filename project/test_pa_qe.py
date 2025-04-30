def negated_disjunctive_normal_form(n):
    return any(
        (
            not n % i == 0
            and (not n + n % i == 0)
            or (not n % i == 1 and (not n + n % i == 1))
            for i in range(n + n)
        )
    )


def main():
    pass


if __name__ == "__main__":
    main()
