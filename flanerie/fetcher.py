from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import os

import osmnx as ox
import pandas

class NetworkFetcher(object):
    VALID_NETWORK_TYPES = ['walk', 'drive']
    CACHE_TTL = timedelta(weeks=1)

    def __init__(self, type_, center, distance, cache_dir):
        """
        Initialize graph fetcher with cetner point and distance of bbox from that point.

        Args:
            type_ (str): The type of graph to fetch (valid values are `walk`, `drive`)
            center (float, float): The center point of the map.
            distance (int): Bounding box distance from center to edges.
            cache_dir (str): Path to directory to use for caching graphs.

        Returns:
            GraphFetcher instance
        """
        self._type = type_
        self._center = center
        self._distance = distance

        raw_cache_key = f'{center[0]},{center[1]};{distance};{type_}'
        cache_key = hashlib.sha256(raw_cache_key.encode('utf-8')).hexdigest()
        self._cache_dir = Path(cache_dir)

        self._graph_cache_path = self._cache_dir.joinpath('graphs').joinpath(f'{cache_key}.graphml')
        self._footprint_cache_path = self._cache_dir.joinpath('gdfs').joinpath(f'{cache_key}.pkl')

    def graph(self):
        self._graph = self._fetch_from_cache('graph', self._graph_cache_path)
        if self._graph is None:
            self._graph = self._fetch_from_remote('graph', self._graph_cache_path)
        return self._graph

    def footprint(self):
        self._footprint = self._fetch_from_cache('footprint', self._footprint_cache_path)
        if self._footprint is None:
            self._footprint = self._fetch_from_remote('footprint', self._footprint_cache_path)
        return self._footprint

    def center_node(self):
        if self._graph is None:
            self.graph()
        return ox.get_nearest_node(self._graph, self._center)

    def nearest_node(self, point):
        return ox.get_nearest_node(self._graph, point)

    def _fetch_from_cache(self, type_, cache_path):
        if not cache_path.exists():
            return None

        mod_time = cache_path.stat().st_mtime
        now = datetime.now().timestamp()
        if (mod_time + self.CACHE_TTL.total_seconds()) < now:
            os.remove(cache_path)
            return None

        if type_ == 'graph':
            return ox.load_graphml(cache_path)
        elif type_ == 'footprint':
            return pandas.read_pickle(cache_path)

    def _fetch_from_remote(self, type_, cache_path):
        if type_ == 'graph':
            graph = ox.graph_from_point(self._center, self._distance, network_type=self._type)
            self._store_graph_cache(graph, cache_path)
            return graph
        elif type_ == 'footprint':
            gdf = ox.footprints_from_point(self._center, self._distance)
            self._store_footprint_cache(gdf, cache_path)
            return gdf

    def _store_graph_cache(self, graph, cache_path):
        self._ensure_dir_exists(cache_path.parent)
        ox.save_graphml(graph, cache_path)

    def _store_footprint_cache(self, gdf, cache_path):
        self._ensure_dir_exists(cache_path.parent)
        gdf.to_pickle(cache_path)

    def _ensure_dir_exists(self, path):
        path.mkdir(parents=True, exist_ok=True)
