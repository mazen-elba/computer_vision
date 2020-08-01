"""
Demo code shows how to estimate human head pose.
Human face is detected by a detector from an OpenCV DNN module.
Then, the face box is slightly modified to suit the need of landmark detection.
Facial landmark detection is done by a custom Convolutional Neural Network trained with TensorFlow.
Finally, head pose is estimated by solving a PnP problem.
"""

from argparse import ArgumentParser
from multiprocessing import Process, Queue

from cv2 import cv2
import numpy as np

from markDetector import MarkDetector
from osDetector import detectOS
from poseEstimator import PoseEstimator
from stabilizer import Stabilizer

print("OpenCV version: {}".format(cv2.__version__))

# multiprocessing may not work on Windows and macOS, check OS for safety
detectOS()

CNN_INPUT_SIZE = 128

# take arguments from user input
parser = ArgumentParser()
parser.add_argument("--video", type=str, default=None,
                    help="Video file to be processed.")
parser.add_argument("--cam", type=int, default=None,
                    help="The webcam index.")
args = parser.parse_args()


def getFace(detector, imgQueue, boxQueue):
    """Get face from image queue. This function is used for multiprocessing"""
    while True:
        image = imgQueue.get()
        box = detector.extractCNNFacebox(image)
        boxQueue.put(box)


def main():
    """MAIN"""
    # video source from webcam or video file
    videoSource = args.cam if args.cam is not None else args.video
    if videoSource is None:
        print("Warning: video source not assigned, default webcam will be used.")
        videoSource = 0

    cap = cv2.VideoCapture(videoSource)
    if videoSource == 0:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    _, sampleFrame = cap.read()

    # introduce markDetector to detect landmarks
    markDetector = MarkDetector()

    # setup process and queues for multiprocessing
    imgQueue = Queue()
    boxQueue = Queue()
    imgQueue.put(sampleFrame)
    boxProcess = Process(target=getFace, args=(
        markDetector, imgQueue, boxQueue,))
    boxProcess.start()

    # introduce pose estimator to solve pose
    # get one frame to setup the estimator according to the image size
    height, width = sampleFrame.shape[:2]
    poseEstimator = PoseEstimator(imgSize=(height, width))

    # introduce scalar stabilizers for pose
    poseStabilizers = [Stabilizer(
        stateNum=2,
        measureNum=1,
        covProcess=0.1,
        covMeasure=0.1) for _ in range(6)]

    tm = cv2.TickMeter()

    while True:
        # read frame, crop it, flip it, suits your needs
        frameGot, frame = cap.read()
        if frameGot is False:
            break

        # crop it if frame is larger than expected
        # frame = frame[0:480, 300:940]

        # if frame comes from webcam, flip it so it looks like a mirror
        if videoSource == 0:
            frame = cv2.flip(frame, 2)

        # Pose estimation by 3 steps:
        # 1. detect face
        # 2. detect landmarks
        # 3. estimate pose

        # feed frame to image queue
        imgQueue.put(frame)

        # get face from box queue
        facebox = boxQueue.get()

        if facebox is not None:
            # detect landmarks from image of 128x128
            faceImg = frame[facebox[1]: facebox[3],
                            facebox[0]: facebox[2]]
            faceImg = cv2.resize(faceImg, (CNN_INPUT_SIZE, CNN_INPUT_SIZE))
            faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)

            tm.start()
            marks = markDetector.detectMarks([faceImg])
            tm.stop()

            # convert the marks locations from local CNN to global image
            marks *= (facebox[2] - facebox[0])
            marks[:, 0] += facebox[0]
            marks[:, 1] += facebox[1]

            # uncomment following line to show raw marks
            # markDetector.drawMarks(frame, marks, color=(0, 255, 0))

            # uncomment following line to show facebox
            # markDetector.drawBox(frame, [facebox])

            # try pose estimation with 68 points
            pose = poseEstimator.solvePoseBy68Points(marks)

            # stabilize the pose
            steadyPose = []
            poseNp = np.array(pose).flatten()
            for value, psStb in zip(poseNp, poseStabilizers):
                psStb.update([value])
                steadyPose.append(psStb.state[0])
            steadyPose = np.reshape(steadyPose, (-1, 3))

            # uncomment following line to draw pose annotation on frame
            # poseEstimator.drawAnnotationBox(frame, pose[0], pose[1], color=(255, 128, 128))

            # uncomment following line to draw stabile pose annotation on frame
            poseEstimator.drawAnnotationBox(
                frame, steadyPose[0], steadyPose[1], color=(128, 255, 128))

            # uncomment following line to draw head axes on frame
            # poseEstimator.drawAxes(frame, stabile_pose[0], stabile_pose[1])

        # Show preview.
        cv2.imshow("Preview", frame)
        if cv2.waitKey(10) == 27:
            break

    # Clean up the multiprocessing process.
    boxProcess.terminate()
    boxProcess.join()


if __name__ == '__main__':
    main()
