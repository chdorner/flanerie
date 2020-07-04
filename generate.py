import click

@click.command()
@click.option('--start', nargs=2, type=click.Tuple([float, float]), help='Starting point as GPS coordinate, first latitude, then longitude.')
@click.option('--min-distance', type=int, help='Minimum distance of generated path.')
def generate(start, min_distance):
    """
    Generate random amble walks based off of a starting point and a minimum target distance.

    e.g. python3 generate.py --start 52.46794 13.31386 --min-distance 5000
    """
    pass

if __name__ == '__main__':
    generate()
