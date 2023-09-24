#!/bin/bash

source `which virtualenvwrapper.sh`
source start_py3cv3.sh
cd /home/pi/RPi4CV/Hobbyist_Code/chapter08-automatically_starting_scripts
python save_frames.py --output output --display 1