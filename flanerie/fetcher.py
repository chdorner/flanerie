from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import os

import osmnx as ox

class GraphFetcher(object):
    VALID_NETWORK_TYPES = ['walk', 'drive']
    CACHE_PREFIX = 'graphs'
    CACHE_TTL = timedelta(weeks=1)

    def __init__(self, type_, start_point, distance, cache_dir):
        """
        Initialize graph fetcher with starting point and distance of bbox from starting point.

        Args:
            type_ (str): The type of graph to fetch (valid values are `walk`, `drive`)
            start_point (float, float): The center point from where to start the walk.
            distance (int): Bounding box distance from center to edges.
            cache_dir (str): Path to directory to use for caching graphs.

        Returns:
            GraphFetcher instance
        """
        self._type = type_
        self._start_point = start_point
        self._distance = distance

        raw_cache_key = f'{start_point[0]},{start_point[1]};{distance};{type_}'
        cache_key = hashlib.sha256(raw_cache_key.encode('utf-8')).hexdigest()
        self._cache_dir = Path(cache_dir).joinpath(self.CACHE_PREFIX)

        self._cache_path = self._cache_dir.joinpath(f'{cache_key}.graphml')
        self._ensure_cache_dir_exists()

    def get(self):
        self._graph = self._fetch_from_cache()
        if self._graph is None:
            self._graph = self._fetch_from_remote()
        return self._graph

    def start_node(self):
        if self._graph is None:
            self.get()
        return ox.get_nearest_node(self._graph, self._start_point)

    def _fetch_from_cache(self):
        if not self._cache_path.exists():
            return None

        mod_time = self._cache_path.stat().st_mtime
        now = datetime.now().timestamp()
        if (mod_time + self.CACHE_TTL.total_seconds()) < now:
            os.remove(self._cache_path)
            return None

        return ox.load_graphml(self._cache_path)

    def _fetch_from_remote(self):
        graph = ox.graph_from_point(self._start_point, self._distance, network_type=self._type)
        self._store_cache (graph)
        return graph

    def _store_cache(self, graph):
        ox.save_graphml(graph, self._cache_path)

    def _ensure_cache_dir_exists(self):
        self._cache_dir.mkdir(parents=True, exist_ok=True)
