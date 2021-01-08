import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from random import random
import plotly
import urllib
import json
import requests

from utils import getTrace

import plotly.graph_objs as go
url1 = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/1'
foot = ['left foot front', 'left foot middle', 'left foot back',
        'right foot front', 'right foot middle', 'right foot back']
x = []
y = []

external_stylesheets = [dbc.themes.FLATLY,dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'PPDV Project'

nav_menu= dbc.NavbarSimple(
    #brand=html.H2("Python programming and data visualisation"),
    brand_href="#",
    color="primary",
    dark=True,

    children=[
        html.H2(dbc.NavItem(dbc.NavLink("Python programming and data visualisation", href="#", active = True))),
        html.H2(dbc.NavItem(dbc.NavLink("Pacjent 1", href="#", active = True))),
        html.H2(dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Pacjent 1", header=True),
                dbc.DropdownMenuItem("Pacjent 2", href="/page-a"),
                dbc.DropdownMenuItem("Pacjent 3", href="/page-b"),
            ],
            nav=True,
            in_navbar=True,
            label="List",
        )),
    ],
    
)

# Card with basic info 

first_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Alert([
            html.H5("Info", className="card-title"),
            html.H6("Name: Albert Lisowski"),
            html.H6("Birthdate: 1991"),
            ] ,color="primary")
        ]
    )
)

second_card = dbc.Card(
    dbc.CardBody(
        [   
            dbc.Alert([
            html.H5("Active" ),
            html.H6("Last active: now"),
            html.H6("Time Active: 1h 12m"),
            ] ,color="info")
        ]
    )
)

third_card = dbc.Card(
    dbc.CardBody(
        [   
            dbc.Alert([
            html.H5("Speed"),
            html.H6("Presure power: 80%"),
            html.H6("Walk speed: 53%"),
            ] ,color="info")
        ]
    )
)

four_card = dbc.Card(
    dbc.CardBody(
        [   
            dbc.Alert([
            html.H5("Rest"),
            html.H6("Active: 8h 23 min"),
            html.H6("No active: 16h 12m"),
            ] ,color="info")
        ]
    )
)

five_card = dbc.Card(
    dbc.CardBody(
        [   
            dbc.Alert([
            html.H5("Anomaly per feet"),
            html.H6("Left: 20 %"),
            html.H6("Right: 80 %"),
            ] ,color="danger")
        ]
    )
)

six_card = dbc.Card(
    dbc.CardBody(
        [   
            dbc.Alert([
            html.H5("Anomaly Status"),
            html.H6("Status: 20 min ago"),
            html.H6("Average time: per 1h"),
            ] ,color="danger")
        ]
    )
)

#Set up screen application layout
app.layout = html.Div([

    nav_menu,


    # first row
    html.Div([
        
        # Head
  
        dbc.Row([dbc.Col(first_card, width=2), dbc.Col(second_card, width=2),dbc.Col(third_card, width=2),dbc.Col(four_card, width=2),dbc.Col(five_card, width=2),dbc.Col(six_card, width=2)]),
        

        # Body
        dbc.Row([
            # first column of first row
            html.Div(children=[
                dcc.Graph(id='graph_1', animate=True),
                dcc.Graph(id='graph_2', animate=True),
                dcc.Interval(id='interval-component', interval=1*1000)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '59%', 'margin-left': '1%'}),

            # second column of first row
            html.Div(children=[
                dcc.Graph(id='radar'),
                dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Left feet'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'RIght feet'},
                    ],
                    'layout': {
                        'title': 'Anomaly Data Visualization'
                    }
                }
            ),
            ], style={'display': 'inline-block', 'width': '39%', 'margin-right': '1%'}),

        ]),

    ])
])


@app.callback([Output('graph_1', 'figure'), Output('graph_2', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_graph_scatter(self):

    # Get data
    data = requests.get(url1)
    r = data.json()
    y.append(getTrace(r))
    x.append(len(x))

    # Set up x layout for graphs
    layout = go.Layout(xaxis=dict(
        range=[min(x), max(x)]), yaxis=dict(range=[0, 1200]))

    # Left foot graph
    leftFoot = go.Figure(layout=layout)
    for i in range(3):
        leftFoot.add_trace(go.Scatter(
            x=x,
            y=[item[i] for item in y],
            name=foot[i]
        ))
    leftFoot.update_layout(title="Left foot", xaxis_title="Second",
                           yaxis_title="Measurements of pressure of feet")

    # Right foot graph
    rightFoot = go.Figure(layout=layout)
    for i in range(3, 6):
        rightFoot.add_trace(go.Scatter(
            x=x,
            y=[item[i] for item in y],
            name=foot[i]
        ))
    rightFoot.update_layout(title="Right foot", xaxis_title="Second",
                            yaxis_title="Measurements of pressure of feet")

    return [leftFoot, rightFoot]

# Radar chart 
@app.callback(Output('radar', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_bar(self):

    data = requests.get(url1)
    r = data.json()

    # Create graph plot
    radar = go.Figure(data=go.Scatterpolar(
        r=getTrace(r),
        theta=foot,
        fill='toself',

    ))

    return radar


if __name__ == '__main__':
    app.run_server(debug=True)