from pathlib import Path

import matplotlib.pyplot as plt
import osmnx as ox

class Plotter(object):
    FIGSIZE = (15,15)
    COLOR_BACKGROUND = '#10627a'
    COLOR_FOOTPRINT = '#083440'

    def __init__(self, walk_id, render_dir):
        self._walk_id = walk_id

        self._render_dir = Path(render_dir).joinpath(walk_id)
        self._ensure_render_dir_exists()

    def plot_map(self, graph, footprint=None):
        _, ax = ox.plot_figure_ground(G=graph, bgcolor=self.COLOR_BACKGROUND, default_width=2,
                                        figsize=self.FIGSIZE, show=False, close=False)

        footprint.plot(ax=ax, color=self.COLOR_FOOTPRINT, alpha=0.75)

    def close(self):
        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.png'))
        plt.savefig(self._render_dir.joinpath(f'{self._walk_id}.svg'))
        plt.close()

        return self._render_dir

    def _ensure_render_dir_exists(self):
        self._render_dir.mkdir(parents=True, exist_ok=True)
