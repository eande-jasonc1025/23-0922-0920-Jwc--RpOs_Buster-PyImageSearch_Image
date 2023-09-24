# USAGE
# python basics.py

# import the necessary packages
import imutils
import cv2
import os

# load the input image and show its dimensions, keeping in mind that
# images are represented as a multi-dimensional NumPy array with shape:
# num rows (height) * num columns (width) * num channels (depth)
p = os.path.sep.join(["images", "30th_birthday.png"])
image = cv2.imread(p)
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))

# display the image to our screen -- we will need to click the window
# opened by OpenCV and press a key on our keyboard to continue execution
cv2.imshow("Image", image)
cv2.waitKey(0)

# access the RGB pixel located at x=430, y=200, keeping in mind that
# OpenCV stores images in BGR order rather than RGB (the pixel value
# at this location is part of the "red" in the jeep)
(B, G, R) = image[200, 430]
print("R={}, G={}, B={}".format(R, G, B))

# extract a 100x100 pixel square ROI (Region of Interest) from the
# input image starting at x=150,y=80 and ending at x=250,y=400
roi = image[80:400, 150:250]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

# resize the image to 300x300px, ignoring aspect ratio
resized = cv2.resize(image, (300, 300))
cv2.imshow("Fixed Resizing", resized)
cv2.waitKey(0)

# resize the image, maintaining aspect ratio
resized = imutils.resize(image, width=300)
cv2.imshow("Aspect Ratio Resize", resized)
cv2.waitKey(0)

# rotate the image 45 degrees clockwise
rotated = imutils.rotate(image, -45)
cv2.imshow("Rotation", rotated)
cv2.waitKey(0)

# apply a Gaussian blur with a 11x11 kernel to the image to smooth it,
# useful when reducing high frequency noise
blurred = cv2.GaussianBlur(image, (11, 11), 0)
cv2.imshow("Blurred", blurred)
cv2.waitKey(0)

# draw a rectangle, circle, and line on the image, then draw text on
# the image as well
cv2.rectangle(image, (150, 80), (250, 400), (255, 0, 255), 5)
cv2.circle(image, (490, 240), 30, (255, 0, 0), -1)
cv2.line(image, (0, 0), (600, 457), (0, 0, 255), 5)
cv2.putText(image, "You're learning OpenCV!", (10, 435),
	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Drawing", image)
cv2.waitKey(0)