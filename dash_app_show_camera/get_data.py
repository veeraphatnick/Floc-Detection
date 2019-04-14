import cv2 
import numpy as np
import datetime
import pandas as pd
import math
import time
import plotly.plotly as py
import plotly.graph_objs as go

def ractangle_floc(roi, cnt, count):
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 3000:
        count = count +1
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #print(area)
    return count

def get_Data():
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.127")

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
        #_, threshold = cv2.threshold(gray_roi,th,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #_, threshold = cv2.threshold(gray_roi,th,255,cv2.THRESH_BINARY_INV)
        #_, threshold = cv2.threshold(gray_roi,127,255,cv2.THRESH_BINARY)
        _, threshold = cv2.threshold(gray_roi,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Find Contours
        _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # Drew Contours
        for cnt in contours:
            count = ractangle_floc(roi, cnt, count)

        elapsed_time = int(time.time() - start_time)

        current = math.floor(time.time())
        if (current != start):
            # Add data time and count in Data table
            data_time = date_time.strftime("%X")
            
            start = current

            return count, data_time

        cv2.imshow('image',roi)

    cap.release()
