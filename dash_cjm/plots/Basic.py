import plotly.graph_objs as go
import numpy as np
import copy
from collections import OrderedDict
from .DashPlot import DashPlot
import os


class BasicPlot(DashPlot):
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

    marker_color = [
                    '#d62728',  # brick red
                    '#9467bd',  # muted purple
                    '#1f77b4',  # muted blue
                    '#ff7f0e',  # safety orange
                    # '#2ca02c',  # cooked asparagus green
                    '#8c564b',  # chestnut brown
                    # '#e377c2',  # raspberry yogurt pink
                    '#7f7f7f',  # middle gray
                    '#bcbd22',  # curry yellow-green
                    '#17becf'   # blue-teal
                    ]

    i_current_shape = 0
    i_current_color = 0
    i_special_color = 0

    def __init__(self, x_label, y_label, x_min=None, x_max=None, x_scale='linear', y_scale='linear', y_min=None, y_max=None,
                 all_classes=None, mode='markers', graph_height=None, graph_width=None, marker_size=15, line_width=3.0,
                 marker_shapes=('circle', 'square', 'triangle-left'), figure_border=2, layout=None):

        super(BasicPlot, self).__init__()

        self.marker_shapes = marker_shapes

        # using the color and shapes, create unique combinations
        self.marker_styles = []
        # for i_color in range(len(self.marker_color)):
        i_color = 0
        i_repeat = len(self.marker_color) % len(self.marker_shapes)
        if i_repeat != 0:
            i_repeat = 0
        else:
            i_repeat = 1
        for i_all in range(len(self.marker_color)*len(self.marker_shapes)):
            for shape in self.marker_shapes:
                # i_select = i_color
                if i_color >= len(self.marker_color):
                    i_color = i_repeat
                    i_repeat += i_repeat
                    # i_select = i_color - len(self.marker_color)
                self.marker_styles.append((shape, self.marker_color[i_color]))
                i_color += 1
        # self.marker_styles = [(shape, color) for shape in self.marker_shapes for color in self.marker_color]

        # save the input properties
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.x_label = x_label
        self.x_min = x_min
        self.x_max = x_max
        self.y_label = y_label
        self.y_min = y_min
        self.y_max = y_max
        self.figure_border = figure_border # width of the figure border

        # save additional layout options added by the user and add graph height and graph width if they are not None
        self.layout = layout if layout is not None else {}
        if graph_width is not None:
            self.layout['width'] = graph_width
        if graph_height is not None:
            self.layout['height'] = graph_height

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

        # basic marker and line properties
        self.mode = mode
        # self.line_width = line_width
        self.opacity = 0.7
        self.marker = {
            'size': marker_size,
            'line': {'width': 1.0, 'color': 'black'},
            # 'symbol': 'circle'
        }
        self.line = {
            'width': line_width
        }

        # now create markers for all the classes if all classes were given
        self.class_markers = {}
        if all_classes is not None:
            for i, _class in enumerate(all_classes):
                marker = self._set_marker_shape(i)
                self.class_markers[_class] = marker

        # placeholders
        self.data = OrderedDict()

    def add_data(self, x_data, y_data, text, name, mode, error_y=None, error_x=None):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': [], 'mode': []}

        self.__add_data(x_data, y_data, text, name, error_y, error_x, mode)
        # self.data[name]['x'].append(x_data)
        # self.data[name]['y'].append(y_data)
        # self.data[name]['text'].append(text)
        # self.data[name]['mode'].append(mode)

    def add_special_data(self, x_data, y_data, text, name, error_y=None, error_x=None):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': [], 'special': True}

        self.__add_data(x_data, y_data, text, name, error_y, error_x)

        # self.data[name]['x'].append(x_data)
        # self.data[name]['y'].append(y_data)
        # self.data[name]['text'].append(text)

    def add_highlight_subset_data(self, x_data, y_data, text, name, set, error_y=None, error_x=None):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': [], 'highlight': True, 'set': set}

        self.__add_data(x_data, y_data, text, name, error_y, error_x)

        # self.data[name]['x'].append(x_data)
        # self.data[name]['y'].append(y_data)
        # self.data[name]['text'].append(text)

    def __add_data(self, x_data, y_data, text, name, error_y=None, error_x=None, mode=None):

        # if x and y_data are not lists, then append to the data
        if not isinstance(x_data, list) and not isinstance(x_data, np.ndarray):
            self.data[name]['x'].append(x_data)
            self.data[name]['y'].append(y_data)
        # else concat them
        else:
            self.data[name]['x'] += list(x_data)
            self.data[name]['y'] += list(y_data)

        # add the error y and x if they are not None
        if error_y is not None:
            assert isinstance(error_y, dict), 'The error_y data is not in dictionary form.  Please make sure error_y follows plotly format'
            assert self.data[name].get('error_y', None) is None, 'You are attempting to add error to y_data that has already been added.' \
                                                                 '  To add error data, you must add all the x and y data in a single add_data() call'
            self.data[name]['error_y'] = error_y
        if error_x is not None:
            assert isinstance(error_x, dict), 'The error_x data is not in dictionary form.  Please make sure error_x follows plotly format'
            assert self.data[name].get('error_x', None) is None, 'You are attempting to add error to x_data that has already been added.' \
                                                                 '  To add error data, you must add all the x and y data in a single add_data() call'
            self.data[name]['error_x'] = error_x

        self.data[name]['text'].append(text)

        if mode is not None:
            self.data[name]['mode'].append(mode)

    # add a trend line
    def add_line(self, x_data, y_data, mode='lines', name=None):
        self.lines.append({'x': x_data, 'y': y_data, 'mode': mode, 'name': name})

    def get_plot(self, new_data=None, as_figure=False):
        if new_data is not None:
            for d in new_data:
                self.add_data(d[0], d[1], d[2], d[3], d[4])
        plot = {
            'data': self._get_data(),
            'layout': self._get_layout()
        }
        if as_figure:
            return go.Figure(plot)
        else:
            return plot

    def _set_marker_shape(self, i, _class=None, data=None):

        marker = copy.deepcopy(self.marker)
        if self.class_markers.get(_class, None) is not None:
            marker = copy.deepcopy(self.class_markers[_class])

        elif data is not None and data.get('highlight', None) is not None:
            marker = copy.deepcopy(self.class_markers[data['set']])
            marker['line']['width'] = 3.0

        else:
            if self.i_current_shape == len(self.marker_styles):
                self.i_current_shape = 0
                # self.i_current_color += 1
                # if self.i_current_color == len(self.marker_color):
                #     self.i_current_color = 0
            marker['symbol'] = self.marker_styles[self.i_current_shape][0]
            marker['color'] = self.marker_styles[self.i_current_shape][1]

        # now check for special conditions
        if data is not None:
            if data.get('special', None) is not None:
                marker['symbol'] = 'star'
                marker['color'] = self.marker_color[self.i_special_color]
                self.i_special_color += 1
        self.i_current_shape += 1
        return marker

    def _get_data(self):
        # add all the data points
        data = []
        i_shape = 0
        for key, d in self.data.items():
            marker = self._set_marker_shape(i_shape + 1, _class=key, data=d)
            # self.marker
            # if d.get('special', None) is not None:
            #     marker['symbol'] = 'star'
            scatter_dict = {
                'x': np.array(d['x']),
                'y': np.array(d['y']),
                'text': np.array(d['text'][0]),
                'name': key,
                'mode': self.mode if d.get('mode', None) is None else d['mode'][0],
                'opacity': self.opacity,
                'marker': marker,
                # 'line'
            }
            error_y = d.get('error_y', None)
            error_x = d.get('error_x', None)
            if error_y is not None:
                scatter_dict['error_y'] = error_y
            if error_x is not None:
                scatter_dict['error_x'] = error_x

            data.append(go.Scatter(**scatter_dict))
            # data.append(go.Scatter(
            #     x=np.array(d['x']),
            #     y=np.array(d['y']),
            #     text=np.array(d['text'][0]),
            #     name=key,
            #     mode=self.mode if d.get('mode', None) is None else d['mode'][0],
            #     opacity=self.opacity,
            #     marker=marker
            # ))
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
            showlegend = False if line['name'] is None else True
            data.append(
                go.Scatter(
                    x=line['x'],
                    y=line['y'],
                    mode=line['mode'],
                    name=line['name'],
                    showlegend=showlegend,
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

        layout_dict = {
            'xaxis': {'type': self.x_scale, 'title': self.x_label, 'showline': self.x_showline, 'mirror': self.x_mirror,
                      'automargin': self.x_automargin, 'linecolor': 'black', 'linewidth': self.figure_border,
                      'tickfont': self.x_tickfont, 'titlefont': self.x_titlefont, 'range': [x_min, x_max]},
            'yaxis': {'type': self.y_scale, 'title': self.y_label, 'showline': self.y_showline, 'mirror': self.y_mirror,
                      'automargin': self.y_automargin, 'exponentformat': self.y_exponentformat, 'linecolor': 'black',
                      'linewidth': self.figure_border,
                      'tickfont': self.y_tickfont, 'titlefont': self.y_titlefont, 'range': [y_min, y_max]},
            'margin': self.margin,
            'legend': self.legend,
            'showlegend': self.showlegend,
            'hovermode': self.hovermode,
            'paper_bgcolor': 'rgba(0,0,0,0)',

            # 'height': self.graph_height if self.graph_height is not None else 700,
            # 'width': self.graph_width if self.graph_width is not None else 700,
            # 'plot_bgcolor': '#fff',
            **self.layout,
        }

        # for key in (('height', 'graph_height'), ('width', 'graph_width'), ('layout', 'layout')):
        #     if self.__dict__[key[1]] is not None:
        #         layout_dict[key[0]] =
        layout = go.Layout(**layout_dict)
        # layout = go.Layout(
        #     xaxis={'type': self.x_scale, 'title': self.x_label, 'showline': self.x_showline, 'mirror': self.x_mirror,
        #            'automargin': self.x_automargin,
        #            'tickfont': self.x_tickfont, 'titlefont': self.x_titlefont, 'range': [x_min, x_max]},
        #     yaxis={'type': self.y_scale, 'title': self.y_label, 'showline': self.y_showline, 'mirror': self.y_mirror,
        #            'automargin': self.y_automargin, 'exponentformat': self.y_exponentformat,
        #            'tickfont': self.y_tickfont, 'titlefont': self.y_titlefont, 'range': [y_min, y_max]},
        #     margin=self.margin,
        #     legend=self.legend,
        #     showlegend=self.showlegend,
        #     hovermode=self.hovermode,
        #     paper_bgcolor='rgba(0,0,0,0)',
        #     # **self.layout if self.layout is not None else None,
        #     height=self.graph_height if self.graph_height is not None else 700,
        #     width=self.graph_width if self.graph_width is not None else 700,
        #     plot_bgcolor='#fff'
        # )
        return layout

    def save_plot(self, name, path='', file_type='svg'):
        """
        Save the plot as a static image of type file_type
        Args:
            name (str): Name of the static image
            path (str): Path to where the image will be saved. Default is local folder
            file_type (str): The type of image file.  Current options are 'svg' or 'png'.  svg is recommend as this is a vectorized format.

        Returns:
            None
        """
        assert file_type is 'svg' or file_type is 'png', 'Invalid file_type {0}.  Must either be png or svg.'.format(file_type)

        # first get the plot then save it
        plot = self.get_plot(as_figure=True)
        plot.write_image(os.path.join(path, '{0}.{1}'.format(name, file_type)))

# if __name__ == '__main__':
#     test = BasicPlot(x_label='X', y_label='Y')
#     test.add_data(0.1, 0.1, 'nothing', 'name')
#     # html.Div(
#     #
#     # )
#     # test.add_div('')
#     test.build_app()
#     test.app.run_server(debug=True)
