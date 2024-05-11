# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
from pandas import json_normalize
import plotly.express as px
import json
import urllib
import requests

#add link
dash.register_page(__name__, name='Basketball')

# Incorporate API data
data_array = []
for i in range(6):
    number = 2019
    url = f'https://nba-stats-db.herokuapp.com/api/playerdata/season/{number+i}'
    response_bball = requests.get(url)
    raw = response_bball.json()
    json_data = json_normalize(raw['results'])
    data_array.append(json_data)
nba = pd.concat([ data_array[0], data_array[1], data_array[2], data_array[3], data_array[4], data_array[5]],axis=0)
nba['season'] = nba['season'].astype('object')

# Select appropriate fields
nba = nba[['id', 'player_name', 'age', 'games', 'games_started', 'minutes_played',
       'field_goals', 'field_attempts', 'three_fg',
       'three_attempts', 'two_fg', 'two_attempts', 'ft', 'fta', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'team',
       'season']]

#Data transformation
nba_grp = nba.groupby(['player_name','team','season'],as_index=False).sum().sort_values(by='season')

# Initialize the app
#app = Dash(__name__)

# App layout
layout = html.Div([
    html.Div(children='Baseball API intergration'),
    html.Hr(),
    dash_table.DataTable(data=nba_grp.to_dict('records'), page_size=6),
    html.Br(),
    html.Br(),
    html.Div([
        'x-axis values',
        dcc.Dropdown(['age', 'games', 'games_started', 'minutes_played',
       'field_goals', 'field_attempts', 'three_fg',
       'three_attempts', 'two_fg', 'two_attempts', 'ft', 'fta', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'team',
       'season'], 'age', id='dropdown-menu-xitem'),
       'y-axis values',
        dcc.Dropdown(['age', 'games', 'games_started', 'minutes_played',
       'field_goals', 'field_attempts', 'three_fg',
       'three_attempts', 'two_fg', 'two_attempts', 'ft', 'fta', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'team',
       'season'], 'games', id='dropdown-menu-yitem'),
       'color values',
        dcc.Dropdown(['age', 'games', 'games_started', 'minutes_played',
       'field_goals', 'field_attempts', 'three_fg',
       'three_attempts', 'two_fg', 'two_attempts', 'ft', 'fta', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'team',
       'season'], 'games_started', id='dropdown-menu-coloritem'),
       ]),
    html.Br(),
    html.Div([dcc.Graph(figure={}, id='scatter-graph')]),
    html.Br(),
    html.Div(['Change y-axis']),
    dcc.Dropdown(['games', 'games_started', 'minutes_played',
       'field_goals', 'field_attempts', 'three_fg',
       'three_attempts', 'two_fg', 'two_attempts', 'ft', 'fta', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'], 'field_goals', id='below-dropdown-menu-yitem'),
    html.Div([dcc.Graph(figure={}, id='nba-bar-graph1'), dcc.Graph(figure={}, id='hist-graph'), dcc.Graph(figure={}, id='nba-bar-graph2')], style={"display":"flex"}),
])

# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Output(component_id='nba-bar-graph2', component_property='figure'),
    Output(component_id='hist-graph', component_property='figure'),
    Output(component_id='nba-bar-graph1', component_property='figure'),
    Input(component_id='dropdown-menu-xitem', component_property='value'),
    Input(component_id='dropdown-menu-yitem', component_property='value'),
    Input(component_id='dropdown-menu-coloritem', component_property='value'),
    Input(component_id='below-dropdown-menu-yitem', component_property='value'),
    prevent_initial_call=True,
)
def update_graph(x_col_chosen,y_col_chosen, cl_col_chosen,y2_col_chosen):
    fig1 = px.scatter(nba_grp, x=x_col_chosen, y=y_col_chosen, color=cl_col_chosen)
    fig2 = px.bar(nba_grp, x='team', y=y2_col_chosen, height=450,width=450)
    fig3 = px.histogram(nba_grp, x='age', y=y2_col_chosen, height=450,width=450)
    fig4 = px.bar(nba_grp, x='season', y=y2_col_chosen, height=450,width=450)
    return fig1, fig2, fig3, fig4


