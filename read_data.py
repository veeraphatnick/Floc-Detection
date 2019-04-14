from dash.dependencies import Output, Input
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go

import cv2 
import numpy as np
import datetime
import pandas as pd
import math
import time
import plotly.plotly as py
import plotly.graph_objs as go
import app
import matplotlib.pyplot as plt

def edge_floc(cnt, count):
    cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
    
def ractangle_floc(cnt, count):
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 3000:
        count = count +1
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #print(area)
    return count

def nothing(x):
    pass

#cap = cv2.VideoCapture('Example3.mp4')
cap = cv2.VideoCapture(0)

data_time = []
data_count = []
start_datetime = datetime.datetime.now().strftime("%H"+"%M"+"%S")
start_time = time.time()
start = math.floor(start_time)

while True:
    ret, frame = cap.read()
    count = 0
    if ret is False:
        break

    roi = frame[:, :]
    rows, cols, _ = roi.shape
    date_time = datetime.datetime.now()

    # Convert BGR to Gray and Filtering
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    # Threshloding
    th = cv2.getTrackbarPos('Threshlod','Threshold')
    #_, threshold = cv2.threshold(gray_roi,th,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #_, threshold = cv2.threshold(gray_roi,th,255,cv2.THRESH_BINARY_INV)
    #_, threshold = cv2.threshold(gray_roi,127,255,cv2.THRESH_BINARY)
    _, threshold = cv2.threshold(gray_roi,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Find Contours
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    # Drew Contours+
    for cnt in contours:
        count = ractangle_floc(cnt, count)

    elapsed_time = int(time.time() - start_time)

    current = math.floor(time.time())
    if (current != start):
        # Add data time and count in Data table
        data_count.append(int(count))
        data_time.append(date_time.strftime("%X"))
        start = current

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()


app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div(className='container-fluid',children=
[
	html.Div(className='row', children=html.Div(dcc.Graph(id='live-graph', animate=True), className='col s12 m12 l12')),
	dcc.Interval(
		id='graph-update',
		interval=5000,
        n_intervals=0
	)
]),
)

@app.callback(
    Output('live-graph','figure'),
    [Input('graph-update','n_intervals')]
)
def graph_update(i):
    return {
        'data':[{
            'x':data_time,
            'y':data_count,
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

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

server = app.server
dev_server = app.run_server(debug=True)