import unittest
from Basic import BasicPlot
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# class TestBasicPlotting():

    # def test_plotting(self):
plot = BasicPlot(x_label='Test X', y_label='Test Y', x_max=1, x_min=0.1,
                 y_max=1, y_min=0.1, x_scale='linear', y_scale='log')

plot.add_data(0.2, 1, 'nothing', 'something')


def basic_dash():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(
        [dcc.Graph('Testing'),
        dcc.Input(name='blank',
                  id='blank')]
    )

    return app


app = basic_dash()


@app.callback(Output('Testing', 'figure'),
              [Input('blank', 'value')])
def update_graph(blank):
    a = plot.get_plot()
    return a


if __name__ == '__main__':
    app.run_server(debug=True)
