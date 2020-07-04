from pathlib import Path
import random
import string

import mong
import osmnx as ox

from .fetcher import NetworkFetcher
from .path_finder import RandomPathFinder
from .rendering import Plotter

CACHE_DIR = '.cache'
RENDER_DIR = 'rendered'

ox.config(use_cache=True, cache_folder=Path(CACHE_DIR).joinpath('osmnx'), log_console=False)

def generate(start_point, bbox_distance, min_walk_distance):
    walk_id = _random_walk_id()
    type_ = 'walk'

    fetcher = NetworkFetcher(type_, start_point, bbox_distance, CACHE_DIR)
    graph = fetcher.graph()
    start_node = fetcher.start_node()
    path, _ = RandomPathFinder(graph, min_walk_distance, start_node).find()

    footprint = fetcher.footprint()

    plotter = Plotter(walk_id, RENDER_DIR)
    plotter.plot_map(start_point, bbox_distance, type_, footprint)
    plotter.plot_route(graph, path)
    render_path = plotter.close()
    print(f'Rendered assets to {render_path}')

def _random_walk_id():
    random_name = mong.get_random_name().replace('_', '-')
    return f'Walk-{random_name}'
