# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

#add link
dash.register_page(__name__, name='FunOlympics')

# Incorporate data
df = pd.read_csv("olympics_test_data.csv")

# Transformation
goldMedals = df[(df.medal_type == 'Gold Medal')]
silverMedals = df[(df.medal_type == 'Silver Medal')]
bronzeMedals = df[(df.medal_type == 'Bronze Medal')]
fields = ['name','gender','country','discipline','event','age']
gold = goldMedals[fields].value_counts().reset_index(name='Gold_Medal_Count')
silver = silverMedals[fields].value_counts().reset_index(name='Silver_Medal_Count')
bronze = bronzeMedals[fields].value_counts().reset_index(name='Bronze_Medal_Count')

gold['Silver_Medal_Count'] = silver['Silver_Medal_Count']
gold['Bronze_Medal_Count'] = bronze['Bronze_Medal_Count']

gold['total_medals'] = gold['Bronze_Medal_Count'] + gold['Silver_Medal_Count'] + gold['Gold_Medal_Count']

new_data = gold

# Initialize the app
#app = Dash(__name__)

# App layout
layout = html.Div([
    html.Div(children='Data analysis of the athletes that won medals in each sport event.'),
    html.Hr(),
    dash_table.DataTable(data=new_data.to_dict('records'), page_size=6),
    html.Br(),
    html.Div(['change y-axis',
              dcc.Dropdown(['Bronze_Medal_Count','Silver_Medal_Count','Gold_Medal_Count'], 'Bronze_Medal_Count', id='dropdown-item'),]),
    html.Br(),
    html.Div([dcc.Graph(figure={}, id='olympic-bar-graph1'), dcc.Graph(figure={}, id='olympic-bar-graph2')], style={"display":"flex"}),
])

# Add controls to build the interaction
@callback(
    Output(component_id='olympic-bar-graph1', component_property='figure'),
    Output(component_id='olympic-bar-graph2', component_property='figure'),
    Input(component_id='dropdown-item', component_property='value'),
    prevent_initial_call=True,
)
def update_graph(col_chosen):
    fig1 = px.bar(new_data,x='discipline', y=col_chosen, title=f"Bar chart of each {col_chosen} by medals")
    fig2 = px.bar(new_data,x='country', y=col_chosen, title=f"Bar chart of each {col_chosen} by medals")
    return fig1, fig2
