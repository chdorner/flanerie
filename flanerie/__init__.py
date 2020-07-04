import osmnx as ox

from .graph_fetcher import GraphFetcher

CACHE_DIR = '.cache'

ox.config(use_cache=False, log_console=False)

def generate(start, bbox_distance, min_walk_distance):
    fetcher = GraphFetcher(start, bbox_distance, CACHE_DIR)
    fetcher.get()
