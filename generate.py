import click

import flanerie

@click.command()
@click.option('--center', type=str, required=True, help='Starting point as GPS coordinate in the format of "{latitude},{longitude}".')
@click.option('--bbox-distance', default=1500, type=int, help='Distance of bounding box in meters from starting point.')
@click.option('--min-walk-distance', type=int, required=True, help='Minimum distance of generated walk in meters.')
@click.option('--random-start', is_flag=True, default=False, help='Select random location to start walk, if false then it uses center as start.')
def generate(center, bbox_distance, min_walk_distance, random_start):
    """
    Generate random amble walks based off of a starting point and a minimum target distance.

    e.g. python3 generate.py --center 52.46794,13.31386 --min-walk-distance 5000
    """
    center_point = [float(v) for v in center.split(',')]
    flanerie.generate(center_point, bbox_distance, min_walk_distance, random_start)


if __name__ == '__main__':
    generate()
