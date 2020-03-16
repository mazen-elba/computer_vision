# Introduction to FAST (Features from Accelerated Segment Test)

We have several feature detectors and many of them are really good. But when looking from a real-time application point of view, they are not fast enough. One best example would be SLAM (Simultaneous Localization and Mapping) mobile robot which has limited computational resources.

<p align="center">   <img src="https://cdn-images-1.medium.com/max/2000/0*mdITGZogcZO6c8iW.jpg" /> </p>

As a solution to this,**_ Features from accelerated segment test (FAST) _** is a corner detection method, which could be used to extract feature points and later used to track and map objects in many computer vision tasks. The FAST corner detector was originally developed by Edward Rosten and Tom Drummond and was published in 2006. The most promising advantage of the FAST corner detector is its computational efficiency. Moreover, when machine learning techniques are applied, superior performance in terms of computation time and resources can be realized. The FAST corner detector is very suitable for real-time video processing application because of this high-speed performance.

## **Feature Detection using FAST**

The algorithm is explained below:

<p align="center">   
    <img src="https://cdn-images-1.medium.com/max/2000/0*iB26EPO33F4LSig3.jpg" />
</p>

- Select a pixel **_p_** in the image which is to be identified as an interest point or not. Let its intensity be **_Ip_**.

- Select appropriate threshold value **_t_**.

- Consider a circle of 16 pixels around the pixel under test. (This is a [Bresenham circle](http://en.wikipedia.org/wiki/Midpoint_circle_algorithm) of radius 3.)

- Now the pixel**_ p_** is a corner if there exists a set of **_n_** contiguous pixels in the circle (of 16 pixels) which are all brighter than **_Ip + t_**, or all darker than **_Ip - t_**. (The authors have used **_n_**= 12 in the first version of the algorithm)

- To make the algorithm fast, first compare the intensity of pixels 1, 5, 9 and 13 of the circle with **_Ip_**. As evident from the figure above, at least three of these four pixels should satisfy the threshold criterion so that the interest point will exist.

- If at least three of the four-pixel values — **_I1, I5, I9, I13_** are not above or below **_Ip + t_**, then **_p_** is not an interest point (corner). In this case reject the pixel **_p_** as a possible interest point. Else if at least three of the pixels are above or below **_Ip + t_**, then check for all 16 pixels and check if 12 contiguous pixels fall in the criterion.

- Repeat the procedure for all the pixels in the image.

There are a few limitations to the algorithm. First, for **_n_**<12, the algorithm does not work very well in all cases because when **_n_**<12 the number of interest points detected are very high. Second, the order in which the 16 pixels are queried determines the speed of the algorithm. A machine learning approach has been added to the algorithm to deal with these issues.

## Machine Learning Approach

- Select a set of images for training (preferably from the target application domain)

- Run FAST algorithm in every image to find feature points.

- For every feature point, store the 16 pixels around it as a vector. Do it for all the images to get feature vector**_ p_**.

- Each pixel (say **_x_**) in these 16 pixels can have one of the following three states:

<p align="center">   <img src="https://cdn-images-1.medium.com/max/2000/0*iRvkt1oaiuwyQBTk.jpg" />
 </p>

- Depending on these states, the feature vector **_P_** is subdivided into 3 subsets **_Pd, Ps, Pb_**.

- Define a variable **_Kp_** which is true if **_p _**is an interest point and false if **_p_** is not an interest point.

- Use the ID3 algorithm (decision tree classifier) to query each subset using the variable Kp for the knowledge about the true class.

- The ID3 algorithm works on the principle of entropy minimization. Query the 16 pixels in such a way that the true class is found (interest point or not) with the minimum number of queries. Or in other words, select the pixel x, which has the most information about the pixel **_p_**. The entropy for the set **_P_** can be mathematically represented as:

<p align="center">   <img src="https://cdn-images-1.medium.com/max/2000/1*dASNQQGi9XIdNCThBzDqpw.png" />
 </p>

- This is recursively applied to all the subsets until its entropy is zero.

- The decision tree so created is used for fast detection in other images.

## Non-maximal Suppression

Detecting multiple interest points in adjacent locations is another problem. It is solved by using Non-maximum Suppression.

- Compute a score function, **_V_** for all the detected feature points. **_V_** is the sum of absolute difference between **_p_** and 16 surrounding pixels values.

- Consider two adjacent keypoints and compute their **_V_** values.

- Discard the one with lower **_V_** value.

## Limitations of the FAST Algorithm

Other corner detection methods work very differently from the FAST method and a surprising result is that FAST does not detect corners on computer-generated images that are perfectly aligned to the **\*x-axes** \*and **_y-axes_**. Since the detected corner must have a ring of darker or lighter pixel values around the center that includes both edges of the corner, crisp images do not work well.

This because the FAST algorithm requires a ring of contrasting pixels more than three-quarters around the center of corner. In the computer-generated image, both edges of a box at a corner are in the ring of the pixel used, so the test for a corner fails. A workaround to this problem is to add blur (by applying a Gaussian filter) to the image so that the corners are less precise but can be detected.

## References

- [https://github.com/deepanshut041/feature-detection/blob/master/fast/README.md](https://github.com/deepanshut041/feature-detection/blob/master/fast/README.md)

- Viswanathan, Deepak. “Features from Accelerated Segment Test ( FAST ).” (2011).

- Edward Rosten and Tom Drummond, “Machine learning for high speed corner detection” in 9th European Conference on Computer Vision, vol. 1, 2006, pp. 430–443.

- Edward Rosten, Reid Porter, and Tom Drummond, “Faster and better: a machine learning approach to corner detection” in IEEE Trans. Pattern Analysis and Machine Intelligence, 2010, vol 32, pp. 105–119.

- [https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_fast/py_fast.html](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_fast/py_fast.html)

- [https://in.udacity.com/course/computer-vision-nanodegree--nd891](https://in.udacity.com/course/computer-vision-nanodegree--nd891)
