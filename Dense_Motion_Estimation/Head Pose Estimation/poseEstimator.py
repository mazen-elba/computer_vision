"""Estimate head pose according to the facial landmarks"""
import cv2
import numpy as np


class PoseEstimator:
    """Estimate head pose according to the facial landmarks"""

    def __init__(self, imgSize=(480, 640)):
        self.size = imgSize

        # 3D model points
        self.modelPoints = np.array([
            (0.0, 0.0, 0.0),             # nose tip
            (0.0, -330.0, -65.0),        # chin
            (-225.0, 170.0, -135.0),     # left eye left corner
            (225.0, 170.0, -135.0),      # right eye right corner
            (-150.0, -150.0, -125.0),    # mouth left corner
            (150.0, -150.0, -125.0)      # mouth right corner
        ]) / 4.5

        self.modelPoints68 = self._getFullModelPoints()

        # camera internals
        self.focalLength = self.size[1]
        self.cameraCenter = (self.size[1] / 2, self.size[0] / 2)
        self.cameraMatrix = np.array(
            [[self.focalLength, 0, self.cameraCenter[0]],
             [0, self.focalLength, self.cameraCenter[1]],
             [0, 0, 1]], dtype="double")

        # assuming no lens distortion
        self.distCoeefs = np.zeros((4, 1))

        # rotation vector and translation vector
        self.rotVec = np.array([[0.01891013], [0.08560084], [-3.14392813]])
        self.transVec = np.array(
            [[-14.97821226], [-10.62040383], [-2053.03596872]])
        # self.rotVec = None
        # self.transVec = None

    def _getFullModelPoints(self, filename='assets/model.txt'):
        """Get all 68 3D model points from file"""
        rawValue = []
        with open(filename) as file:
            for line in file:
                rawValue.append(line)
        modelPoints = np.array(rawValue, dtype=np.float32)
        modelPoints = np.reshape(modelPoints, (3, -1)).T

        # transform the model into a front view
        modelPoints[:, 2] *= -1

        return modelPoints

    def show3dModel(self):
        from matplotlib import pyplot
        from mpl_toolkits.mplot3d import Axes3D
        fig = pyplot.figure()
        ax = Axes3D(fig)

        x = self.modelPoints68[:, 0]
        y = self.modelPoints68[:, 1]
        z = self.modelPoints68[:, 2]

        ax.scatter(x, y, z)
        ax.axis("square")
        pyplot.xlabel("x")
        pyplot.ylabel("y")
        pyplot.show()

    def solvePose(self, imagePoints):
        """
        Solve pose from image points
        Return (rotation vector, translation vector) as pose
        """
        assert imagePoints.shape[0] == self.modelPoints68.shape[0], "3D points and 2D points should be of same number"
        (_, rotationVector, translationVector) = cv2.solvePnP(
            self.modelPoints, imagePoints, self.cameraMatrix, self.distCoeefs)

        # (success, rotationVector, translationVector) = cv2.solvePnP(
        #     self.modelPoints,
        #     imagePoints,
        #     self.cameraMatrix,
        #     self.distCoeefs,
        #     rvec=self.rotVec,
        #     tvec=self.transVec,
        #     useExtrinsicGuess=True)
        return (rotationVector, translationVector)

    def solvePoseBy68Points(self, imagePoints):
        """
        Solve pose from all the 68 image points
        Return (rotationVector, translationVector) as pose
        """

        if self.rotVec is None:
            (_, rotationVector, translationVector) = cv2.solvePnP(
                self.modelPoints68, imagePoints, self.cameraMatrix, self.distCoeefs)
            self.rotVec = rotationVector
            self.transVec = translationVector

        (_, rotationVector, translationVector) = cv2.solvePnP(
            self.modelPoints68,
            imagePoints,
            self.cameraMatrix,
            self.distCoeefs,
            rvec=self.rotVec,
            tvec=self.transVec,
            useExtrinsicGuess=True)

        return (rotationVector, translationVector)

    def drawAnnotationBox(self, image, rotationVector, translationVector, color=(255, 255, 255), lineWidth=2):
        """Draw a 3D box as annotation of pose"""
        point3d = []
        rearSize = 75
        rearDepth = 0
        point3d.append((-rearSize, -rearSize, rearDepth))
        point3d.append((-rearSize, rearSize, rearDepth))
        point3d.append((rearSize, rearSize, rearDepth))
        point3d.append((rearSize, -rearSize, rearDepth))
        point3d.append((-rearSize, -rearSize, rearDepth))

        frontSize = 100
        frontDepth = 100
        point3d.append((-frontSize, -frontSize, frontDepth))
        point3d.append((-frontSize, frontSize, frontDepth))
        point3d.append((frontSize, frontSize, frontDepth))
        point3d.append((frontSize, -frontSize, frontDepth))
        point3d.append((-frontSize, -frontSize, frontDepth))
        point3d = np.array(point3d, dtype=np.float).reshape(-1, 3)

        # map to 2d image points
        (point2d, _) = cv2.projectPoints(point3d,
                                         rotationVector,
                                         translationVector,
                                         self.cameraMatrix,
                                         self.distCoeefs)
        point2d = np.int32(point2d.reshape(-1, 2))

        # draw all the lines
        cv2.polylines(image, [point2d], True, color, lineWidth, cv2.LINE_AA)
        cv2.line(image, tuple(point2d[1]), tuple(
            point2d[6]), color, lineWidth, cv2.LINE_AA)
        cv2.line(image, tuple(point2d[2]), tuple(
            point2d[7]), color, lineWidth, cv2.LINE_AA)
        cv2.line(image, tuple(point2d[3]), tuple(
            point2d[8]), color, lineWidth, cv2.LINE_AA)

    def drawAxis(self, img, R, t):
        points = np.float32(
            [[30, 0, 0], [0, 30, 0], [0, 0, 30], [0, 0, 0]]).reshape(-1, 3)

        axisPoints, _ = cv2.projectPoints(
            points, R, t, self.cameraMatrix, self.distCoeefs)

        img = cv2.line(img, tuple(axisPoints[3].ravel()), tuple(
            axisPoints[0].ravel()), (255, 0, 0), 3)
        img = cv2.line(img, tuple(axisPoints[3].ravel()), tuple(
            axisPoints[1].ravel()), (0, 255, 0), 3)
        img = cv2.line(img, tuple(axisPoints[3].ravel()), tuple(
            axisPoints[2].ravel()), (0, 0, 255), 3)

    def drawAxes(self, img, R, t):
        img = cv2.drawFrameAxes(img, self.cameraMatrix,
                                self.distCoeefs, R, t, 30)

    def getPoseMarks(self, marks):
        """Get marks ready for pose estimation from 68 marks"""
        poseMarks = []
        poseMarks.append(marks[30])    # nose tip
        poseMarks.append(marks[8])     # chin
        poseMarks.append(marks[36])    # left eye left corner
        poseMarks.append(marks[45])    # right eye right corner
        poseMarks.append(marks[48])    # mouth left corner
        poseMarks.append(marks[54])    # mouth right corner
        return poseMarks
