import click

import flanerie

@click.command()
@click.option('--start', nargs=2, type=float, required=True, help='Starting point as GPS coordinate, first latitude, then longitude.')
@click.option('--bbox-distance', default=5000, type=int, help='Distance of bounding box in meters from starting point.')
@click.option('--min-walk-distance', type=int, required=True, help='Minimum distance of generated walk in meters.')
def generate(start, bbox_distance, min_walk_distance):
    """
    Generate random amble walks based off of a starting point and a minimum target distance.

    e.g. python3 generate.py --start 52.46794 13.31386 --min-distance 5000
    """
    flanerie.generate(start, bbox_distance, min_walk_distance)


if __name__ == '__main__':
    generate()
