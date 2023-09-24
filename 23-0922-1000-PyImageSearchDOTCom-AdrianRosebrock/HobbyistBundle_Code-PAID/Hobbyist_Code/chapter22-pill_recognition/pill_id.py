# USAGE
# python pill_id.py --conf config/config.json

# import the necessary packages
from imutils.video import VideoStream
from pyimagesearch.pillsearcher import PillSearcher
from pyimagesearch.utils import Conf
from pyimagesearch.pill_finder import find_measurement_area
from pyimagesearch.pill_finder import find_pills
from pyimagesearch.pill_describer import describe_shape
from pyimagesearch.pill_describer import describe_color
from pyimagesearch.pill_describer import describe_texture
import argparse
import imutils
import pickle
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration
conf = Conf(args["conf"])

# initialize the pills database
print("[INFO] initializing pill database...")
nextID = 0
db = {}

# if the pill database exists on disk, load it
if os.path.exists(conf["db_path"]):
	print("[INFO] loading pill database...")
	db = pickle.loads(open(conf["db_path"], "rb").read())
	nextID = max(db.keys()) + 1

# initialize the pill searcher
ps = PillSearcher(db)

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

# loop over frames from the video stream
while True:
	# read a frame from the camera sensor
	frame = vs.read()

	# if the height is greater than the width, then resize the frame
	# to have a maximum height of 600 pixels
	if frame.shape[0] > frame.shape[1]:
		frame = imutils.resize(frame, height=600)

	# otherwise, the width is greater than the height so resize the
	# frame to have a maximum width of 600 pixels
	else:
		frame = imutils.resize(frame, width=600)

	# find the pill measurement area in the frame
	area = find_measurement_area(frame)
	foundArea = False

	# only continue if the pill measurement area was found
	if area[0] is not None:
		# draw the contour corresponding to the measurement area
		(areaCnt, area) = area
		foundArea = True
		cv2.drawContours(frame, [areaCnt], -1, (0, 0, 255), 2)

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# check to see if we should register a new pill in the database
	if key == ord("r") and foundArea:
		# find all pills in the measurement area
		pills = find_pills(area, conf["measurement_area_size"])

		# loop over each of the detected pills
		for pill in pills:
			# quantify the color, shape, and texture of the pill
			color = describe_color(pill.pill, pill.mask)
			shape = describe_shape(pill.contour)
			texture = describe_texture(pill.pill, pill.mask)

			# grab the pill name from the user
			name = input("Enter the pill name: ")

			# construct the data for pill
			data = {
				"id": nextID,
				"name": name,
				"size": pill.size,
				"color": color,
				"shape": shape,
				"texture": texture
			}

			# update the database with the new pill
			print("[INFO] added pill ID {} with name '{}'".format(
				nextID, name))
			db[nextID] = data
			nextID += 1

			# write the new, updated database to disk
			f = open(conf["db_path"], "wb")
			f.write(pickle.dumps(db))
			f.close()

	# check to see if we should recognize the pill(s) in the frame
	elif key == ord("v") and foundArea:
		# find all pills in the measurement area
		pills = find_pills(area, conf["measurement_area_size"])

		# ensure at least one pill was found
		if len(pills) > 0:
			# grab the original width of the measurement area, resize
			# it, and then compute the ratio of the new area width to
			# the old area width -- we'll use this ratio later when
			# scaling the bounding boxes of the pills
			origW = area.shape[1]
			area = imutils.resize(area, width=256)
			ratio = area.shape[1] / float(origW)

			# loop over each of the detected pills
			for pill in pills:
				# quantify the color, shape, and texture of the pill
				color = describe_color(pill.pill, pill.mask)
				shape = describe_shape(pill.contour)
				texture = describe_texture(pill.pill, pill.mask)

				# identify the pill
				results = ps.search(pill.size, shape, color,
					texture, conf["weights"])
				pillID = results[0][1]
				name = db[pillID]["name"]

				# compute the bounding box of the pill and then scale
				# the bounding box based on our computed ratio
				(x, y, w, h) = cv2.boundingRect(pill.contour)
				x = int(x * ratio)
				y = int(y * ratio)
				w = int(w * ratio)
				h = int(h * ratio)

				# draw a bounding box surrounding the pill along with
				# the name of the pill itself
				cv2.rectangle(area, (x, y),
					(x + w, y + h), (0, 0, 255), 2)
				cv2.putText(area, name, (x, y - 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# show the output pill identifications
			cv2.imshow("Pill IDs", area)

	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()