import os
import time
import shutil

source = "/home/pi/PiHead/main.py"
destinationFolder = "/media/pi/CIRCUITPY/"
destinationFile = "main.py"

fileCopied = False
while fileCopied == False:
    if os.path.exists(destinationFolder):
        shutil.copy2(source, destinationFolder + destinationFile)
        fileCopied = True
    time.sleep(0.25)