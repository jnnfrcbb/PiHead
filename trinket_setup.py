import os
import time
import shutil

source = "/home/pi/PiHead/code.py"
destinationFolder = "/media/pi/CIRCUITPY/"
destinationFile = "code.py"

while not os.path.exists(destinationFolder):
    time.sleep(0.25)
#shutil.copy2(source, destinationFolder + destinationFile)
#os.sustem("sudo cp -fr " + source + " " + destinationFolder + destinationFile)