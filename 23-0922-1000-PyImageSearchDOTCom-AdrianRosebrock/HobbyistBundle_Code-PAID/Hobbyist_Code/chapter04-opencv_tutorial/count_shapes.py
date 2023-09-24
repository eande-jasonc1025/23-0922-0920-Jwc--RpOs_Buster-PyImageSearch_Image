# USAGE
# python count_shapes.py --image images/shapes.png

# import the necessary packages
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the input image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blur the image (to reduce false-positive detections) and then
# perform edge detection
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blurred, 50, 130)

# find contours in the edge map and initialize the total number of
# shapes found
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
total = 0

# loop over the contours one by one
for c in cnts:
	# if the contour area is small, then the area is likely noise, so
	# we should ignore the contour
	if cv2.contourArea(c) < 25:
		continue

	# otherwise, draw the contour on the image and increment the total
	# number of shapes found
	cv2.drawContours(image, [c], -1, (204, 0, 255), 2)
	total += 1

# show the output image and the final shape count
print("[INFO] found {} shapes".format(total))
cv2.imshow("Image", image)
cv2.waitKey(0)