"""
This py will give basic error divs for dash
"""
import dash_html_components as html


def basic_error(error_message):

    return html.Div(
        html.P(
            style={'color': 'warning'},
            children=[
                error_message
            ]
        )
    )
