"""
Just a basic class for Dash Plots
"""
import plotly.graph_objs as go


class DashPlot(object):

    def __init__(self, graph_height=None, graph_width=None):
        self.graph_height = graph_height
        self.graph_width = graph_width
        self.margin = {'l': 60, 'b': 40, 't': 10, 'r': 60}

    def get_plot(self, *args, **kwargs):
        plot = self.get_plot_data(*args, **kwargs)
        plot['layout'] = go.Layout(
            height=self.graph_height if self.graph_height is not None else 450,
            width=self.graph_width if self.graph_width is not None else 700,
            # margin=self.margin
        )

        return plot

    def get_plot_data(self, new_data):
        raise NotImplementedError('You must implement the get_plot_data function')
