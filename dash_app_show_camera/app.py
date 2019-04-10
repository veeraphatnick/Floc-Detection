import camera 
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(camera.gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    html.Div([
        dcc.Input(id='my-id', value='initial value', type='text'),
        html.Div(id='my-div')
    ]),
    html.Div([
        html.H1("Webcam Test"),
        html.Img(src="/video_feed"),
    ])
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')],
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
        
if __name__ == '__main__':
    app.run_server(debug=True)