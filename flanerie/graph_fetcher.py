from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import os

import osmnx as ox

class GraphFetcher(object):
    NETWORK_TYPE = 'walk'
    CACHE_PREFIX = 'graphs'
    CACHE_TTL = timedelta(weeks=1)

    def __init__(self, start_point, distance, cache_dir):
        """
        Initialize graph fetcher with starting point and distance of bbox from starting point.

        Args:
            start_point (float, float): The center point from where to start the walk.
            distance (int): Bounding box distance from center to edges.

        Returns:
            GraphFetcher instance
        """
        self._start_point = start_point
        self._distance = distance

        raw_cache_key = f'{start_point[0]},{start_point[1]};{distance}'
        cache_key = hashlib.sha256(raw_cache_key.encode('utf-8')).hexdigest()
        self._cache_dir = Path(cache_dir).joinpath(self.CACHE_PREFIX)
        self._cache_path = self._cache_dir.joinpath(f'{cache_key}.graphml')
        self._ensure_cache_dir_exists()

    def get(self):
        graph = self._fetch_from_cache()
        if graph is None:
            graph = self._fetch_from_remote()
        return graph

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
        graph = ox.graph_from_point(self._start_point, self._distance, network_type=self.NETWORK_TYPE)
        self._store_graph_cache(graph)
        return graph

    def _store_graph_cache(self, graph):
        ox.save_graphml(graph, self._cache_path)

    def _ensure_cache_dir_exists(self):
        self._cache_dir.mkdir(parents=True, exist_ok=True)
