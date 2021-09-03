#use this as a master script that loads all other scripts
#instead of having to get loads of stuff to run, just need to set this master script to autorun on boot
#can easily change the master script list and install to / update from pi using git
#add reference in /etc/rc.local

import RPi.GPIO as GPIO # import our GPIO module
import time
from subprocess import call
import os

#CONTROLLER_SERVICE
os.system ("controller_service \home\pi\PiHead\volume_encoder.ini")     #ENC1
os.system ("controller_service \home\pi\PiHead\playback_encoder.ini")   #ENC2
