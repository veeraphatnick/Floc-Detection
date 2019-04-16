import cv2 
import numpy as np
import datetime
import pandas as pd
import math
import time
import plotly.plotly as py
import plotly.graph_objs as go
import csv
import os

def edge_floc(roi, cnt, count):
    cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)

def ractangle_floc(roi, cnt, count):
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 3000:
        count = count +1
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return count

def circle_floc(roi, cnt, count, floc_size):
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    area = math.pi*radius**2
    if area < 3000:
        count = count+1
        cv2.circle(roi,center,radius,(0,0,255),2)
        floc_size += area
    
    return count, floc_size

def nothing(x):
    pass

def detection(ret,frame):
    count = 0
    record = 0
    floc_size = 0 
    roi = frame
    rows, cols, _ = roi.shape
    
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
    '''
    histogram = cv2.calcHist([gray_roi], [0], None, [256], [0, 255]) 
    histogram = np.array(histogram)

    df = pd.DataFrame(data=histogram[:,0:1],columns=['histogram'])
    df.to_csv('histogram.csv')
    '''

    # Drew Contours
    for cnt in contours:
        count,floc_size = circle_floc(roi, cnt, count, floc_size)

    if(count != 0):
        avg_floc_size = floc_size/count
    else:
        avg_floc_size = 0

    date_time = datetime.datetime.now()

    #time_t = date_time.strftime("%X")
    time_t = date_time
    time_t = str(time_t).split('.')
    
    if (os.stat('data.txt').st_size == 0):
        record += 1
        with open('data.txt', 'a') as textFile_w:
            textFile_w.write(str(record))
            textFile_w.write(','+str(time_t[0]))
            textFile_w.write(','+str(count))
            textFile_w.write(','+str(int(avg_floc_size))+'\n')
    else :
        with open('data.txt', 'r') as textFile:
            lines = textFile.read().splitlines()
            last_line = lines[-1].split(',')
            record = int(last_line[0])+1
            last_line = last_line[1].split('.')
            if(str(last_line[0]) != str(time_t[0])):
                with open('data.txt', 'a') as textFile_w:
                    textFile_w.write(str(record))
                    textFile_w.write(','+str(time_t[0]))
                    textFile_w.write(','+str(count))
                    textFile_w.write(','+str(int(avg_floc_size))+'\n')
                textFile_w.close()
        textFile.close()
    
    



    return roi, threshold