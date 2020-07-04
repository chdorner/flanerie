import random
import string

import osmnx as ox

from .fetcher import NetworkFetcher
from .fetcher import GraphFetcher
from .rendering import Plotter

CACHE_DIR = '.cache'
RENDER_DIR = 'rendered'

ox.config(use_cache=False, log_console=False)

def generate(start, bbox_distance, min_walk_distance):
    walk_id = _random_walk_id()

    fetcher = NetworkFetcher('walk', start, bbox_distance, CACHE_DIR)
    graph = fetcher.graph()
    start_node = fetcher.start_node()

    footprint = fetcher.footprint()

    plotter = Plotter(walk_id, RENDER_DIR)
    plotter.plot_map(graph, footprint)
    render_path = plotter.close()
    print(f'Rendered assets to {render_path}')

def _random_walk_id():
    random_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f'walk-{random_id}'
