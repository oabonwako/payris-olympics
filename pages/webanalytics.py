import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#add link
dash.register_page(__name__, path='/', name='Web Analytics')

#1. Load web log file
test_data = pd.read_csv('websitelog.csv')

#2. Data Transformation
first = test_data.columns
columns = ['ip_address','datetime','HTTPResponse','last_status_code',
                'sports_event','interaction_type','view_duration(mins)','Ad_Revenue($)','session_duration(mins)','Latitude','Longitude','country_of_origin','continent','traffic_source',
                'device_type','browser_type','response_time','content_size']
test_data.columns = columns
test_data.loc[len(test_data.index)] = first
test_data = test_data.sort_values(by='datetime')

#2.1 Change data types
test_data[['view_duration(mins)']] = test_data[['view_duration(mins)']].astype('int64')
test_data[['Ad_Revenue($)']] = test_data[['Ad_Revenue($)']].astype('int64')
test_data[['session_duration(mins)']] = test_data[['session_duration(mins)']].astype('int64')

#2.2 grouping data
test_grp = test_data[['datetime','interaction_type','traffic_source','device_type','browser_type','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['datetime','interaction_type','traffic_source','device_type','browser_type'],as_index=False).sum()
test_grp1 = test_data[['datetime','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['datetime'],as_index=False).sum()
test_grp2 = test_data[['datetime','interaction_type','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['datetime','interaction_type'],as_index=False).sum()
test_grp3 = test_data[['Latitude','Longitude','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['Latitude','Longitude',],as_index=False).sum()
test_grp4 = test_data[['country_of_origin','Latitude','Longitude','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['country_of_origin','Latitude','Longitude',],as_index=False).sum()
test_grp5 = test_data[['continent','Latitude','Longitude','view_duration(mins)','Ad_Revenue($)','session_duration(mins)']].groupby(['continent','Latitude','Longitude'],as_index=False).sum()

#3 Initialize line figure
fig = go.Figure()

# Add Traces

fig.add_trace(
    go.Scatter(x=list(test_grp1.datetime),
               y=list(test_grp1['Ad_Revenue($)']),
               name="Ad_Revenue",
               line=dict(color="#33CFA5")))

fig.add_trace(
    go.Scatter(x=list(test_grp1.datetime),
               y=[test_grp1['Ad_Revenue($)'].mean()] * len(test_grp1.index),
               name="Ad_Revenue Average",
               visible=False,
               line=dict(color="#33CFA5", dash="dash")))

fig.add_trace(
    go.Scatter(x=list(test_grp1.datetime),
               y=list(test_grp1['view_duration(mins)']),
               name="view_duration(mins)",
               line=dict(color="#F06A6A")))

fig.add_trace(
    go.Scatter(x=list(test_grp1.datetime),
               y=[test_grp1['view_duration(mins)'].mean()] * len(test_grp1.index),
               name="view_duration(mins) Average",
               visible=False,
               line=dict(color="#F06A6A", dash="dash")))

# Add Annotations and Buttons
high_annotations = [dict(x="2018-03-01",
                         y=test_grp1['Ad_Revenue($)'].mean(),
                         xref="x", yref="y",
                         text="Ad_Revenue Average:<br> %.3f" % test_grp1['Ad_Revenue($)'].mean(),
                         ax=0, ay=-40),
                    dict(x=test_grp1.datetime[test_grp1['Ad_Revenue($)'].idxmax()],
                         y=test_grp1['Ad_Revenue($)'].max(),
                         xref="x", yref="y",
                         text="Ad_Revenue Max:<br> %.3f" % test_grp1['Ad_Revenue($)'].max(),
                         ax=-40, ay=-40)]
low_annotations = [dict(x="2018-10-01",
                        y=test_grp1['view_duration(mins)'].mean(),
                        xref="x", yref="y",
                        text="view_duration Average:<br> %.3f" % test_grp1['view_duration(mins)'].mean(),
                        ax=0, ay=40),
                   dict(x=test_grp1.datetime[test_grp1['Ad_Revenue($)'].idxmin()],
                        y=test_grp1['view_duration(mins)'].min(),
                        xref="x", yref="y",
                        text="view_duration Min:<br> %.3f" % test_grp1['view_duration(mins)'].min(),
                        ax=0, ay=40)]

fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="None",
                     method="update",
                     args=[{"visible": [True, False, True, False]},
                           {"title": "Ad Revenue($) and View duration of streams by date",
                            "annotations": []}]),
                dict(label="Ad_Revenue",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {"title": "Ad Revenue($) from streams by date",
                            "annotations": high_annotations}]),
                dict(label="view_duration(mins)",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "View duration of streams by date",
                            "annotations": low_annotations}]),
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Ad Revenue($) and View duration of streams by date, including average",
                            "annotations": high_annotations + low_annotations}]),
            ]),
        )
    ])

