import camera 
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response
import pandas as pd 



server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(camera.gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    html.Div([
        html.H1("Webcam Test"),
        html.Img(src="/video_feed"),
    ]),
    
    html.Div([
        dcc.Graph(id='live-update-graph', animate=True),
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
    with open("data.txt") as f :
        for line in f :
            data_list.append([str(n) for n in line.strip().split(',')])
    for d in data_list:
        data_time.append(d[0])
        count.append(d[1])
    
    return {
        'data':[{
            'x':data_time,
            'y':count,
            'line':{
                'width':3,
            }
        }],
        'layout':{
            'margin':{
                'l':30,
                'r':20,
                'b':30,
                't':20
            }
        }
    }
        
if __name__ == '__main__':
    app.run_server(debug=True)