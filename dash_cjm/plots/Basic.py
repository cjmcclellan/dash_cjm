import plotly.graph_objs as go
import numpy as np


class BasicPlot(object):
    """
        The BasicPlot class is a simple Dash plotting class.
      Args:
          x_scale:
          x_label:
          x_min:
          x_max:
          y_scale:
          y_label:
          y_min:
          y_max:
      """

    # some class properties
    marker_shapes = ['circle', 'square', 'triangle-left']
    i_current_shape = 0
    repeat_shape = 2

    def __init__(self, x_label, y_label, x_min=None, x_max=None, x_scale='linear', y_scale='linear', y_min=None, y_max=None):

        # save the input properties
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.x_label = x_label
        self.x_min = x_min
        self.x_max = x_max
        self.y_label = y_label
        self.y_min = y_min
        self.y_max = y_max

        # save the basic properties for this plot
        self.x_showline = True
        self.x_mirror = True
        self.x_automargin = True
        self.x_tickfont = {'size': 15}
        self.x_titlefont = {'size': 20}
        self.y_showline = True
        self.y_mirror = True
        self.y_automargin = True
        self.y_tickfont = {'size': 15}
        self.y_titlefont = {'size': 20}
        self.y_exponentformat = 'power'
        self.legend = {'x': 1.02, 'y': 0.95, 'font': {'size': 15}}
        self.margin = {'l': 60, 'b': 40, 't': 10, 'r': 60}
        self.hovermode = 'closest'
        self.showlegend = True

        # placeholder for the lines
        self.lines = []

        # basic marker properties
        self.mode = 'markers'
        self.opacity = 0.7
        self.marker = {
            'size': 15,
            'line': {'width': 1.0, 'color': 'black'},
            # 'symbol': 'circle'
        }

        # placeholders
        self.data = {}

    def add_data(self, x_data, y_data, text, name):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': []}

        self.data[name]['x'].append(x_data)
        self.data[name]['y'].append(y_data)
        self.data[name]['text'].append(text)

    def add_special_data(self, x_data, y_data, text, name):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': [], 'special': True}

        self.data[name]['x'].append(x_data)
        self.data[name]['y'].append(y_data)
        self.data[name]['text'].append(text)

    # add a trend line
    def add_line(self, x_data, y_data, name):
        self.lines.append({'x': x_data, 'y': y_data, 'name': name})

    def get_plot(self):
        return {
            'data': self._get_data(),
            'layout': self._get_layout()
        }

    def _set_marker_shape(self, i):
        if self.repeat_shape % i == 0:
            self.i_current_shape += 1
            if self.i_current_shape == len(self.marker_shapes):
                self.i_current_shape = 0
            self.marker['symbol'] = self.marker_shapes[self.i_current_shape]

    def _get_data(self):
        # add all the data points
        data = []
        i_shape = 0
        for key, d in self.data.items():
            self._set_marker_shape(i_shape + 1)
            marker = self.marker
            if d.get('special', None) is not None:
                marker['symbol'] = 'star'

            data.append(go.Scatter(
                x=np.array(d['x'][0]),
                y=np.array(d['y'][0]),
                text=np.array(d['text'][0]),
                name=key,
                mode=self.mode,
                opacity=self.opacity,
                marker=marker
            ))
        # data = [go.Scatter(
        #     x=np.array(d['x'])[0],
        #     y=np.array(d['y'])[0],
        #     text=np.array(d['text'])[0],
        #     name=key,
        #     mode=self.mode,
        #     opacity=self.opacity,
        #     marker=self.marker
        #
        # ) for key, d in self.data.items()]

        # now add lines
        for line in self.lines:
            data.append(
                go.Scatter(
                    x=line['x'],
                    y=line['y'],
                    mode='lines',
                    name=line['name']
                )
            )

        return data

    # update the max and mins
    def update_max_min(self, x_min=None, x_max=None, y_min=None, y_max=None):
        for a in [('x_min', x_min), ('x_max', x_max), ('y_min', y_min), ('y_max', y_max)]:
            if a[1] is not None:
                setattr(self, a[0], a[1])

    def _get_layout(self):

        x_min, x_max, y_min, y_max = (None, None, None, None)

        if self.x_min is not None:
            x_min = float(self.x_min)
        if self.x_max is not None:
            x_max = float(self.x_max)
        if self.y_min is not None:
            y_min = float(self.y_min)
        if self.y_max is not None:
            y_max = float(self.y_max)

        # change to log scale if need be:
        if self.x_scale == 'log':
            if self.x_min is not None:
                x_min = np.log10(self.x_min)
            if self.x_max is not None:
                x_max = np.log10(self.x_max)

        if self.y_scale == 'log':
            if self.y_min is not None:
                y_min = np.log10(self.y_min)
            if self.y_max is not None:
                y_max = np.log10(self.y_max)

        layout = go.Layout(
            xaxis={'type': self.x_scale, 'title': self.x_label, 'showline': self.x_showline, 'mirror': self.x_mirror,
                   'automargin': self.x_automargin,
                   'tickfont': self.x_tickfont, 'titlefont': self.x_titlefont, 'range': [x_min, x_max]},
            yaxis={'type': self.y_scale, 'title': self.y_label, 'showline': self.y_showline, 'mirror': self.y_mirror,
                   'automargin': self.y_automargin, 'exponentformat': self.y_exponentformat,
                   'tickfont': self.y_tickfont, 'titlefont': self.y_titlefont, 'range': [y_min, y_max]},
            margin=self.margin,
            legend=self.legend,
            showlegend=self.showlegend,
            hovermode=self.hovermode
        )
        return layout
