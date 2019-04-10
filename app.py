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

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

def ractangle_floc(cnt, count):
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 3000:
        count = count +1
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return count

if __name__ == '__main__':
    app.run_server(debug=True)
    cap = cv2.VideoCapture(0)
    
    data = []
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
            data.append([date_time.strftime("%X"),int(count)])
            start = current
            #print(date_time.strftime("%X"))
            

        # Show Text on Display
        cv2.putText(roi,'Number of Floc : ' + str(count) + ', Time ' + str(elapsed_time),
            (10,20),                  # bottomLeftCornerOfText
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.5,                      # fontScale
            (0,0,0),                  # fontColor
            1)                        # lineType
        cv2.putText(roi,' Date Time : ' + str(date_time.strftime("%H"+":"+"%M"+":"+"%S")),
            (290,20),                 # bottomLeftCornerOfText
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.5,                      # fontScale
            (0,0,0),                  # fontColor
            1)                        # lineType

        cv2.imshow("Threshold", threshold)
        cv2.imshow("Roi", roi)
        key = cv2.waitKey(30)
        if key == 27:
            break

    #data = np.array(data)

    #df = pd.DataFrame(data=data[:,0:2],columns=['Time','Number_of_Floc'])

    #print(df)

    cap.release()
    cv2.destroyAllWindows()