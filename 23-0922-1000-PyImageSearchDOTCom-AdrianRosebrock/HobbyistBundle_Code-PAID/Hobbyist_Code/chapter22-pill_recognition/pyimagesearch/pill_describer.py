# import the necessary packages
from skimage.feature import local_binary_pattern
import numpy as np
import cv2

def describe_color(pill, mask, bins=(4, 4, 4)):
	# convert the pill image to the HSV color space, then extract
	# a 3D color histogram from the masked region of the pill
	hsv = cv2.cvtColor(pill, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], mask, bins,
		[0, 180, 0, 256, 0, 256])

	# normalize the histogram and flatten it
	hist = cv2.normalize(hist, hist).flatten()

	# return the histogram
	return hist

def describe_shape(mask):
	# compute the Hu moments shape features
	moments = cv2.HuMoments(cv2.moments(mask)).flatten()

	# log transform the moments to make them comparable
	sign = np.copysign(1.0, moments)
	log = np.log10(np.absolute(moments))
	moments = -1 * sign * log

	# return the log transformed Hu moments
	return moments

def describe_texture(pill, mask, numPoints=24, radius=8, eps=1e-7):
	# convert the pill image to grayscale
	gray = cv2.cvtColor(pill, cv2.COLOR_BGR2GRAY)

	# compute the Local Binary Pattern representation of the
	# grayscale image, then grab the LBP values for *only* the
	# masked region
	lbp = local_binary_pattern(gray, numPoints, radius,
		method="uniform")
	lbp = lbp[mask > 0]

	# compute a histogram based on the LBP values
	(hist, _) = np.histogram(lbp, bins=np.arange(0, numPoints + 3),
		range=(0, numPoints + 2))

	# normalize the histogram
	hist = hist.astype("float")
	hist /= (hist.sum() + eps)

	# return the LBP histogram
	return hist