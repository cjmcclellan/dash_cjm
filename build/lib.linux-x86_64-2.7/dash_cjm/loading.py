import io
import base64
import pandas as pd
import dash_html_components as html
import os


# load the given contents into a pandas dataframe
def load_csv_or_xls(contents, filename):

    try:
        if 'csv' in filename:
            # if the filename is a path, try to import that, otherwise bytes stream
            if os.path.exists(filename):
                df = pd.read_csv(filename)
            else:
                content_type, content_string = contents.split(',')

                decoded = base64.b64decode(content_string)
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            content_type, content_string = contents.split(',')

            decoded = base64.b64decode(content_string)
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df
