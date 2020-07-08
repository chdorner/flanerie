import random

import networkx as nx

class WeightedRandomPathFinder(object):
    def __init__(self, graph, min_path_distance, start_node=None):
        self._graph = graph
        self._min_path_distance = min_path_distance

        self._nodes = list(graph.nodes())

        if start_node is None:
            start_node = random.choice(self._nodes)
        self._start_node = start_node

    def find(self):
        total_distance = 0
        current_node = self._start_node
        path = [current_node]

        while total_distance < self._min_path_distance:
            successors = list(self._graph.successors(current_node))
            destinations = [n for n in successors if n not in path]

            # Check if we found a dead-end, if so allow to backtrack.
            if not destinations:
                # If more than one successor, prevent the path from going back where
                # it came from.
                if len(successors) > 1:
                    destinations = [s for s in successors if s != path[-1]]
                else:
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
        # Edge type weight
        edge_type = self._edge_type_weight(edge['edge'])
        # Randomize weight
        randomizer = random.choice(range(66, 100)) / 100

        weight = normalized_length * edge_type * randomizer
        return weight

    def _edge_type_weight(self, edge):
        PREFERRED, ACCEPTABLE, DISCOURAGED, AVOID = 1.0, 0.75, 0.25, 0
        types = {
            # preferred
            'path': PREFERRED,
            'track': PREFERRED,
            'corridor': PREFERRED,
            'footway': PREFERRED,
            'pedestrian': PREFERRED,
            'steps': PREFERRED,
            'living_street': PREFERRED,
            'service': PREFERRED,
            'residential': PREFERRED,
            # acceptable
            'tertiary_link': ACCEPTABLE,
            'tertiary': ACCEPTABLE,
            'secondary_link': ACCEPTABLE,
            'secondary': ACCEPTABLE,
            # discouraged
            'primary_link': DISCOURAGED,
            'primary': DISCOURAGED,
            # avoid
            'trunk': AVOID,
            'trunk_link': AVOID,
            'motorway': AVOID,
            'unclassified': AVOID,
        }

        type_ = edge['highway']
        if isinstance(type_, list):
            type_ = type_[0]

        weight = types.get(type_)
        if weight is None:
            print(f'Found unclassified edge type "{type_}"')
            return AVOID

        return weight
