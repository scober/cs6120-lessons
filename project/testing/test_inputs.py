import itertools

import click


@click.group
def cli():
    pass


@cli.command
def demo():
    for n in range(5000):
        print(n)


@cli.command
def perf_one():
    for n in range(-10000, 10000):
        print(n)


@cli.command
def one():
    for n in range(-10, 10):
        print(n)


@cli.command
def two():
    for m, n in itertools.product(range(-10, 10), range(-10, 10)):
        print(m, n)


@cli.command
def three():
    for l, m, n in itertools.product(range(-10, 10), range(-10, 10), range(-10, 10)):
        print(l, m, n)


if __name__ == "__main__":
    cli()
