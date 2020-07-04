from pathlib import Path

import matplotlib.pyplot as plt
import osmnx as ox

class Plotter(object):
    FIGSIZE = (15,15)
    BGCOLOR = '#10627a'

    def __init__(self, graph, walk_id, render_dir):
        self._graph = graph
        self._walk_id = walk_id

        self._render_dir = Path(render_dir)
        self._ensure_render_dir_exists()

    def plot(self):
        fig, ax = ox.plot_figure_ground(G=self._graph, bgcolor=self.BGCOLOR, default_width=2,
                                        figsize=self.FIGSIZE, show=False, close=False)

        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.png'))
        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.svg'))
        plt.close()

    def _ensure_render_dir_exists(self):
        self._render_dir.mkdir(parents=True, exist_ok=True)
