import cv2 
import numpy as np
import datetime
import pandas as pd
import math
import time
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style



def ractangle_floc(cnt, count):
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 3000:
        count = count +1
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #print(area)
    return count

cap = cv2.VideoCapture(0)

data_time = []
data_num = []
start_datetime = datetime.datetime.now().strftime("%H"+"%M"+"%S")
start_time = time.time()
start = math.floor(start_time)


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


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
        dt = date_time.strftime("%X")
        f = open("data.txt", "a")
        f.write(str(count)+","+str(dt)+'\n')
        f.close()
        #data_time.append(int(count))
        #data_num.append(int(count))
        
        start = current
    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    #cv2.imshow("Threshold", threshold)
    #cv2.imshow("Roi", roi)
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()