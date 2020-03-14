import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html


def NamedInput(name, style=None, raw_html=False, **kwargs):
    style = __get_style(style)
    if raw_html:
        return html.Div([
            html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('{}:'.format(name)), style=style),
            dcc.Input(**kwargs, style=style)
        ])
    else:
        return html.Div([
            html.P('{}:'.format(name), style=style),
            dcc.Input(**kwargs, style=style)
            ])


def NamedDropdown(name, style=None, **kwargs):
    style = __get_style(style)
    return html.Div([
        html.P('{}:'.format(name), style=style),
        dcc.Dropdown(**kwargs)
        ])


def NamedChecklist(name, style=None, **kwargs):
    style = __get_style(style)
    return html.Div([
        html.P('{}:'.format(name), style=style),
        dcc.Checklist(**kwargs)
    ])


def NamedSlider(name, style=None, **kwargs):
    style = __get_style(style)
    return html.Div([
        html.P('{}:'.format(name), style=style),
        dcc.Slider(**kwargs)
        ])


def NamedRadio(name, style=None, **kwargs):
    style = __get_style(style)
    return html.Div([
        html.P('{}:'.format(name), style=style),
        dcc.RadioItems(**kwargs)
        ])


def __get_style(style):
    # default_style = {'margin-left': '3px'}
    default_style = {}
    if style is None:
        return default_style
    else:
        for key in default_style.keys():
            if style.get(key, None) is None:
                style[key] = default_style[key]
        return style
