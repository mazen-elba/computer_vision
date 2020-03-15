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
argParse.add_argument("-i", "--image", required=True,
                      help="path to input image")
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

# Initialize legend visualization
legend = np.zeros(((len(CLASSES) * 25) + 25, 300, 3), dtype="uint8")

# Loop over class names & colors
for i, (className, color) in enumerate(zip(CLASSES, COLORS)):
    # draw class name & color on legend
    color = [int(c) for c in color]
    cv2.putText(legend, className, (5, (i * 25) + 17),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.rectangle(legend, (100, (i * 25)),
                  (300, (i * 25) + 25), tuple(color), -1)

# Load serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNet(args["model"])

# Load input image, resize it, and construct a blob from it
# ... note - original input image dimensions (here, 1024x512)
image = cv2.imread(args["image"])
image = imutils.resize(image, width=args["width"])
blob = cv2.dnn.blobFromImage(
    image, 1/255.0, (1024, 512), 0, swapRB=True, crop=False)

# Perform forward pass using segmentation model
net.setInput(blob)
start = time.time()
output = net.forward()
end = time.time()

# Show amount of time inference took
print("[INFO] inference took {:.4f} seconds".format(end - start))

# Infer total number of classes with spatial dimensions of mask image via shape of output array
(numClasses, height, width) = output.shape[1:4]

# Find class label with largest probability for each (x, y)-coordinate in image
# ... note - output class ID map is num_classes x height x wisth in size
classMap = np.argmax(output[0], axis=0)

# Map each class ID to its corresponding color
mask = COLORS[classMap]

# Resize mask & class map (for dimensions to match original size of input)
mask = cv2.resize(
    mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
classMap = cv2.resize(
    classMap, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

# Loop over each individual class IDs in image
for classID in np.unique(classMap):
    # build binary mask for current class
    # ... then use mask to visualize all pixels in image belonging to class
    print("[INFO] class: {}".format(CLASSES[classID]))
    classMask = (mask == COLORS[classID]).astype("uint8") * 255
    classMask = classMask[:, :, 0]
    classOutput = cv2.bitwise_and(image, image, mask=classMask)
    classMask = np.hstack([image, classOutput])

    # show output class visualization
    cv2.imshow("Class Vis", classMask)
    cv2.waitKey(0)

# Perform weighted combination of input image with mask (to form output visualizetion)
output = ((0.4 * image) + (0.6 * mask)).astype("uint8")

# Show input & output images
cv2.imshow("Legend", legend)
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)
