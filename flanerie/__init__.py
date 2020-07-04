import osmnx as ox

from .fetcher import GraphFetcher

CACHE_DIR = '.cache'

ox.config(use_cache=False, log_console=False)

def generate(start, bbox_distance, min_walk_distance):
    fetcher = GraphFetcher('walk', start, bbox_distance, CACHE_DIR)
    graph = fetcher.get()
    start_node = fetcher.start_node()
