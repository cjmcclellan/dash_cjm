"""
A basic 2D Plotting App.
"""
from dash_cjm.dash_cjm.plots.BasicApp import BasicApp
import dash_core_components as dcc
import dash_html_components as html
from dash_cjm.dash_cjm.named_components import NamedRadio, NamedDropdown, NamedInput
from dash_cjm.dash_cjm.formatting.formatting import create_dropdown_options, create_dash_option, round_to_n
from dash.dependencies import Input, Output, State
from dash_cjm.dash_cjm.plots.Basic import BasicPlot
import numpy as np


class BasicInputPlotting(BasicApp):

    def __init__(self, x_variables, y_variables, dataset, *args, **kwargs):

        self.x_options = create_dropdown_options(x_variables)
        self.y_options = create_dropdown_options(y_variables)

        self.dataset = dataset

        initial_x = self.x_options[0]['label']
        initial_y = self.y_options[0]['label']

        self.dash_inputs = []

        # for now, only work with two inputs

        super(BasicInputPlotting, self).__init__(x_label=initial_x, y_label=initial_y, hidden_update=False, *args, **kwargs)

        # save the update graph function
        self.update_function = self.update_graph_func

        # now setup the call back options
        self.callback_inputs += [Input('x-value', 'value'), Input('y-value', 'value'), Input('x-scale', 'value'), Input('y-scale', 'value')]

        self.app_layout.children += [
            html.Div(
                className='row',
                children=[
                    html.Div(
                        className='col-sm',
                        children=[
                            NamedDropdown(
                                # style=named_header_style,
                                name='Select a x variable',
                                id='x-value',
                                options=self.x_options,
                                placeholder='Select a x variable.',
                                value=self.x_options[0]['value']  # 4 for setting Contact Spacing as default
                            ),
                            dcc.RadioItems(
                                id='x-scale',
                                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                                value='log',
                            ),
                        ]
                    ),
                    html.Div(
                        className='col-sm',
                        children=[
                            NamedDropdown(
                                # style=named_header_style,
                                name='Select a y variable',
                                id='y-value',
                                options=self.y_options,
                                placeholder='Select a y variable',
                                value=self.y_options[0]['value']
                            ),
                            dcc.RadioItems(
                                id='y-scale',
                                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                                value='log',
                            )
                        ]
                    ),
                ]
            ),
        ]

    def init_plot(self, x_label, y_label, x_scale, y_scale):

        self.plot = BasicPlot(x_label=x_label, y_label=y_label, x_scale=x_scale, y_scale=y_scale,
                              graph_height=self.graph_height, graph_width=self.graph_width, marker_shapes=('circle',))

        # make the plot only have circles
        self.plot.marker['size'] = 8

    def update_graph_func(self, *args, **kwargs):

        # recreate the plot with the current x and y labels
        self.init_plot(x_label=kwargs['x-value'], y_label=kwargs['y-value'], x_scale=kwargs['x-scale'], y_scale=kwargs['y-scale'],
                       )

        new_data = [[self.dataset[kwargs['x-value']], self.dataset[kwargs['y-value']], '', '', 'lines+markers']]
        # for i in range(len(compute_input[kwargs['x-value']][0])):
        #     label = '{0} = {1}'.format(not_plotted_input, round_to_n(compute_input[not_plotted_input][0][i], 3))
        #     new_data.append([plot_input[kwargs['x-value']][:, i], output_data[kwargs['y-value']][:, i], label, label, 'lines+markers'])

        return new_data


def test_compute(input_dict):

    output = {'Id': input_dict['Vg'] * 10 + input_dict['Vd'], 'Ig': input_dict['Vd']}

    return output


if __name__ == '__main__':
    test = BasicInputPlotting(name='Testing', y_scale='log', y_variables=['Vg', 'Vd'], x_variables=['Vd', 'Vg'],
                              dataset={'Vd': [0, 1, 2, 3], 'Vg': [3, 2, 1, 0]})
    test.build_app()
    test.app.run_server(debug=True)
