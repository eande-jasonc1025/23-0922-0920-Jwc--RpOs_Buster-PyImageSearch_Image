# USAGE
# python image_sub.py --bg images/bg.jpg --fg images/adrian.jpg

# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--bg", required=True,
	help="path to background image")
ap.add_argument("-f", "--fg", required=True,
	help="path to foreground image")
args = vars(ap.parse_args())

# load the background and foreground images
bg = cv2.imread(args["bg"])
fg = cv2.imread(args["fg"])

# convert the background and foreground images to grayscale
bgGray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
fgGray = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)

# perform background subtraction by subtracting the foreground from
# the background and then taking the absolute value
sub = bgGray.astype("int32") - fgGray.astype("int32")
sub = np.absolute(sub).astype("uint8")

# threshold the image to find regions of the subtracted image with
# larger pixel differences
thresh = cv2.threshold(sub, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# perform a series of erosions and dilations to remove noise
thresh = cv2.erode(thresh, None, iterations=1)
thresh = cv2.dilate(thresh, None, iterations=1)

# find contours in the thresholded difference map and then initialize
# our bounding box regions that contains the *entire* region of motion
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(minX, minY) = (np.inf, np.inf)
(maxX, maxY) = (-np.inf, -np.inf)

# loop over the contours
for c in cnts:
	# compute the bounding box of the contour
	(x, y, w, h) = cv2.boundingRect(c)

	# reduce noise by enforcing requirements on the bounding box size
	if w > 20 and h > 20:
		# update our bookkeeping variables
		minX = min(minX, x)
		minY = min(minY, y)
		maxX = max(maxX, x + w - 1)
		maxY = max(maxY, y + h - 1)

# draw a rectangle surrounding the region of motion
cv2.rectangle(fg, (minX, minY), (maxX, maxY), (0, 255, 0), 2)

# show the output image
cv2.imshow("Output", fg)
cv2.waitKey(0)