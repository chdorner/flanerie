import random

import networkx as nx

class RandomPathFinder(object):
    def __init__(self, graph, min_path_distance, start_node):
        self._graph = graph
        self._min_path_distance = min_path_distance
        self._start_node = start_node

        self._nodes = list(graph.nodes())

    def find(self):
        total_distance = 0
        current_node = self._start_node
        path = [current_node]

        while total_distance < self._min_path_distance:
            segment, distance = self._find_segment(current_node)
            # Omit first node in segment as it's the last node on the previous segment.
            path.extend(segment[1:])

            current_node = segment[-1]
            total_distance += distance

        return path, total_distance

    def _find_segment(self, from_node):
        next_node = random.choice(self._nodes)
        paths = list(nx.all_shortest_paths(self._graph, from_node, next_node, weight='length'))

        segment = random.choice(paths)
        distance = nx.shortest_path_length(self._graph, from_node, next_node, weight='length')

        return segment, distance
