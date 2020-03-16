#include <opencv2/opencv.hpp>
#include "opencv2/xfeatures2d.hpp"
#include "opencv2/features2d.hpp"

using namespace std;
using namespace cv;
using namespace cv::xfeatures2d;

const int MAX_FEATURES = 500;
cont float GOOD_MATCHES_PERCENT = 0.15f;

void alignImages(Mat &im1, Mat &im2, Mat &im1Reg, Mat &h)
{
    // convert images to grayscale
    Mat im1Gray, im2Gray;
    cvtColor(im1, im1Gray, CV_BGR2GRAY);
    cvtColor(im2, im2Gray, CV_BGR2GRAY);

    // variables to store keypoints and descriptors
    std::vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;

    // detect ORB features and compute descriptors
    Ptr<Feature2D> orb = ORB::create(MAX_FEATURES);
    orb->detectAndCompute(im1Gray, Mat(), keypoints1, descriptors1);
    orb->detectAndCompute(im2Gray, Mat(), keypoints2, descriptors2);

    // match features
    std::vector<DMatch> matches;
    Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create("BruteForce-Hamming");
    matcher->match(descriptors1, descriptors2, matches, Mat());

    // sort matches by score
    std::sort(matches.begin(), matches.end());

    // remove not so good matches
    const int numGoodMatches = matches.size() * GOOD_MATCH_PERCENT;
    matches.erase(matches.begin() + numGoodMatches, matches.end());

    // draw top matches
    Mat imMatches;
    drawMatches(im1, keypoints1, im2, keypoints2, matches, imMatches);
    imwrite("matches.jpg", imMatches);

    // extract location of good matches
    std::vector<Point2f> points1, points2;

    for (size_t i = 0; i < matches.size(); i++)
    {
        points1.push_back(keypoints1[matches[i].queryIdx].pt);
        points2.push_back(keypoints2[matches[i].trainIdx].pt);
    }

    // find homography
    h = findHomography(points1, points2, RANSAC);

    // use homography to warp image
    warpPerspective(im1, im1Reg, h, im2.size());
}

int main(int argc, char **argv)
{
    // read reference image
    string refFilename("form.jpg");
    cout << "Reading reference image : " << refFilename << endl;
    Mat imReference = imread(refFilename);

    // read image to be aligned
    string imFilename("scanned-page.jpg");
    cout << "Reading image to align : " << imFilename << endl;
    Mat im = imread(imFilename);

    // registered image will be stored in imReg
    // estimated homography will be stored in h
    Mat imReg, h;

    // align images
    cout << "Aligning images ..." << endl;
    alignImages(im, imReference, imReg, h);

    // write aligned image to disk
    string outFilename("aligned.jpg");
    cout << "Saving aligned image : " << outFilename << endl;
    imwrite(outFilename, imReg);

    // print estimated homography
    cout << "Estimated homography : \n"
         << h << endl;
}