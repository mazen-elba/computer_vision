from __future__ import print_function

# Dependencies
import cv2
import numpy as np

# Set constants
MAX_MATCHES = 500
GOOD_MATCH_PERCENT = 0.15

# Alignment function


def alignImages(im1, im2):

    # convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # detect ORB features & compute descriptors
    orb = cv2.ORB_create(MAX_MATCHES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # match features
    matcher = cv2.DescriptorMatcher_create(
        cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # draw top matches
    imMatches = cv2.drawMatches(
        im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    # extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

        # find homography
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # use homography
        height, width, channels = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))

        return im1Reg, h


# Driver function
if __name__ == "__main__":

    # read reference image
    refFilename = "form.jpg"
    print("Reading reference image : ", refFilename)
    imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

    # read image to be aligned
    imFilename = "scanned-page.jpg"
    print("Reading image to align : ", imFilename)
    im = cv2.imread(imFilename, cv2.IMREAD_COLOR)

    print("Aligning images ...")

    # registered image will be restored in imReg
    # estimated homography will be stored in h
    imReg, h = alignImages(im, imReference)

    # write aligned image to disk
    outFilename = "aligned.jpg"
    print("Saving aligned image : ", outFilename)
    cv2.imwrite(outFilename, imReg)

    # print estimated homography
    print("Estimated homography : \n", h)
