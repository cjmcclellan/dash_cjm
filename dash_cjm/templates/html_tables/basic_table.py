import dash_core_components as dcc
import dash_html_components as html
from dash_cjm.templates.html_object import HTMLObject


class BasicTable(HTMLObject):

    def get_html(self, columns, data):
        assert len(columns) == len(data[0]), 'Your column and data numbers are off. Columns shape == (num columns,)' \
                                             ' and data shape == (num rows, num columns)'
        result = html.Div(
            id=self.name,
            style={},
            children=[
                html.Table(
                    [html.Tr([html.Th(col) for col in columns], className='thead-dark')] +
                    [html.Tr([
                        html.Td(j) for j in i
                    ]) for i in data],
                    className='table table-striped table-bordered table-sm'
                )
            ]
        )

        return result
