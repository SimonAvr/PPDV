import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
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


app = dash.Dash(__name__)
app.title = 'PPDV Project'

#Set up screen application layout
app.layout = html.Div(

    # first row
    html.Div(children=[

        # first column of first row
        html.Div(children=[
            dcc.Graph(id='graph_1', animate=True),
            dcc.Graph(id='graph_2', animate=True),
            dcc.Interval(id='interval-component', interval=1*1000)
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '60%'}),

        # second column of first row
        html.Div(children=[
            dcc.Graph(id='radar'),
        ], style={'display': 'inline-block', 'width': '40%'}),
    ])
)


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