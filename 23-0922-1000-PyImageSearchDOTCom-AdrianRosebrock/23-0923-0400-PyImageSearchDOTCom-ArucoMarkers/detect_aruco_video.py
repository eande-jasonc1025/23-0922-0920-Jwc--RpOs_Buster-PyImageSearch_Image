# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
# jwc note that '_' is used as even a '-' will be converted to '_'
ap.add_argument("-v", "--video_mode", type=str, 
    default="VideoStream",
	help="VideoStream (faster) or VideoCapture (slower)")

args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

framecount = 0
prevMillis = 0
def fpsCount():
    global prevMillis
    global framecount
    millis = int(round(time.time() * 1000))
    framecount += 1
    if millis - prevMillis > 1000:
        print(framecount)
        prevMillis = millis 
        framecount = 0

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

if args["video_mode"] == "VideoCapture":
	print("[INFO] Video Mode: '{}'...".format(args["video_mode"]))
	stream = cv2.VideoCapture(0)
	time.sleep(2.0)

elif args["video_mode"] == "VideoStream":
	# initialize the video stream and allow the camera sensor to warm up
	###jwc o print("[INFO] starting ideo stream...")
	print("[INFO] Video Mode: '{}'...".format(args["video_mode"]))

 	###jwc o src=0 for CsiCam: vs = VideoStream(src=0).start()
	###jwc src=1 for UsbCam
	###jwc y vs = VideoStream(src=1).start()
	###jwc y 14-15fps vs = VideoStream(src=1,resolution=(640, 480)).start()
	###jwc vs = VideoStream(src=1,resolution=(320, 240)).start()
	###jwc UsbCam Logitechc922 14-15fps but more drops to 5 once in a while (10%)
	###jwc CsiCam Landzo 15-16fps but fewer drops to 5 once in a while (10%)
	###jwc y vs = VideoStream(src=0,resolution=(320, 240)).start()
	vs = VideoStream(src=0, usePiCamera=True, resolution=(320, 240), framerate=60).start()
	time.sleep(2.0)

# loop over the frames from the video stream
while True:
	if args["video_mode"] == "VideoCapture":
		(grabbed, frame) = stream.read()

	elif args["video_mode"] == "VideoStream":
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 1000 pixels
		frame = vs.read()
  
	###jwc y 2-3fps CsiCam Lanzo seems good (better vs. CsiPiCam2): frame = imutils.resize(frame, width=1000)
	###jwc y 7-8 fps: frame = imutils.resize(frame, width=500)
	###jwc y 17-18fps frame = imutils.resize(frame, width=250)
	###jwc y 33-35fps frame = imutils.resize(frame, width=125)
	###jwc yy 15-16fps seems just right
	###jwc yy same fps for CsiCam_Lanzo_PiCamClone
	###jwc yy frame = imutils.resize(frame, width=320)
	###jwc yyy 19-20fps with 'height' added and now h,w in sync w/ above 'VideoStream' :)+
	frame = imutils.resize(frame, height=320, width=240)

 	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
		arucoDict, parameters=arucoParams)
 
	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()
		
        # loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			
            # convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))
   
			# draw the bounding box of the ArUCo detection
			cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

			# draw the ArUco marker ID on the frame
			cv2.putText(frame, str(markerID),
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
 
	fpsCount()    

	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop

	if key == ord("q"):
		print("[INFO] ending video stream...")
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()   
print("[INFO] destroy all windows & stopped video stream.")
 