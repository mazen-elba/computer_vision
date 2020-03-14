#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dependencies
from imutils.video import VideoStream
from imutils.video import FPS  # motion from camera
from urllib.request import urlopen  # motion from webcam

import sys
import numpy as np
import argparse
import imutils
import time
import cv2

host = "http://192.168.0.101:8080"
url = host + "shot.jpg"

# Construct argument parse & parse arguments
argParse = argparse.ArgumentParser()
argParse.add_argument("-p", "--prototxt", required=True,
                      help="path to Caffe 'deploy' prototxt file")
argParse.add_argument("-m", "--model", required=True,
                      help="path to Caffe pre-trained model")
argParse.add_argument("-c", "--confidence", type=float, default=0.2,
                      help="minimum probability to filter weak detections")

args = vars(argParse.parse_args())

# Initialize list of class labels MobileNet SSD trained to detect
# ... generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES, 3)))

# Load serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Initialize video stream (allow camera sensor to warmup)
# ... or initialize FPS counter
print("[INFO] starting video stream...")

if args["source"] == "webcam":
    vs = cv2.VideoCapture(0)

vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# Loop over frames from video stream
while True:
    # grab frame from threaded video stream & resize it with max width of 400 pixels
    if args["source"] == "webcam":
        ret, frame = vs.read()
    else:
        imgResp = urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)

    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # grab frame dimensions & convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(
        frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass blob through network & obtain detections and predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over detections
    for i in np.arange(0, detections.shape[2]):
        # extract confidence (ie; probability) associated with prediction
        confidence = detections[0, 0, i, 2]

        # filter-out weak detections (by ensuring confidence > minimum confidence)
        if confidence > args["confidence"]:
            # extract index of class label from detections
            # ... compute (x, y)-coordinates of bounding box for object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw prediction on frame
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(frame, (startX, startY),
                          (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # break the loop if "q" key was pressed
    if key == ord("q"):
        break

    # update FPS counter
    fps.update()

# Stop timers & display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approximate time: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()
vs.stop()
