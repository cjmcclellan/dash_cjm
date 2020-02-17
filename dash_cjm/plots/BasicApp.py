import unittest
from dash_cjm.plots.Basic import BasicPlot
from dash_cjm.loading import load_csv_or_xls
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import pandas as pd


class BaseApp(object):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    name = None

    def __init__(self, name, django=False, add_bootstrap_links=False):

        self.name = name

        if django:
            self.app = DjangoDash(name, add_bootstrap_links=add_bootstrap_links)
        else:
            self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)


class BasicApp(BaseApp):

    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    def __init__(self, x_label, y_label, x_scale='linear', y_scale='linear', hidden_update=True,
                 graph_height=None, graph_width=None, upload_input=False, *args, **kwargs):

        super(BasicApp, self).__init__(*args, **kwargs)

        self.graph_height = graph_height
        self.graph_width = graph_width

        self.upload_input = upload_input

        self.init_plot(x_label=x_label, y_label=y_label, x_scale=x_scale, y_scale=y_scale)

        self.update_function = None

        # the callback options
        self.callback_inputs = []
        self.callback_states = []
        self.callback_outputs = []

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

    def add_div(self, div, top=False, bottom=False):
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

        # if there is an upload data module, run the callback creator
        if self.upload_input:
            self._upload_input_callback()

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

        @self.app.callback([Output(self.name, 'figure')] + self.callback_outputs,
                           [Input('update_' + self.name, 'n_clicks')] + self.callback_inputs, self.callback_states)
        def update_graph(update_n, *args):
            # create the kwargs
            output_callbacks = tuple([None for i in self.callback_outputs])
            callbacks = self.callback_inputs + self.callback_states
            kwargs = {callback.component_id: _input for _input, callback in zip(args, callbacks)}
            # if data was uploaded to through an upload module, then convert the json to a dataframe
            if self.upload_input:
                kwargs['uploaded-data'] = self._read_df_from_json(kwargs['uploaded-data'])

            if self.update_function is not None:
                new_data = self.update_function(update_n, **kwargs)
                # print(new_data)
                if new_data is not None:
                    # if new data is a dict, then extract the plot and callback data
                    if isinstance(new_data, dict):
                        callback_data = new_data['callback_data']
                        new_data = new_data['plot_data']
                        # look through the new data for any outputs that match the callback_outputs
                        callback_outputs = [callback_data.get(callback.component_id, None) for callback in self.callback_outputs]
                    else:
                        callback_outputs = output_callbacks

                    return (self.plot.get_plot(new_data=new_data),) + tuple(callback_outputs)

            return (self.plot.get_plot(),) + output_callbacks

        return update_graph

    def add_data(self, x, y, text, name, mode='markers'):
        self.plot.add_data(x, y, text, name, mode=mode)

    def _upload_input_callback(self):
        """
        Create the callback for uploading data
        Returns:

        """

        @self.app.callback(Output('uploaded-data', 'children'),
                           [Input('upload-data', 'contents')],
                           [State('upload-data', 'filename')])
        def process_uploaded_data(contents, names):

            if contents is None:
                return None
            else:
                cleaned_data = load_csv_or_xls(contents, names)

            # now return the data as json
            return cleaned_data.to_json(orient='split')

        return process_uploaded_data

    @staticmethod
    def _read_df_from_json(json_data):
        """
        Simply read read json data and output a pandas dataframe
        Args:
            json_data (str): Json string of data to be read

        Returns:
            pd.DataFrame or None if json_data was None
        """
        if json_data is None:
            return json_data
        return pd.read_json(json_data, orient='split')

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
