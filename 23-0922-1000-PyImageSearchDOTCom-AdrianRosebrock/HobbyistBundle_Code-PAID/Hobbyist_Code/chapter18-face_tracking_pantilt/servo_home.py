# USAGE
# python servo_home.py

# import necessary packages
import pantilthat as pth
import time

# enable the pan and tilt servos
pth.servo_enable(1, True)
pth.servo_enable(2, True)

# tilt to position zero
pth.tilt(0)
time.sleep(1)

# pan to position zero
pth.pan(0)
time.sleep(1)

# disable the servos
pth.servo_enable(1, False)
pth.servo_enable(2, False)