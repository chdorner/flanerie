import random

import networkx as nx

class WeightedRandomPathFinder(object):
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
            successors = list(self._graph.successors(current_node))
            destinations = [n for n in successors if n not in path]

            # Check if we found a dead-end, if so allow to backtrack.
            if not destinations:
                destinations = successors

            edges = self._calculate_edges(current_node, destinations)
            selected_edge = max(edges, key=lambda x: x['weight'])

            next_node = selected_edge['dest']
            total_distance += selected_edge['length']

            path.append(next_node)
            current_node = next_node

        return path, total_distance

    def _calculate_edges(self, origin, destinations):
        edges = [{'origin': origin,
                  'dest': destination,
                  'edge': self._graph[origin][destination][0],
                  'length': self._graph[origin][destination][0]['length']}
                 for destination in destinations]

        max_length = max([e['length'] for e in edges])
        for edge in edges:
            edge['weight'] = self._calculate_edge_weight(edge, max_length)

        return edges

    def _calculate_edge_weight(self, edge, max_length):
        # Normalized length weight, falls between 0.5 and 1.0
        normalized_length = ((float(edge['length']) / max_length) / 2) + 0.5
        # Randomize weight
        randomizer = random.choice(range(66, 100)) / 100

        weight = normalized_length * randomizer

        return weight
