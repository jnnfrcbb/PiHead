import os
import time
import shutil

source = "/home/pi/PiHead/main.py"
destinationFolder = "/media/pi/CIRCUITPY/"
destinationFile = "main.py"

##code option 1
while not os.path.exists(destinationFolder):
    time.sleep(0.25)
shutil.copy2(source, destinationFolder + destinationFile)


##code option 2
#fileCopied = False
#while fileCopied == False:
#    if os.path.exists(destinationFolder):
#        ret = shutil.copy2(source, destinationFolder + destinationFile)
#        print(ret)
#        fileCopied = True
#    time.sleep(0.25)