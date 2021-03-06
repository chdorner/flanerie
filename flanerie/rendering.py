from pathlib import Path

from gpxpy import gpx as gpxpy
import matplotlib.pyplot as plt
import osmnx as ox

class Plotter(object):
    FIGSIZE = (15,15)
    COLOR_BACKGROUND = '#10627a'
    COLOR_FOOTPRINT = '#083440'
    COLOR_ROUTE = '#f30c2c'

    def __init__(self, walk_id, render_dir):
        self._walk_id = walk_id

        self._render_dir = Path(render_dir).joinpath(walk_id)
        _ensure_dir_exists(self._render_dir)

    def plot_map(self, start_point, distance, type_, footprint=None):
        _, self._ax = ox.plot_figure_ground(point=start_point,
                                dist=distance,
                                network_type=type_,
                                bgcolor=self.COLOR_BACKGROUND,
                                default_width=4,
                                figsize=self.FIGSIZE,
                                show=False,
                                close=False)

        if footprint is not None:
            footprint.plot(ax=self._ax, color=self.COLOR_FOOTPRINT, alpha=0.75)

    def plot_route(self, graph, route):
        if self._ax is None:
            raise Exception('Need to plot the map first before the route.')

        ox.plot_graph_route(graph, route, ax=self._ax, route_colors=self.COLOR_ROUTE,
                             alpha=1, orig_dest_size=250, route_linewidth=4,
                             show=False, close=False)

    def close(self):
        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.png'))
        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.svg'))
        plt.close()

        return self._render_dir


class GPXRenderer(object):
    def __init__(self, walk_name, walk_slug, render_dir):
        self._walk_name = walk_name
        self._walk_slug = walk_slug

        self._render_dir = Path(render_dir).joinpath(walk_slug)
        _ensure_dir_exists(self._render_dir)

    def render_route(self, graph, route):
        gpx = gpxpy.GPX()
        gpx.name = self._walk_name

        nodes = graph.nodes()
        track = gpxpy.GPXTrack()
        track.name = self._walk_name
        segment = gpxpy.GPXTrackSegment()
        track.segments.append(segment)

        for node_id in route:
            node = nodes[node_id]
            segment_point = gpxpy.GPXTrackPoint(latitude=node['y'], longitude=node['x'])
            segment.points.append(segment_point)

        gpx.tracks.append(track)

        with open(self._render_dir.joinpath(f'{self._walk_slug}.gpx'), 'w') as fp:
            fp.write(gpx.to_xml())


def _ensure_dir_exists(path):
    path.mkdir(parents=True, exist_ok=True)
