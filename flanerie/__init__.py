from pathlib import Path
import random
import string

import mong
import osmnx as ox

from .fetcher import NetworkFetcher
from .name_generator import NameGenerator
from .path_finder import WeightedRandomPathFinder
from .rendering import GPXRenderer, Plotter

CACHE_DIR = '.cache'
RENDER_DIR = 'rendered'

ox.config(use_cache=True,
          cache_folder=Path(CACHE_DIR).joinpath('osmnx'),
          log_console=False,
          useful_tags_way=ox.settings.useful_tags_way + ['railway'])

def generate(center, bbox_distance, min_walk_distance, random_start):
    walk_name, walk_slug = _random_name_and_slug()
    type_ = 'walk'

    fetcher = NetworkFetcher(type_, center, bbox_distance, CACHE_DIR)
    graph = fetcher.graph()

    start_node = None
    if not random_start:
        start_node = fetcher.center_node()
    path, _ = WeightedRandomPathFinder(graph, min_walk_distance, start_node).find()

    footprint = fetcher.footprint()
    railway_graph = fetcher.railway_graph()

    gpx_renderer = GPXRenderer(walk_name, walk_slug, RENDER_DIR)
    gpx_renderer.render_route(graph, path)

    plotter = Plotter(walk_slug, RENDER_DIR)
    plotter.plot_map(center, bbox_distance, type_, footprint, additional_graphs=[railway_graph])
    plotter.plot_route(graph, path)
    render_path = plotter.close()

    print(f'Rendered assets to {render_path}')

def _random_name_and_slug():
    name = NameGenerator.generate()
    slug = NameGenerator.slugify(name)

    return f'Walk - {name}', f'walk-{slug}'
