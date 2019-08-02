import unittest
from Basic import BasicPlot
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


class BasicApp(object):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    name = None

    def __init__(self, x_label, y_label, name, x_scale='linear', y_scale='linear'):

        self.plot = BasicPlot(x_label=x_label, y_label=y_label, x_scale=x_scale, y_scale=y_scale)

        self.name = name

        self.app.layout = html.Div(
            [dcc.Graph(self.name),
             html.Div(
                 style={'display': 'none'},
                 children=
                 [dcc.Input(name='blank',
                           id='blank')]
             )
             ]

        )

        # self.plot.add_data(0.2, 0.5, 'nothing', 'something')

        @self.app.callback(Output(name, 'figure'),
                      [Input('blank', 'value')])
        def update_graph(x_value):
            return self.plot.get_plot()

    def add_data(self, x, y, text, name):
        self.plot.add_data(x, y, text, name)


if __name__ == '__main__':
    test = BasicApp('X', 'Y', 'Testing')
    test.add_data(0.1, 0.1, 'nothing', 'name')
    test.app.run_server(debug=True)
