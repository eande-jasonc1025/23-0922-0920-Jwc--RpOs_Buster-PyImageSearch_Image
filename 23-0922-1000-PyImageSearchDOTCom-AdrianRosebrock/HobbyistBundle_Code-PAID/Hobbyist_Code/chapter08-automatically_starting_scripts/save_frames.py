# USAGE
# python save_frames.py --output output --display 1

# import the necessary packages
from imutils.video import VideoStream
import argparse
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, 
	help="Path to the output directory")
ap.add_argument("-d", "--display", type=int, default=0,
	help="boolean used to indicate if frames should be displayed")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# set the frame count to zero
count = 0

# loop over frames from the video stream
while True:
	# grab the next frame from the stream
	frame = vs.read()

	# write the current frame to output directory
	p = os.path.sep.join([args["output"], "{}.jpg".format(count)])
	cv2.imwrite(p, frame)

	# check to see if the display flag is set
	if args["display"] > 0:
		# show the output frame
		cv2.imshow("frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break

	# increment the count
	count += 1

	# if the count reaches 1000, stop saving frames by breaking out
	# of the loop
	if count % 1000 == 0:
		break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
vs.stop()