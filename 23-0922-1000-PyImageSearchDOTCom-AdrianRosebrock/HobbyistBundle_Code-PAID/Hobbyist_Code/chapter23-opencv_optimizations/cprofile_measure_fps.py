# USAGE
# python cprofile_measure_fps.py

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import cProfile
import imutils
import time
import cv2

# initialize and enable the profiler
pr = cProfile.Profile()
pr.enable()

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True, resolution=(640, 480)).start()
time.sleep(2.0)

# load OpenCV's face detector and start our FPS throughput measurement
# class
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the  video stream, resize it to have a
	# maximum width of 400 pixels, and then convert it to graysacle
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale image
	rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=9,
		minSize=(40, 40), flags=cv2.CASCADE_SCALE_IMAGE)

	# loop over the bounding boxes and draw a rectangle around each face
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

# disable the profiler and print sorted statistics
pr.disable()
pr.print_stats(sort="time")
