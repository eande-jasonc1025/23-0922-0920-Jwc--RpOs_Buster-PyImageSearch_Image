# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
from sklearn.metrics import pairwise
from scipy.spatial import distance as dist
from collections import namedtuple
import numpy as np
import imutils
import cv2

# define the detected pill object
DetectedPill = namedtuple("DetectedPill",
	["contour", "pill", "mask", "size"])

def find_measurement_area(image, keep=5):
	# convert the image to grayscale and then perform edge detection
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edged = cv2.Canny(gray, 50, 128)

	# find contours in the edge map, keeping only the five largest
	# ones
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]

	# initialize the list of candidate regions that *could* be the
	# pill measurement region along with (1) the contour corresponding
	# to the measurement region and (2) the warped ROI of the
	# measurement region
	regions = []
	areaCnt = None
	warped = None

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# check to see if our approximated contour has four points,
		# implying that we have potentially found the pill measurement
		# region
		if len(approx) == 4:
			# compute the bounding box of the contour region and then
			# compute the average grayscale pixel intensity of the ROI
			(x, y, w, h) = cv2.boundingRect(c)
			roi = gray[y:y + h, x:x + w]
			avg = cv2.mean(roi)[0]

			# add the mean pixel intensity and contour approximation
			# to the candidate regions list
			regions.append((avg, approx))

	# ensure at least one candidate region was found
	if len(regions) > 0:
		# sort the regions according to the average grayscale pixel
		# intensity, maintaining the assumption that the *darkest
		# region* (due to the black square) will be our pill
		# measurement area
		areaCnt = sorted(regions, key=lambda x: x[0])[0][1]

		# apply the four point transform to obtain a top-down
		# view of the input image
		warped = four_point_transform(image, areaCnt.reshape(4, 2))

	# return a tuple of the measurement area contour and the warped,
	# top-down view of the pill region
	return (areaCnt, warped)

def find_pills(image, height, keep=10, minArea=250):
	# blur the image slightly to help reduce high frequency noise and
	# then allocate memory for the output mask
	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	mask = np.zeros(image.shape[:2], dtype="uint8")

	# loop over the channels of the image
	for chan in cv2.split(blurred):
		# automatically threshold the channel using Otsu thresholding,
		# then take the bitwise OR with the mask
		thresh = cv2.threshold(chan, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		mask = cv2.bitwise_or(mask, thresh)

	# remove any connected-components that are attached to the border
	# of the mask
	mask = clear_border(mask)

	# find contours in the mask, keeping only the largest ones
	cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]

	# initialize the list of detected pills
	detectedPills = []

	# loop over the contours
	for c in cnts:
		# ensure the contour area is sufficiently large
		if cv2.contourArea(c) > minArea:
			# compute the bounding box of the pill and then use the
			# bounding box coordinates to extract both the pill and
			# its mask
			(x, y, w, h) = cv2.boundingRect(c)
			pill = image[y:y + h, x:x + w]
			pillMask = mask[y:y + h, x:x + w]

			# extract the (x, y)-coordinates from the contour and
			# then compute the pairwise euclidean distances between
			# the set of coordinates
			pts = [list(p[0]) for p in c]
			D = pairwise.pairwise_distances(pts, metric="euclidean")

			# find the indexes of the coordinates where the distance
			# is the largest
			maxDists = np.where(D == D.max())[0]
			(mI, mJ) = (maxDists[0], maxDists[1])

			# if the event there are *multiple* coordinates with the
			# same distance, we'll just take the first two points out
			# of convenience
			if maxDists.shape[0] > 2:
				mJ = maxDists[int(len(maxDists) / 2)]

			# if the height of the image is greater than the width,
			# then set the divisor equal to the width, otherwise set
			# it equal to the height
			div = image.shape[1] if image.shape[0] > image.shape[1] \
				else image.shape[0]

			# compute the distance (in pixels) between the two points
			# and then convert the distance to millimeters to estimate
			# the length of the pill
			d = dist.euclidean(pts[mI], pts[mJ])
			mm = (height / div) * d

			# create the detected pill object and update the list of
			# detected pills
			dp = DetectedPill(c, pill, pillMask, mm)
			detectedPills.append(dp)

	# return the list of pills
	return detectedPills