import os
import time

source = "/home/pi/PiHead/code.py"
destinationFolder = "/media/pi/CIRCUITPY/"

while not os.path.exists(destinationFolder):
    time.sleep(0.25)

os.system("sudo cp -f " + source + " " + destinationFolder)