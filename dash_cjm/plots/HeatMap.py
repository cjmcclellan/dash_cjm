import plotly.graph_objs as go
from .DashPlot import DashPlot


class DashHeatMap(DashPlot):

    def __init__(self, map_x_range=(-1, 1), map_y_range=(-1, 1), data_scale='linear', *args, **kwargs):

        super(DashHeatMap, self).__init__(*args, **kwargs)

        # save the data scale
        assert data_scale is 'linear' or data_scale is 'log', 'You can only have linear or log data scales'
        self.data_scale = data_scale

        # save the data on the range of the map
        self.map_x_range = map_x_range
        self.map_y_range = map_y_range

    def get_plot_data(self, new_data):
        data = go.Heatmap(z=new_data, colorbar={'title': 'Temperature'})
        return {
            'data': [data]
        }
