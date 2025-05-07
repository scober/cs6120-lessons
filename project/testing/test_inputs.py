import itertools

import click


@click.group
def cli():
    pass


@cli.command
def one():
    for n in range(-1000, 1000):
        print(n)


@cli.command
def two():
    for m, n in itertools.product(range(-100, 100), range(-100, 100)):
        print(m, n)


@cli.command
def three():
    for l, m, n in itertools.product(range(-10, 10), range(-10, 10), range(-10, 10)):
        print(l, m, n)


if __name__ == "__main__":
    cli()
