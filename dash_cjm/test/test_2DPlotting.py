"""
Testing program for 2D plotting
"""
from dash_cjm.plots.Plotting2DApp import Plotting2DApp, StaticPlotting2DApp
import numpy as np


def test_compute(input_dict=None):

    return {'Id': np.array([[1, 2], [4, 5]]), 'Ig': np.array([[3, 4]]), 'Vd': np.array([[1, 2]]), 'class': ['in', 'in'],
            'Vg': np.array([[3, 4], [3, 4]])}

    # output = {'Id': input_dict['Vg'] * 10 + input_dict['Vd'], 'Ig': input_dict['Vd']}
    #
    # return output


if __name__ == '__main__':
    test = StaticPlotting2DApp(name='Testing', y_scale='log', y_variables=['Id', 'Ig'], x_variables=['Vg', 'Vd'],
                               compute_function=test_compute, class_name='class')
    test.build_app()
    test.app.run_server(debug=True)
