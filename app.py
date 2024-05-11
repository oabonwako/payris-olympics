# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input


# Initialize the app
app = dash.Dash(__name__,use_pages=True)
server = app.server
# App layout
app.layout = html.Div([
    html.Div(children='2024 Payris FunOlympic Games analysis tool', style={'fontSize':50, 'textAlign':'center'}),
    html.Div([
        dcc.Link(page['name']+" | ", href=page['relative_path'])
        for page in dash.page_registry.values()
    ]),
    html.Hr(),

    #Content of each page
    dash.page_container
])
# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

#NB type in terminal {python app.py} to launch the app

