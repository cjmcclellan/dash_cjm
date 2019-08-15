import unittest
from dash_cjm.plots.Basic import BasicPlot
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

        # app layout
        self.app_layout = html.Div(
            children=[
                dcc.Graph(self.name),
                html.Div(
                    style={'display': 'none'},
                    children=
                    [dcc.Input(name='blank',
                               id='blank')]
                )
            ]
        )

    def add_div(self, div, top=True, bottom=False):
        # assert not top or not bottom, 'You must choose to add to the top or the bottom'
        assert top or bottom, 'You must choose to add to the top or the bottom'
        assert isinstance(div, html.Div), 'The input must be of type Div'
        if top:
            self.app_layout.children = [div] + self.app_layout.children
        elif bottom:
            self.app_layout.children.append(div)

    def build_app(self):

        self.app.layout = self.app_layout

        @self.app.callback(Output(self.name, 'figure'),
                      [Input('blank', 'value')])
        def update_graph(x_value):
            return self.plot.get_plot()

    def add_data(self, x, y, text, name):
        self.plot.add_data(x, y, text, name)


if __name__ == '__main__':
    test = BasicApp('X', 'Y', 'Testing')
    test.add_data(0.1, 0.1, 'nothing', 'name')
    html.Div(

    )
    test.add_div('')
    test.build_app()
    test.app.run_server(debug=True)
