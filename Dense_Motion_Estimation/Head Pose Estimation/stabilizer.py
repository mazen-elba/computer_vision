"""
    Using Kalman Filter as a point stabilizer to stabilize a 2D point
"""

import numpy as np
import cv2


class Stabilizer:
    """Using Kalman filter as a point stabillizer."""

    def __init__(self,
                 stateNum=4,
                 measureNum=2,
                 covProcess=0.0001,
                 covMeasure=0.1):
        """Initialization"""
        # currently, only supports scalar and point, so check user input first
        assert stateNum == 4 or stateNum == 2, "only scalar and point supported, check stateNum please."

        # store the parameters
        self.stateNum = stateNum
        self.measureNum = measureNum

        # Kalman filter
        self.filter = cv2.KalmanFilter(stateNum, measureNum, 0)

        # store the state
        self.state = np.zeros((stateNum, 1), dtype=np.float32)

        # store the measurement result
        self.measurement = np.array((measureNum, 1), np.float32)

        # store the prediction
        self.prediction = np.zeros((stateNum, 1), np.float32)

        # Kalman parameters setup for scalar
        if self.measureNum == 1:
            self.filter.transitionMatrix = np.array([[1, 1],
                                                     [0, 1]], np.float32)

            self.filter.measurementMatrix = np.array([[1, 1]], np.float32)

            self.filter.processNoiseCov = np.array([[1, 0],
                                                    [0, 1]], np.float32) * covProcess

            self.filter.measurementNoiseCov = np.array(
                [[1]], np.float32) * covMeasure

        # Kalman parameters setup for point
        if self.measureNum == 2:
            self.filter.transitionMatrix = np.array([[1, 0, 1, 0],
                                                     [0, 1, 0, 1],
                                                     [0, 0, 1, 0],
                                                     [0, 0, 0, 1]], np.float32)

            self.filter.measurementMatrix = np.array([[1, 0, 0, 0],
                                                      [0, 1, 0, 0]], np.float32)

            self.filter.processNoiseCov = np.array([[1, 0, 0, 0],
                                                    [0, 1, 0, 0],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]], np.float32) * covProcess

            self.filter.measurementNoiseCov = np.array([[1, 0],
                                                        [0, 1]], np.float32) * covMeasure

    def update(self, measurement):
        """Update the filter"""
        # make Kalman prediction
        self.prediction = self.filter.predict()

        # get new measurement
        if self.measureNum == 1:
            self.measurement = np.array([[np.float32(measurement[0])]])
        else:
            self.measurement = np.array([[np.float32(measurement[0])],
                                         [np.float32(measurement[1])]])

        # correct according to measurement
        self.filter.correct(self.measurement)

        # update state value
        self.state = self.filter.statePost

    def setQR(self, covProcess=0.1, covMeasure=0.001):
        """Set new value for processNoiseCov and measurementNoiceCov"""
        if self.measureNum == 1:
            self.filter.processNoiseCov = np.array([[1, 0],
                                                    [0, 1]], np.float32) * covProcess

            self.filter.measurementNoiseCov = np.array(
                [[1]], np.float32) * covMeasure
        else:
            self.filter.processNoiseCov = np.array([[1, 0, 0, 0],
                                                    [0, 1, 0, 0],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]], np.float32) * covProcess

            self.filter.measurementNoiseCov = np.array([[1, 0],
                                                        [0, 1]], np.float32) * covMeasure


def main():
    """Test code"""
    global mp

    # measurement
    mp = np.array((2, 1), np.float32)

    def onMouse(k, x, y, s, p):
        global mp
        mp = np.array([[np.float32(x)], [np.float32(y)]])

    cv2.namedWindow("kalman")
    cv2.setMouseCallback("kalman", onMouse)
    kalman = Stabilizer(4, 2)

    # drawing canvas
    frame = np.zeros((480, 640, 3), np.uint8)

    while True:
        kalman.update(mp)
        point = kalman.prediction
        state = kalman.filter.statePost
        cv2.circle(frame, (state[0], state[1]), 2, (255, 0, 0), -1)
        cv2.circle(frame, (point[0], point[1]), 2, (0, 255, 0), -1)
        cv2.imshow("kalman", frame)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break


if __name__ == "__main__":
    main()
