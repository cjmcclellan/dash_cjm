import dash_core_components as dcc
import dash_html_components as html


def NamedInput(name, **kwargs):
    return html.Div([
        html.P('{}:'.format(name), style={'margin-left': '3px'}),
        dcc.Input(**kwargs)
        ])


def NamedDropdown(name, **kwargs):
    return html.Div([
        html.P('{}:'.format(name), style={'margin-left': '3px'}),
        dcc.Dropdown(**kwargs)
        ])


def NamedSlider(name, **kwargs):
    return html.Div([
        html.P('{}:'.format(name), style={'margin-left': '3px'}),
        dcc.Slider(**kwargs)
        ])


def NamedRadio(name, **kwargs):
    return html.Div([
        html.P('{}:'.format(name), style={'margin-left': '3px'}),
        dcc.RadioItems(**kwargs)
        ])

