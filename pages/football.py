# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import json
import urllib
import requests

#add link
dash.register_page(__name__, name='Football')

# Incorporate API data
url = 'https://api.sportsdata.io/v4/soccer/scores/json/Standings/EPL/2024?key=8121a5d8365d4b93aea0f054d01a48eb'
response = requests.get(url)

#Convertion of json to panadas dataframe
epldata = response.json()
epl = pd.json_normalize(epldata, record_path='Standings')

#Define column names
epl.columns = ['StandingId', 'RoundId', 'TeamId', 'Name', 'ShortName', 'Scope',
       'Rank', 'Games', 'Wins', 'Losses', 'Draws', 'GoalsScored',
       'GoalsAgainst', 'GoalsDifferential', 'Points', 'Group', 'GlobalTeamID']

#Data transformation
epl_standings = epl[['Rank', 'TeamId', 'Name', 'ShortName',
        'Games', 'Wins', 'Losses', 'Draws', 'GoalsScored',
       'GoalsAgainst', 'GoalsDifferential', 'Points']].sort_values(by='Points', ascending=False)

# Initialize the app
#app = Dash(__name__)

# App layout
layout = html.Div([
    html.Div(children='Football API Integration'),
    html.Hr(),
    dash_table.DataTable(data=epl_standings.to_dict('records'), page_size=10),
    html.Br(),
    html.Br(),
    dcc.Dropdown(['Wins', 'Losses', 'Draws', 'GoalsScored',
       'GoalsAgainst', 'GoalsDifferential', 'Points'], 'Wins', id='demo-dropdown'),
    html.Br(),
    html.Div([dcc.Graph(figure={}, id='bar-graph')], style={"display":"flex"}),
])

# Add controls to build the interaction
@callback(
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id='demo-dropdown', component_property='value'),
    prevent_initial_call=True,
)
def update_graph(col_chosen):
    fig = fig = px.bar(epl_standings, x='Name', y=col_chosen, title=f"Teams and their total {col_chosen}",width=1300, height=450)
    return fig