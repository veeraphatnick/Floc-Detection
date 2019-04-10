import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

from flask import Flask, Response
import cv2
import detection
import numpy as np
class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image, threshold = detection.detection(success,image)
        ret, jpeg = cv2.imencode('.jpg',image)
        ret2, jpeg2 = cv2.imencode('.jpg',threshold)
        return jpeg.tobytes(), jpeg2.tobytes()

def gen(camera):
    
    while True:
        frame, threshold = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



