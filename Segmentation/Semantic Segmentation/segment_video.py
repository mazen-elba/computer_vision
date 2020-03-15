#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dependencies
import numpy as np
import argparse
import imutils
import time
import cv2

# Construct argument parse & parse arguments
argParse = argparse.ArgumentParser()
argParse.add_argument("-m", "--model", required=True,
                      help="path to deep learning segmentation model")
argParse.add_argument("-c", "--classes", required=True,
                      help="path to .txt file containing class labels")
argParse.add_argument("-v", "--video", required=True,
                      help="path to input video file")
argParse.add_argument("-o", "--output", required=True,
                      help="path to output video file")
argParse.add_argument("-s", "--show", type=int, default=1,
                      help="whether or not to display frame to screen")
argParse.add_argument("-l", "--colors", type=str,
                      help="path to .txt file containing colors for labels")
argParse.add_argument("-w", "--width", type=int, default=500,
                      help="desired width (in pixels) of input image")

args = vars(argParse.parse_args())

# Load class label names
CLASSES = open(args["classes"]).read().strip().split("\n")

# Load color file from disk if it was supplied
if args["colors"]:
    COLORS = open(args["colors"]).read().strip().split("\n")
    COLORS = [np.array(c.split(",")).astype("int") for c in COLORS]
    COLORS = np.array(COLORS, dtype="uint8")
# Otherwise, randomly generate RGB colors for each class label
else:
    # initialize list of colors torepresent each class label in the mask
    # ... starting with "black" for background/unlabeled regions
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(CLASSES)-1, 3), dtype="uint8")
    COLORS = np.vstack([[0, 0, 0], COLORS]).astype("uint8")

# Load serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNet(args["model"])

# Initialize video stream & pointer to output video file
vs = cv2.VideoCapture(args["video"])
writer = None

# Try to determine total number of frames in video file
try:
    prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() else cv2.CAP_PROP_FRAME_COUNT
except:
    print("[INFO] could not determine # of frames in video")
    total = -1

# Loop over frames from video file stream
while True:
    # read next frame from file
    (grabbed, frame) = vs.read()

    # if frmae was not grabbed, we have reached end of stream
    if not grabbed:
        break

    # construct a blob from frame & perform forward pass
    frame = imutils.resize(frame, width=args["width"])
    blob = cv2.dnn.blobFromImage(
        frame, 1/255.0, (1024, 512), 0, swapRB=True, crop=False)

    # Perform forward pass using segmentation model
    net.setInput(blob)
    start = time.time()
    output = net.forward()
    end = time.time()

    # Infer total number of classes with spatial dimensions of mask image via shape of output array
    (numClasses, height, width) = output.shape[1:4]

    # Find class label with largest probability for each (x, y)-coordinate in image
    # ... note - output class ID map is num_classes x height x wisth in size
    classMap = np.argmax(output[0], axis=0)

    # Map each class ID to its corresponding color
    mask = COLORS[classMap]

    # Resize mask & class map (for dimensions to match original size of input)
    mask = cv2.resize(
        mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Perform weighted combination of input frame with mask (to form output visualizetion)
    output = ((0.3 * frame) + (0.7 * mask)).astype("uint8")

    # check if video writer is None
    if writer is None:
        # initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(
            args["output"], fourcc, 30, (output.shape[1], output.shape[0]), True)

        # processing single frames
        if total > 0:
            elap = (end - start)
            print("[INFO] single frame {:.4f} seconds".format(elap))
            print("[INFO] estimated total time: {:.4f}".format(elap * total))

    # write output frame to disk
    writer.write(output)

    # check if need to display output frame to screen
    if args["show"] > 0:
        cv2.imshow("Frame", output)
        key = cv2.waitKey(1) & 0xFF

        # if "q" key is pressed, break from loop
        if key == ord("q"):
            break

# Release file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
