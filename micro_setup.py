import os
import time

source = "/home/pi/PiHead/code.py"
destinationFolder = "/media/pi/CIRCUITPY/"

while not os.path.isdir(destinationFolder):
    time.sleep(0.25)

print("microcontroller found")

os.system("sudo chmod a+r+w+ " + destinationFolder)

os.system("cp -f " + source + " " + destinationFolder)