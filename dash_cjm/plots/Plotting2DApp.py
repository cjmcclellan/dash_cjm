"""
A basic 2D Plotting App.
"""
from dash_cjm.dash_cjm.plots.BasicApp import BasicApp
import dash_core_components as dcc
import dash_html_components as html
from dash_cjm.dash_cjm.named_components import NamedRadio, NamedDropdown, NamedInput
from dash_cjm.dash_cjm.formatting.formatting import create_dropdown_options, create_dash_option, round_to_n
from dash.dependencies import Input, Output, State
import numpy as np


class Plotting2DApp(BasicApp):

    def __init__(self, x_variables, y_variables, inputs, outputs, compute_function, *args, **kwargs):

        self.x_options = create_dropdown_options(x_variables)
        self.y_options = create_dropdown_options(y_variables)

        self.outputs = outputs
        self.compute_function = compute_function

        initial_x = self.x_options[0]['label']
        initial_y = self.y_options[0]['label']

        self.dash_inputs = []

        # for now, only work with two inputs
        assert (len(inputs) < 3), 'The Plotting App only works with 2 inputs right now.'

        for _input in inputs:
            self.dash_inputs.append({'step_id': create_dash_option(_input) + '_step_id', 'min_id': create_dash_option(_input) + '_min_id',
                                     'max_id': create_dash_option(_input) + '_max_id', 'name': _input})

        super(Plotting2DApp, self).__init__(x_label=initial_x, y_label=initial_y, hidden_update=False, *args, **kwargs)

        # save the update graph function
        self.update_function = self.update_graph_func

        # now setup the call back options
        self.callback_inputs += [Input('x-value', 'value'), Input('y-value', 'value'), Input('x-scale', 'value'), Input('y-scale', 'value')]
        for _input in self.dash_inputs:
            self.callback_states.append(State(_input['step_id'], 'value'))
            self.callback_states.append(State(_input['min_id'], 'value'))
            self.callback_states.append(State(_input['max_id'], 'value'))

        input_list = [
            html.Div(className='container', children=[
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            className='col-3',
                            children=[
                                NamedInput(
                                    name='Min value for {0}'.format(_input['name']),
                                    id=_input['min_id'],
                                    value='0.1',
                                    placeholder='Give the min value for {0}'.format(_input['name']),
                                    type='text',
                                ),
                            ]
                        ),
                        html.Div(
                            className='col-3',
                            children=[
                                NamedInput(
                                    name='Max value for {0}'.format(_input['name']),
                                    id=_input['max_id'],
                                    value='1.0',
                                    placeholder='Give the max value for {0}'.format(_input['name']),
                                    type='text',
                                )
                            ]
                        ),
                        html.Div(
                            className='col-3',
                            children=[
                                NamedInput(
                                    name='Step value for {0}'.format(_input['name']),
                                    id=_input['step_id'],
                                    value='0.1',
                                    placeholder='Give the step value for {0}'.format(_input['name']),
                                    type='text',
                                ),
                            ]
                        ),
                    ]
                ),
            ])
            for _input in self.dash_inputs]

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
        ] + input_list

    def update_graph_func(self, *args, **kwargs):

        # recreate the plot with the current x and y labels
        self.init_plot(x_label=kwargs['x-value'], y_label=kwargs['y-value'], x_scale=kwargs['x-scale'], y_scale=kwargs['y-scale'],
                       )

        # first, create np ranges
        compute_input = {}

        input_base_dim = []
        input_names = []
        for dash_input in self.dash_inputs:
            _min, _max, step = kwargs[dash_input['min_id']], kwargs[dash_input['max_id']], kwargs[dash_input['step_id']]

            # if they are all not None, add the data points for the compute input
            if _min is not None and _max is not None and step is not None:
                input_data = np.arange(float(_min), float(_max), float(step))

                compute_input[dash_input['name']] = input_data

                # add the name to the list of input names. If this is to be plotted, then push to the front of
                # the list (used for ensuring proper input matrix's for later)
                if dash_input['name'] == kwargs['x-value']:
                    input_names.insert(0, dash_input['name'])
                    input_base_dim.insert(0, len(input_data))
                else:
                    input_names.append(dash_input['name'])
                    input_base_dim.append(len(input_data))

            # if anything is None, we can not compute so return
            else:
                return None

        # now create a N-dimensional matrix for N inputs [len(input 1), len(input 2), ... , len(input N)]
        input_base = np.ones(input_base_dim)
        n_dim = len(input_base.shape)
        # save which input is not being plotted
        not_plotted_input = None
        plot_input = {}
        for i, key in enumerate(input_names):
            new_axis = list(range(n_dim))
            new_axis[0] = i
            new_axis[i] = 0
            new_input_base = np.transpose(input_base, new_axis)
            plot_input[key] = new_input_base * np.expand_dims(compute_input[key], axis=-1)
            compute_input[key] = np.transpose(plot_input[key], new_axis)

            # save which x is not being plotted
            if key != kwargs['x-value']:
                not_plotted_input = key

        # format the compute input to be flatten
        formatted_compute = {}

        for key in compute_input.keys():
            formatted_compute[key] = compute_input[key].flatten()
        # now compute the data
        output_data = self.compute_function(formatted_compute)

        for key in output_data.keys():
            output_data[key] = np.reshape(output_data[key], newshape=input_base_dim)

        new_data = []
        for i in range(len(compute_input[kwargs['x-value']][0])):
            label = '{0} = {1}'.format(not_plotted_input, round_to_n(compute_input[not_plotted_input][0][i], 3))
            new_data.append([plot_input[kwargs['x-value']][:, i], output_data[kwargs['y-value']][:, i], label, label, 'lines'])

        return new_data


def test_compute(input_dict):

    output = {'Id': input_dict['Vg'] * 10 + input_dict['Vd'], 'Ig': input_dict['Vd']}

    return output


if __name__ == '__main__':
    test = Plotting2DApp(name='Testing', y_scale='log', y_variables=['Id', 'Ig'], x_variables=['Vg', 'Vd'],
                         inputs=['Vg', 'Vd'], outputs=['Id', 'Ig'], compute_function=test_compute)
    test.build_app()
    test.app.run_server(debug=True)
