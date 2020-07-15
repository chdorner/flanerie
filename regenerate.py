import click

import flanerie

@click.command()
@click.option('--gpx', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True), required=True, help='GPX file to parse and regenerate the map.')
@click.option('--bbox-distance', default=1500, type=int, help='Distance of bounding box in meters from starting point.')
def regenerate(gpx, bbox_distance):
    flanerie.regenerate(gpx, bbox_distance)


if __name__ == '__main__':
    regenerate()
