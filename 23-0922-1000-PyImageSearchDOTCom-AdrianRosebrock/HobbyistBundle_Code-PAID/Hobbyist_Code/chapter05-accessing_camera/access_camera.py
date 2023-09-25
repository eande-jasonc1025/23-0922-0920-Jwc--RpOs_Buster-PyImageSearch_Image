# USAGE
# python access_camera.py

# import the necessary packages
from imutils.video import VideoStream
import imutils
import time
import cv2

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

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
# jwc UsbCam
###jwc y vs = VideoStream(src=0).start()
# jwc pi_camera
###jwc o vs = VideoStream(usePiCamera=True, resolution=(640, 480)).start()
vs = VideoStream(usePiCamera=True, resolution=(640, 480)).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the  video stream and resize it to have a
	# maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

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
