"""
Lucas-Kanade sparse optical flow tracker. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.
"""

from math import sqrt
import numpy as np
import cv2


class Tracker:
    """Lucas-Kanade sparse optical flow tracker"""

    def __init__(self):
        self.trackLen = 5
        self.tracks = []
        self.lkParams = dict(winSize=(15, 15),
                             maxLevel=2,
                             criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.featureParams = dict(maxCorners=500,
                                  qualityLevel=0.3,
                                  minDistance=7,
                                  blockSize=7)

    def updateTracks(self, imgOld, imgNew):
        """Update tracks"""
        # get old points, using the latest one.
        pointsOld = np.float32([track[-1]
                                for track in self.tracks]).reshape(-1, 1, 2)

        # get new points from old points.
        pointsNew, _st, _err = cv2.calcOpticalFlowPyrLK(
            imgOld, imgNew, pointsOld, None, **self.lkParams)

        # get inferred old points from new points.
        pointsOldInferred, _st, _err = cv2.calcOpticalFlowPyrLK(
            imgNew, imgOld, pointsNew, None, **self.lkParams)

        # compare between old points and inferred old points
        errorTerm = abs(
            pointsOld - pointsOldInferred).reshape(-1, 2).max(-1)
        pointValid = errorTerm < 1

        newTracks = []
        for track, (x, y), goodFlag in zip(self.tracks, pointsNew.reshape(-1, 2), pointValid):
            # is track good?
            if not goodFlag:
                continue

            # new point is good, add to track
            track.append((x, y))

            # need to drop first old point?
            if len(track) > self.trackLen:
                del track[0]

            # track updated, add to track groups
            newTracks.append(track)

        # new track groups got, do update
        self.tracks = newTracks

    def getNewTracks(self, frame, roi):
        """Get new tracks every detectInterval frames"""
        # using mask to determine where to look for feature points
        mask = np.zeros_like(frame)
        mask[roi[0]:roi[1], roi[2]:roi[3]] = 255

        # get good feature points.
        featurePoints = cv2.goodFeaturesToTrack(
            frame, mask=mask, **self.featureParams)

        if featurePoints is not None:
            for x, y in np.float32(featurePoints).reshape(-1, 2):
                self.tracks.append([(x, y)])

    def getAverageTrackLength(self):
        """Get the average track length"""
        length = 0
        tracks = np.array(self.tracks)

        def distance(track):
            """Get distance between the first and last point"""
            delta_x = abs(track[-1][0] - track[0][0])
            delta_y = abs(track[-1][1] - track[0][1])
            return sqrt(delta_x*delta_x + delta_y*delta_y)
        for track in tracks:
            length += distance(track)
        return length / len(tracks)

    def drawTrack(self, image):
        """Draw track lines on image"""
        cv2.polylines(image, [np.int32(track)
                              for track in self.tracks], False, (0, 255, 0))


def main():
    """Test Code"""
    import sys
    try:
        videoSource = sys.argv[1]
    except:
        videoSource = 0

    tracker = Tracker()

    cam = cv2.VideoCapture(videoSource)
    detectInterval = 5
    frameIdx = 0

    prevGray = cam.read()
    while True:
        _ret, frame = cam.read()
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # update tracks
        if len(tracker.tracks) > 0:
            tracker.updateTracks(prevGray, frameGray)

        # get new tracks every detectInterval frames
        targetBox = [100, 400, 100, 400]
        if frameIdx % detectInterval == 0:
            tracker.getNewTracks(frameGray, targetBox)

        # draw tracks
        tracker.drawTrack(frame)

        frameIdx += 1
        prevGray = frameGray
        cv2.imshow('lkTrack', frame)
        ch = cv2.waitKey(1)
        if ch == 27:
            break


if __name__ == '__main__':
    main()
