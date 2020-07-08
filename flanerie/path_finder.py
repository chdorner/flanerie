import math
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
                way_out, distance = self._find_way_out_of_dead_end(current_node, path)

                path.extend(way_out)
                total_distance += distance
                current_node = way_out[-1]
            else:
                edges = self._calculate_edges(current_node, destinations)
                selected_edge = max(edges, key=lambda x: x['weight'])

                next_node = selected_edge['dest']
                total_distance += selected_edge['length']

                path.append(next_node)
                current_node = next_node

        return path, total_distance

    def _find_way_out_of_dead_end(self, current_node, traversed_path):
        all_paths = nx.single_source_shortest_path(self._graph, current_node)
        not_visited = {k: v for k, v in all_paths.items() if k not in traversed_path}
        not_visited_nodes = sorted(not_visited.keys(), key=lambda x: len(not_visited[x]))

        closest_one_percent = not_visited_nodes[0:math.ceil(len(not_visited_nodes)*0.01)]
        closest = random.choice(closest_one_percent)

        path = all_paths[closest]
        distance = 0
        for idx, node in enumerate(path):
            # Check if there's still a next node.
            if (idx + 1) <= len(path) - 1:
                next_node = path[idx + 1]
                distance += self._graph[node][next_node][0]['length']

        return path[1:], distance

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
