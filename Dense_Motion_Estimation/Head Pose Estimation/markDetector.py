"""Human facial landmark detector based on Convolutional Neural Network"""

from cv2 import cv2
import numpy as np
import tensorflow as tf


class FaceDetector:
    """Detect human face from image"""

    def __init__(self,
                 dnnProtoText='assets/deploy.prototxt',
                 dnnModel='assets/res10_300x300_ssd_iter_140000.caffemodel'):
        """Initialization"""
        self.faceNet = cv2.dnn.readNetFromCaffe(dnnProtoText, dnnModel)
        self.detectionResult = None

    def getFaceboxes(self, image, threshold=0.5):
        """
        Get the bounding box of faces in image using dnn
        """
        rows, cols, _ = image.shape

        confidences = []
        faceboxes = []

        self.faceNet.setInput(cv2.dnn.blobFromImage(
            image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False))
        detections = self.faceNet.forward()

        for result in detections[0, 0, :, :]:
            confidence = result[2]
            if confidence > threshold:
                xLeftBottom = int(result[3] * cols)
                yLeftBottom = int(result[4] * rows)
                xRightTop = int(result[5] * cols)
                yRightTop = int(result[6] * rows)
                confidences.append(confidence)
                faceboxes.append(
                    [xLeftBottom, yLeftBottom, xRightTop, yRightTop])

        self.detectionResult = [faceboxes, confidences]

        return confidences, faceboxes

    def drawAllResult(self, image):
        """Draw the detection result on image"""
        for facebox, conf in self.detectionResult:
            cv2.rectangle(image, (facebox[0], facebox[1]),
                          (facebox[2], facebox[3]), (0, 255, 0))
            label = "face: %.4f" % conf
            labelSize, baseLine = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            cv2.rectangle(image, (facebox[0], facebox[1] - labelSize[1]),
                          (facebox[0] + labelSize[0],
                           facebox[1] + baseLine),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, label, (facebox[0], facebox[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))


class MarkDetector:
    """Facial landmark detector by Convolutional Neural Network"""

    def __init__(self, savedModel='assets/poseModel'):
        """Initialization"""
        # face detector is required for mark detection
        self.faceDetector = FaceDetector()

        self.cnnInputSize = 128
        self.marks = None

        # get a TensorFlow session ready to do landmark detection
        # load a Tensorflow saved model into memory
        self.graph = tf.Graph()
        config = tf.ConfigProto()
        # config.gpu_options.allow_growth = True
        self.sess = tf.Session(graph=self.graph, config=config)

        # restore model from the savedModel file, that is exported by TensorFlow estimator
        tf.saved_model.loader.load(self.sess, ["serve"], savedModel)

    @staticmethod
    def drawBox(image, boxes, boxColor=(255, 255, 255)):
        """Draw square boxes on image"""
        for box in boxes:
            cv2.rectangle(image,
                          (box[0], box[1]),
                          (box[2], box[3]), boxColor, 3)

    @staticmethod
    def moveBox(box, offset):
        """Move the box to direction specified by vector offset"""
        xLeft = box[0] + offset[0]
        yTop = box[1] + offset[1]
        xRight = box[2] + offset[0]
        yBottom = box[3] + offset[1]
        return [xLeft, yTop, xRight, yBottom]

    @staticmethod
    def getSquareBox(box):
        """Get a square box out of the given box, by expanding it"""
        xLeft = box[0]
        yTop = box[1]
        xRight = box[2]
        yBottom = box[3]

        boxWidth = xRight - xLeft
        boxHeight = yBottom - yTop

        # check if box is already a square. If not, make it a square
        diff = boxHeight - boxWidth
        delta = int(abs(diff) / 2)

        if diff == 0:                   # already a square
            return box
        elif diff > 0:                  # height > width, a slim box
            xLeft -= delta
            xRight += delta
            if diff % 2 == 1:
                xRight += 1
        else:                           # width > height, a short box
            yTop -= delta
            yBottom += delta
            if diff % 2 == 1:
                yBottom += 1

        # make sure box is always square
        assert ((xRight - xLeft) == (yBottom - yTop)), 'Box is not square.'

        return [xLeft, yTop, xRight, yBottom]

    @staticmethod
    def boxInImage(box, image):
        """Check if the box is in image"""
        rows = image.shape[0]
        cols = image.shape[1]
        return box[0] >= 0 and box[1] >= 0 and box[2] <= cols and box[3] <= rows

    def extractCNNFacebox(self, image):
        """Extract face area from image."""
        _, rawBoxes = self.faceDetector.getFaceboxes(
            image=image, threshold=0.9)

        for box in rawBoxes:
            # move box down
            # diffHeightWidth = (box[3] - box[1]) - (box[2] - box[0])
            yOffset = int(abs((box[3] - box[1]) * 0.1))
            boxMoved = self.moveBox(box, [0, yOffset])

            # make box square
            facebox = self.getSquareBox(boxMoved)

            if self.boxInImage(facebox, image):
                return facebox

        return None

    def detectMarks(self, imageNp):
        """Detect marks from image"""
        # get result tensor by its name
        logitsTensor = self.graph.get_tensor_by_name(
            'layer6/final_dense:0')

        # actual detection
        predictions = self.sess.run(
            logitsTensor,
            feed_dict={'image_tensor:0': imageNp})

        # convert predictions to landmarks
        marks = np.array(predictions).flatten()[:136]
        marks = np.reshape(marks, (-1, 2))

        return marks

    @staticmethod
    def drawMarks(image, marks, color=(255, 255, 255)):
        """Draw mark points on image"""
        for mark in marks:
            cv2.circle(image, (int(mark[0]), int(
                mark[1])), 1, color, -1, cv2.LINE_AA)
