"""
Uploading CSV, XLS, and TXT data files
"""
import dash
import dash_core_components as dcc
import dash_html_components as html


def get_upload_div(message):
    """
    Get an upload data div
    Args:
        message (str): The message to add to the upload module

    Returns:
        dash html.Div
    """
    return html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select {0}'.format(message)),
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Do not allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='output-data-upload'),
            html.Div(id='uploaded-data',
                     style={'display': 'none', 'width': '50%'}
                     )
    ])

