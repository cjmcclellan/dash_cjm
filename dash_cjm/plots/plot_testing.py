"""
Testing for dash_cjm.plots
"""
import unittest
import plotly.graph_objs as go
from dash_cjm.plots.Basic import BasicPlot
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


class TestBasicPlot(unittest.TestCase):

    def test_plotting(self):
        # create a basic plot, request the layout and data, then create a plotly figure
        test = BasicPlot(x_label='Test', y_label='Test Y', graph_height=400, graph_width=400, marker_size=6.0,
                         layout={'plot_bgcolor': '#fff'}, figure_border=1, x_min=0, x_max=2.0, y_min=0, y_max=2.0)

        # now add some data
        test.add_data(x_data=[0.1, 0.2], y_data=[0.5, 0.6], error_x={'type': 'data', 'array': [0.05, 0.05], 'visible': True},
                      mode='markers+lines', name='testing', text='testing_text')

        test_plot = test.get_plot(as_figure=True)

        # fig = go.Figure(
        #     data=[go.Bar(y=[2, 1, 3])],
        #     layout_title_text="A Figure Displayed with the 'png' Renderer"
        # )
        # fig.show(renderer="png")

        # fig = go.Figure(data=test_plot['data'], layout=test_plot['layout'])

        test_plot.write_image('test.svg')

        # plot(fig)
        # fig.show(renderer='png')

        a = 5
