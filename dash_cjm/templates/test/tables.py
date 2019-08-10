from dash_cjm.templates.html_tables.basic_table import BasicTable
from dash_cjm.plots.BasicApp import BasicApp



if __name__ == '__main__':
    test = BasicApp('X', 'Y', 'Testing')
    table = BasicTable(name='test_table')
    test.add_div(table.get_html(['0', '1'], data=[['2', '3'], ['poop', 'yes']]))
    test.build_app()
    test.app.run_server(debug=True)
