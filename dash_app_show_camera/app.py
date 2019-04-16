import camera 
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly
from collections import deque

from flask import Flask, Response
import pandas as pd 
import datetime

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(camera.gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    html.Div([
        html.H1("Webcam Test"),
        html.Img(
            src="/video_feed"
         ),
    ]),
    html.Div([
        dcc.Graph(
            id='live-update-graph', 
            animate=True,
            style={
                'height': 800
            },
        ),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
        )
    ])
])

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')]
)
def update_graph_scatter(count):
    data_list = []
    data_time = []
    count = []
    data_size = []
    record = []
    with open("data.txt") as f :
        for line in f :
            data_list.append([str(n) for n in line.strip().split(',')])
    
    for d in data_list:
        record.append(d[0])
        data_time.append(d[1])
        count.append(d[2])
        data_size.append(d[3])

    count_line = go.Scatter(
            x=data_time,
            y=count,
            name='Count',
            line = dict(color = '#FF9933'),
            opacity = 0.8
    )
    size_line = go.Scatter(
            x=data_time,
            y=data_size,
            name='Size',
            yaxis='y2',    
            line = dict(color = '#3399FF'),
            opacity = 0.8
    )
    data = [count_line,size_line]
    layout = go.Layout(
        title='Graph Relation Number of Floc, Average Size of Floc and Time ',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=60,
                        label='60s',
                        step='second',
                        stepmode='backward'),
                    dict(count=120,
                        label='120s',
                        step='second',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True
            ),
            autorange = True,
            type='date'
        ),
        yaxis=dict(
            title='Number of Floc (unit)',
            titlefont=dict(
                color='rgb(51, 153, 255)'
            ),
            tickfont=dict(
                color='rgb(51, 153, 255)'
            ),
        ),
        yaxis2=dict(
            title='Average Size of Floc (px)',
            titlefont=dict(
                color='rgb(255, 153, 51)'
            ),
            tickfont=dict(
                color='rgb(255, 153, 51)'
            ),
            overlaying='y',
            side='right',
        ),
        autosize=True
    )
    return {
        'data': data,
        'layout': layout
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)