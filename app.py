import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import datetime
import pandas as pd
import math
import time
import cv2
import pandas as pd


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-update-graph', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
            )
    ]
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')]
)
def update_graph_scatter(count):

    X.append(X[-1]+1)
    Y.append(count)
    
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode='lines+markers'
            )

    return {
        'data': [data],
        'layout' : go.Layout(
            xaxis=dict(
                range=[min(X),max(X)]),
            yaxis=dict(
                range=[min(Y),max(Y)]),)}
    

if __name__ == '__main__':
    app.run_server(debug=True)
    