# Set title and date range buttons
fig.update_layout(
    title_text="Ad Revenue($) and View duration of streams",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)


import plotly.graph_objects as go
from plotly.subplots import make_subplots


# frequency of Country
freq = test_grp4
freq = test_grp4.country_of_origin.value_counts().reset_index().rename(columns={"index": "x"})

fre2 = test_grp5
freq2 = test_grp5.continent.value_counts().reset_index().rename(columns={"index": "x"})


data = test_grp3.sample(1000)
# Initialize figure with subplots
fig3 = make_subplots(
    rows=2, cols=2,
    column_widths=[0.6, 0.4],
    row_heights=[0.4, 0.6],
    specs=[[{"type": "scattergeo", "rowspan": 2}, {"type": "bar"}],
           [            None                    , {"type": "bar"}]])

# Add scattergeo globe map of volcano locations
fig3.add_trace(
    go.Scattergeo(lat=data["Latitude"],
                  lon=data["Longitude"],
                  mode="markers",
                  hoverinfo="text",
                  showlegend=False,
                  marker=dict(color="crimson", size=4, opacity=0.8)),
    row=1, col=1
)

# Add locations bar chart
fig3.add_trace(
    go.Bar(x=freq2["continent"][0:10],y=freq2["count"][0:10], marker=dict(color="crimson"), showlegend=False),
    row=1, col=2
)

# Add locations bar chart
fig3.add_trace(
    go.Bar(x=freq["country_of_origin"][0:10],y=freq["count"][0:10], marker=dict(color="crimson"),showlegend=False),
    row=2, col=2
)

# Update geo subplot properties
fig3.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue",
)

# Rotate x-axis labels
fig3.update_xaxes(tickangle=45)

# Set theme, margin, and annotation in layout
fig3.update_layout(
    margin=dict(r=10, t=25, b=40, l=60),
    title_text='Total count of visits for each country of origin and continent',
    annotations=[
        dict(
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)



# Initialize the app
#app = Dash(__name__)

# App layout
layout = html.Div([
    html.Div(children='Web analytics for the Olympic website to aid marketing and advertising'),
    html.Hr(),
    dash_table.DataTable(data=test_grp.to_dict('records'), page_size=6),
    html.Br(),
    html.Br(),
    html.Div([dcc.Graph(figure=fig)]),
    html.Br(),
    html.Br(),
    html.Div([dcc.Graph(figure=fig3)]),
    html.Br(),
    html.Br(),
    html.Div(children='yaxis Controls for line and pie'),
    dcc.Dropdown(['view_duration(mins)','Ad_Revenue($)','session_duration(mins)'],'view_duration(mins)', id='line-and-pie-dropdown-menu'),
    html.Br(),
    html.Br(),
    html.Div(children='xaxis Controls for pie'),
    dcc.Dropdown(['traffic_source','device_type','browser_type'], 'traffic_source', id='dropdown-menu'),
    html.Div([dcc.Graph(figure={}, id='line-graph'), dcc.Graph(figure={}, id='pie-graph')], style={"display":"flex"}),
])

# Add controls to build the interaction
@callback(
    Output(component_id='line-graph', component_property='figure'),
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='dropdown-menu', component_property='value'),
    Input(component_id='line-and-pie-dropdown-menu', component_property='value'),
    #prevent_initial_call=True
)
def update_graph(x_col_chosen, y_col_chosen):
    fig1 = px.pie(test_grp, values=y_col_chosen, names=x_col_chosen, hole=.5, title=f"Pie chart of {x_col_chosen} by {y_col_chosen}")
    #line graph
    fig2 = px.line(test_grp2,x='datetime',y=y_col_chosen,color='interaction_type', title=f"Line chart of {y_col_chosen} by date")
    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig1, fig2