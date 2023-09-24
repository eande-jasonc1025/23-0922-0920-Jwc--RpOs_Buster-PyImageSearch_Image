# USAGE
# python change_picamera_parameters.py

# import the necesary packages
from imutils.video import VideoStream
from itertools import cycle
from pprint import pprint
import time
import cv2

# set the video stream as a global variable
global vs

def get_picam_settings(output=False):
	# access globals
	global picamSettings
	global vs

	# initialize variable to hold current settings
	currentPicamSettings = {}

	# print status message if the output will be displayed
	if output:
		print("[INFO] reading settings...")

	# grab picamera attributes from the object
	for attr in picamSettings.keys():
		currentPicamSettings[attr] = getattr(vs.camera, attr)

	# print settings to the terminal if required
	if output:
		pprint(currentPicamSettings)

	# update the global
	picamSettings = currentPicamSettings

	# return the settings to the calling function
	return currentPicamSettings

def get_single_picam_setting(setting):
	currentPicamSettings = get_picam_settings()
	return currentPicamSettings[setting]

def _set_picam_setting(**kwargs):
	# create a new video stream with the settings
	global vs
	vs.stop()
	time.sleep(0.25)
	vs = VideoStream(usePiCamera=True, **kwargs).start()
	time.sleep(1.5)
	print("[INFO] success")

def set_picam_setting(**kwargs):
	# access globals
	global picamSettings
	global vs

	# read the current settings
	print("[INFO] reading settings...")
	currentPicamSettings = get_picam_settings()

	# print the past and new values
	for (attr, value) in kwargs.items():
		print("[INFO] changing {} from {} to {}".format(attr,
			currentPicamSettings[attr], value))
		currentPicamSettings[attr] = value

	# initialize variable to hold the duplicate attributes to delete
	# since we can't have duplicates in kwargs
	attrsToDel = []

	# loop over current settings attributes
	for attr in currentPicamSettings.keys():
		# test for a value of None and if so, mark the attribute for
		# deletion
		if currentPicamSettings[attr] == None:
			attrsToDel.append(attr)

	# delete all duplicate attributes that have been marked
	for attr in attrsToDel:
		currentPicamSettings.pop(attr)

	# reassign kwargs and set camera settings
	kwargs = currentPicamSettings
	_set_picam_setting(**kwargs)

# initialize the camera's video stream
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# auto white balance and ISO modes
awbModes = ["off", "auto", "sunlight", "cloudy", "shade",
	"tungsten", "fluorescent", "flash", "horizon"]
isoModes = [0, 100, 200, 320, 400, 500, 640, 800, 1600]

# initialize two cycle pools
isoModesPool = cycle(isoModes)
awbModesPool = cycle(awbModes)

# the following dictionary consists of PiCamera attributes that can be
# *changed*; the list is not exhaustive because some settings can only
# be changed based on the values of others, so be sure to refer to
# the docs
picamSettings = {
	"awb_mode": None,
	"awb_gains": None,
	"brightness": None,
	"color_effects": None,
	"contrast": None,
	"drc_strength": None,
	"exposure_compensation": None,
	"exposure_mode": None,
	"flash_mode": None,
	"hflip": None,
	"image_denoise": None,
	"image_effect": None,
	"image_effect_params": None,
	"iso": None,
	"meter_mode": None,
	"rotation": None,
	"saturation": None,
	"sensor_mode": None,
	"sharpness": None,
	"shutter_speed": None,
	"vflip": None,
	"video_denoise": None,
	"video_stabilization": None,
	"zoom": None
}

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

	# handle *w* keypresses for "auto white balance"
	elif key == ord("w"):
		# read the white balance mode and change it
		awbMode = get_single_picam_setting("awb_mode")
		set_picam_setting(awb_mode=next(awbModesPool))

	# handle *i* keypresses for "ISO"
	elif key == ord("i"):
		# read the ISO and increase it (looping back after 1600)
		iso = get_single_picam_setting("iso")
		set_picam_setting(iso=next(isoModesPool))

	# handle *b* keypresses for "brightness"
	elif key == ord("b"):
		# read the brightness and increase it
		brightness = get_single_picam_setting("brightness")
		brightness += 1
		set_picam_setting(brightness=brightness)

	# handle *d* keypresses for "darken brightness"
	elif key == ord("d"):
		# read the brightness and decrease it
		brightness = get_single_picam_setting("brightness")
		brightness -= 1
		set_picam_setting(brightness=brightness)

	# handle *r* keypresses for "read settings"
	elif key == ord("r"):
		get_picam_settings(output=True)

	# handle *c* keypresses for "custom settings"
	elif key == ord("c"):
		set_picam_setting(brightness=30, iso=800, awb_mode="cloudy",
			vflip=True)

# cleanup
vs.stop()
cv2.destroyAllWindows()
