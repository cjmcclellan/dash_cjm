import unittest
from .Basic import BasicPlot
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash


class BasicApp(object):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    name = None

    def __init__(self, x_label, y_label, name, x_scale='linear', y_scale='linear', django=False, hidden_update=True,
                 graph_height=None, graph_width=None):

        self.graph_height = graph_height
        self.graph_width = graph_width

        self.init_plot(x_label=x_label, y_label=y_label, x_scale=x_scale, y_scale=y_scale)

        self.name = name

        if django:
            self.app = DjangoDash(name)
        else:
            self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)

        self.update_function = None

        # the callback options
        self.callback_inputs = []
        self.callback_states = []

        # app layout
        self.app_layout = html.Div(
            style={'margin': '0 auto'},
            children=[
                dcc.Graph(self.name),
                html.Div(
                    className='col-sm',
                    style={'display': 'none'} if hidden_update else {},
                    children=
                    [html.Button('Update',
                                 name='update_' + self.name,
                                 id='update_' + self.name,
                                 className='alert')]
                )
            ],
        )

    def add_div(self, div, top=True, bottom=False):
        # assert not top or not bottom, 'You must choose to add to the top or the bottom'
        assert top or bottom, 'You must choose to add to the top or the bottom'
        assert isinstance(div, html.Div), 'The input must be of type Div'
        if top:
            self.app_layout.children = [div] + self.app_layout.children
        elif bottom:
            self.app_layout.children.append(div)

    def init_plot(self, x_label, y_label, x_scale, y_scale):

        self.plot = BasicPlot(x_label=x_label, y_label=y_label, x_scale=x_scale, y_scale=y_scale,
                              graph_height=self.graph_height, graph_width=self.graph_width)

    def build_app(self):

        self.app.layout = self.app_layout

        self._update_graph_function()

        # @self.app.callback(Output(self.name, 'figure'),
        #               [Input('blank', 'value'), Input('update_' + self.name, 'n_clicks')])
        # def update_graph(x_value, update):
        #     if self.update_function is not None:
        #         new_data = self.update_function(update)
        #         # print(new_data)
        #         if new_data is not None:
        #             return self.plot.get_plot(new_data=new_data)
        #     else:
        #         return self.plot.get_plot()

    def _update_graph_function(self):

        @self.app.callback(Output(self.name, 'figure'),
                           [Input('update_' + self.name, 'n_clicks')] + self.callback_inputs, self.callback_states)
        def update_graph(update_n, *args):
            # create the kwargs
            callbacks = self.callback_inputs + self.callback_states
            kwargs = {callback.component_id: _input for _input, callback in zip(args, callbacks)}
            if self.update_function is not None:
                new_data = self.update_function(update_n, **kwargs)
                # print(new_data)
                if new_data is not None:
                    return self.plot.get_plot(new_data=new_data)

            return self.plot.get_plot()

        return update_graph

    def add_data(self, x, y, text, name, mode='markers'):
        self.plot.add_data(x, y, text, name, mode=mode)

    def add_update_graph(self, update_function):
        """
        Add a function that will be run for updating the graph
        Args:
            update_function: Function to run

        Returns:

        """
        self.update_function = update_function


if __name__ == '__main__':
    test = BasicApp('X', 'Y', 'Testing', y_scale='log')
    test.add_data([0.1, 0.4], [1.0, 0.1], 'nothing', 'name', 'lines+markers')
    # html.Div(
    #
    # )
    # test.add_div('')
    test.build_app()
    test.app.run_server(debug=True)
