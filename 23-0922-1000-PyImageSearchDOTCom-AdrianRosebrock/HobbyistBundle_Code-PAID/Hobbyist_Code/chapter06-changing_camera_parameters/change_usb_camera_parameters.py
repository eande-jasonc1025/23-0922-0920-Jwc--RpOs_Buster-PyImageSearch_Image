# USAGE
# python change_usb_camera_parameters.py

# import the necesary packages
from imutils.video import VideoStream
import time
import cv2

def toggle_autofocus(vs, autofocus=True):
	# set the autofocus camera property on or off
	vs.stream.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0)
	print("[INFO] autofocus has been set to {}".format(
		"ON" if autofocus else "OFF"))

	# read back the property to ensure it was set
	actualAutofocus = vs.stream.get(cv2.CAP_PROP_AUTOFOCUS)
	print("[INFO] actual autofocus {}".format(actualAutofocus))

def toggle_auto_whitebalance(vs, autowb=True):
	# set the auto whitebalance camera property on or off
	vs.stream.set(cv2.CAP_PROP_AUTO_WB, 1 if autowb else 0)
	print("[INFO] auto white balance has been set to {}".format(
		"ON" if autowb else "OFF"))

	# read back the property to ensure it was set
	actualAutoWhitebalance = vs.stream.get(cv2.CAP_PROP_AUTO_WB)
	print("[INFO] actual auto white balance {}".format(
		actualAutoWhitebalance))

def set_zoom(vs, zoom=100):
	# set the zoom camera property on or off
	vs.stream.set(cv2.CAP_PROP_ZOOM, zoom)
	print("[INFO] zoom has been set to {}".format(zoom))

	# read back the property to ensure it was set
	actualZoom = vs.stream.get(cv2.CAP_PROP_ZOOM)
	print("[INFO] actual zoom {}".format(actualZoom))

# initialize the camera's video stream
vs = VideoStream(src=0).start()
time.sleep(2.0)

# initialize the camera parameter settings
autofocus = True
autowb = True
zoom = 100

# loop over frames
while True:
	# grab a frame
	frame = vs.read()

	# display the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)

	# handle *q* keypresses for "quit"
	if key == ord("q"):
		break

	# handle *f* keypresses for "autofocus"
	elif key == ord("f"):
		# toggle autofocus and set the camera property
		autofocus = not autofocus
		toggle_autofocus(vs, autofocus)

	# handle *w* keypresses for "auto white balance"
	elif key == ord("w"):
		# toggle auto white balance and set the camera property
		autowb = not autowb
		toggle_auto_whitebalance(vs, autowb)

	# handle *i* keypresses for "zoom in"
	elif key == ord("i"):
		# increase zoom and set the camera property
		zoom += 1
		set_zoom(vs, zoom)

	# handle *o* keypresses for "zoom out"
	elif key == ord("o"):
		# decrease zoom and set the camera property
		zoom -= 1
		set_zoom(vs, zoom)

# reset camera parameter settings
toggle_autofocus(vs, 1)
toggle_auto_whitebalance(vs, 1)
set_zoom(vs, 100)

# cleanup
vs.stop()
cv2.destroyAllWindows()