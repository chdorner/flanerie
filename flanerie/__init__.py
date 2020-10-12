from pathlib import Path
import random
import string

import osmnx as ox

from .fetcher import NetworkFetcher
from .name_generator import NameGenerator
from .parsing import GPXParser
from .path_finder import WeightedRandomPathFinder
from .rendering import GPXRenderer, Plotter

CACHE_DIR = '.cache'
RENDER_DIR = 'rendered'

NETWORK_TYPE = 'walk'

ox.config(use_cache=True, cache_folder=Path(CACHE_DIR).joinpath('osmnx'), log_console=False)

def generate(center, bbox_distance, min_walk_distance, random_start):
    walk_name, walk_slug = _random_name_and_slug()

    fetcher = NetworkFetcher(NETWORK_TYPE, center, bbox_distance, CACHE_DIR)
    graph = fetcher.graph()

    start_node = None
    if not random_start:
        start_node = fetcher.center_node()
    route, _ = WeightedRandomPathFinder(graph, min_walk_distance, start_node).find()

    footprint = fetcher.footprint()

    gpx_renderer = GPXRenderer(walk_name, walk_slug, RENDER_DIR)
    gpx_renderer.render_route(graph, route)

    plotter = Plotter(walk_slug, RENDER_DIR)
    plotter.plot_map(center, bbox_distance, NETWORK_TYPE, footprint)
    plotter.plot_route(graph, route)
    render_path = plotter.close()

    print(f'Rendered assets to {render_path}')

def regenerate(gpx_input, bbox_distance):
    parser = GPXParser(gpx_input)

    walk_name = parser.name
    walk_slug = NameGenerator.slugify(walk_name)
    path = parser.path
    center = path[0]

    fetcher = NetworkFetcher(NETWORK_TYPE, center, bbox_distance, CACHE_DIR)
    graph = fetcher.graph()

    route = [fetcher.nearest_node(p) for p in path]

    import networkx as nx
    updated_route = [route[0]]
    for idx, n in enumerate(route):
        if n == route[-1]:
            break
        target = route[idx + 1]

        shortest_path = nx.shortest_path(graph, n, target)
        updated_route.extend(shortest_path[1:])

    gpx_renderer = GPXRenderer(walk_name, walk_slug, RENDER_DIR)
    gpx_renderer.render_route(graph, updated_route)

    footprint = fetcher.footprint()
    plotter = Plotter(walk_slug, RENDER_DIR)
    plotter.plot_map(center, bbox_distance, NETWORK_TYPE, footprint)
    plotter.plot_route(graph, updated_route)
    render_path = plotter.close()

    print(f'Rendered assets to {render_path}')


def _random_name_and_slug():
    name = NameGenerator.generate()
    slug = NameGenerator.slugify(name)

    return name, slug
