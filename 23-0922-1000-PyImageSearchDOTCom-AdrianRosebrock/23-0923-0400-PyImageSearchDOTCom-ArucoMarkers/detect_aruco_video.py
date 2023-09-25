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

    # jwc Seems that framerate has no effect, whether 60 or 30, try 10

     ###jwc o src=0 for CsiCam: vs = VideoStream(src=0).start()
    ###jwc src=1 for UsbCam
    ###jwc y vs = VideoStream(src=1).start()
    ###jwc y 14-15fps vs = VideoStream(src=1,resolution=(640, 480)).start()
    ###jwc vs = VideoStream(src=1,resolution=(320, 240)).start()
    ###jwc UsbCam Logitechc922 14-15fps but more drops to 5 once in a while (10%)
    ###jwc CsiCam Landzo 15-16fps but fewer drops to 5 once in a while (10%)
    ###jwc y vs = VideoStream(src=0,resolution=(320, 240)).start()
    
    # jwc VideoStream = Vi, Imutils.resize = Im
    # jwc 'VideoStream: h,w' should be in sync w/ 'imutils.resize: h,w' :)+
    # jwc seems Vi 512, 256 decent accuracy for even Marker Id 24+
    # jwc seems Im 600, 400 max, any bigger causes screen refresh lag of even 1-2 secs
    # jwc TYJ seems Vi 512, 256 good accuracy of 2nd level complicated ArUco (e.g. Id24), w/ Im 600, 400  :)+
    # jwc seems that even above, after 10' of operation, 1-2 delay lag, so maybe decrease 90fps to 30fps
 
    ###jwc y 25-30fps on Sd37: vs = VideoStream(src=0, usePiCamera=True, resolution=(320, 240), framerate=60).start()
    ###jwc y: vs = VideoStream(src=0, usePiCamera=True, resolution=(160, 120), framerate=60).start()
    ###jwc vs = VideoStream(src=0, usePiCamera=True, resolution=(80, 60), framerate=60).start()
    ###jwc vs = VideoStream(src=0, usePiCamera=True, resolution=(80, 60), framerate=10).start()
    ###jwc not good enough for Id-38, Marker Size 80 Original Aruco, 20-25fps, but realistically 30fps+: vs = VideoStream(src=0, usePiCamera=True, resolution=(80, 60), framerate=10).start()
    # jwc seems min VideoStream 160,128 dimensions for accurate Original Aruco 0-5 (most basic designs) w/ frame 800,600
     # vs = VideoStream(src=0, usePiCamera=True, resolution=(160, 128), framerate=10).start()
    # jwc Vi 256, 128 >> Im 1200, 900
    ### vs = VideoStream(src=0, usePiCamera=True, resolution=(256, 128), framerate=10).start()
    #
    # jwc seems Vi 512, 256 decent accuracy for even Marker Id 24+, Im 1200, 900 seems laggy on display, try 1000, 750, try 800, 600, try 400, 300

    ###jwc try framerate 10 to 120 vs = VideoStream(src=0, usePiCamera=True, resolution=(512, 256), framerate=10).start()
    ###jwc n 120, 100 too big: vs = VideoStream(src=0, usePiCamera=True, resolution=(512, 256), framerate=120).start()
    ###jwc vs = VideoStream(src=0, usePiCamera=True, resolution=(512, 256), framerate=90).start()
    ###jwc vs = VideoStream(src=0, usePiCamera=True, resolution=(512, 256), framerate=30).start()
    ###jwc 30 to 60fps, seems faster repsonse: vs = VideoStream(src=0, usePiCamera=True, resolution=(256, 128), framerate=30).start()
    ###jwc 60 to 90fps seems to provide more snappier response :)+: vs = VideoStream(src=0, usePiCamera=True, resolution=(256, 128), framerate=60).start()
    
    ###jwc yyy switch to UsbCam vs = VideoStream(src=0, usePiCamera=True, resolution=(256, 128), framerate=90).start()
    ###jwc UsbCam C922 more laggier: vs = VideoStream(src=1, usePiCamera=False, resolution=(256, 128), framerate=90).start()
    vs = VideoStream(src=0, usePiCamera=True, resolution=(256, 128), framerate=90).start()

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
    #jwc 'VideoStream: h,w' should be in sync w/ 'imutils.resize: h,w' :)+
    ###jwc y: frame = imutils.resize(frame, height=320, width=240)
    ###jwc y frame = imutils.resize(frame, height=160, width=120)
    ###jwc videostream 80,60  30fps seems but shows 6-8fps
    ###jwc frame = imutils.resize(frame, height=1600, width=1200)
    ###jwc yy frame = imutils.resize(frame, height=800, width=600)
    ###jwc y frame = imutils.resize(frame, height=1200, width=900)
    ###jwc y frame = imutils.resize(frame, height=1000, width=750)
    ###jwc y frame = imutils.resize(frame, height=800, width=600)
    ###jwc yy frame = imutils.resize(frame, height=400, width=300)
    ###jwc 1-2 sec lag: frame = imutils.resize(frame, height=750, width=500)
    frame = imutils.resize(frame, height=600, width=400)


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
 
    ###jwc comment-out to increase resonse_time y: fpsCount()    
    # jwc does not seem to cause too much delay in response_time:
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
 