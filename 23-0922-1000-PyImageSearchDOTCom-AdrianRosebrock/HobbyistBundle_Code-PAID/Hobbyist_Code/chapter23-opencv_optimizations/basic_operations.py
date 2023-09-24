# USAGE
# python basic_operations.py

# import the necessary packages
import numpy as np
import time
import cv2

def time_it(msg, start, end):
	# show the time difference
	print("[INFO] {} took {:.8} seconds".format(msg, end - start))

# load the image from disk
start = time.time()
image = cv2.imread("coins.png")
time_it("load", start, time.time())

# convert the image to grayscale
start = time.time()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
time_it("grayscale", start, time.time())

# blur the image
start = time.time()
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
time_it("blur", start, time.time())

# perform edge detection
start = time.time()
edged = cv2.Canny(blurred, 30, 150)
time_it("edge detection", start, time.time())

# stack the original input image and edge map image so we can
# visualize it with a single cv2.imshow call
start = time.time()
output = np.hstack([image, np.dstack([edged] * 3)])
time_it("stacking", start, time.time())

# show the output image
cv2.imshow("Output", output)
cv2.waitKey(0)