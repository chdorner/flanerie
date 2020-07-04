import random
import string

import osmnx as ox

from .fetcher import GraphFetcher
from .rendering import Plotter

CACHE_DIR = '.cache'
RENDER_DIR = 'out'

ox.config(use_cache=False, log_console=False)

def generate(start, bbox_distance, min_walk_distance):
    walk_id = _random_walk_id()

    fetcher = GraphFetcher('walk', start, bbox_distance, CACHE_DIR)
    graph = fetcher.get()
    start_node = fetcher.start_node()

    Plotter(graph, walk_id, RENDER_DIR).plot()

def _random_walk_id():
    random_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f'walk-{random_id}'
