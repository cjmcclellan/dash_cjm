import plotly.graph_objs as go


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
    
    def __init__(self, x_scale, x_label, x_min, x_max, y_scale, y_label, y_min, y_max):

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
        self.legend_pos = {'x': 1.02, 'y': 0.95}
        self.margin = {'l': 60, 'b': 40, 't': 10, 'r': 60}
        self.hovermode = 'closest'


        # basic marker properties
        self.mode = 'markers'
        self.opacity = 0.7
        self.marker = {
                          'size': 15,
                          'line': {'width': 1.0, 'color': 'black'},
                          'symbol': 'square'
                      }
        
        # placeholders
        self.data = {}
    
    def add_data(self, x_data, y_data, text, name):
        if self.data.get(name, None) is None:
            self.data[name] = {'x': [], 'y': [], 'text': []}

        self.data[name]['x'].append(x_data)
        self.data[name]['y'].append(y_data)
        self.data[name]['text'].append(text)

    def get_plot(self):
        return {
            'data': self._get_data(),
            'layout': self._get_layout()
        }

    def _get_data(self):
        data = [go.Scatter(
            x=d['x'],
            y=d['y'],
            text=d['text'],
            name=key,
            mode=self.mode,
            opacity=self.opacity,
            marker=self.marker

        ) for key, d in self.data.items()]
        return data

    def _get_layout(self):
        layout = go.Layout(
            xaxis={'type': self.x_scale, 'title': self.x_label, 'showline': self.x_showline, 'mirror': self.x_mirror, 'automargin': self.x_automargin,
                   'tickfont': self.x_tickfont, 'titlefont': self.x_titlefont, 'range': [self.x_min, self.x_max]},
            yaxis={'type': self.y_scale, 'title': self.y_label, 'showline': self.y_showline, 'mirror': self.y_mirror,
                   'automargin': self.y_automargin, 'exponentformat': self.y_exponentformat,
                   'tickfont': self.y_tickfont, 'titlefont': self.y_titlefont, 'range': [self.y_min, self.y_max]},
            margin=self.margin,
            legend=self.legend_pos,
            hovermode=self.hovermode
        )
        return layout
