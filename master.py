#use this as a master script that loads all other scripts
#instead of having to get loads of stuff to run, just need to set this master script to autorun on boot
#can easily change the master script list and install to / update from pi using git
#add reference in /etc/rc.local

import os

def appendString(fileString,writingString,signOff=""):
    if signOff is not "":
        signOffRemoved = removeString(fileString,signOff)
    with open(fileString, "a+") as myFile:
        fileData = myFile.read()
        IsMod = False
        if len(fileData)> 0:
            myFile.write("\n")
        for s in writingString:
            if not writingString(s) in fileData:
                myFile.write(writingString(s))
                IsMod = True 
        myFile.close()
        if signOffRemoved:
            m = appendString(fileString,signOff)
    return IsMod

def changeString(fileString,beforeString,afterString):
    with open(fileString, "r") as myFile:
        fileData = myFile.read()
        myFile.close()
        IsMod = False
        for s in beforeString:
            if beforeString(s) in fileData:
                fileData = fileData.replace(beforeString(s),afterString(s))
                IsMod = True
    if IsMod:
        with open(fileString, 'w') as modFile:
            modFile.write(fileData)
            modFile.close()
    return IsMod 

def removeString(fileString,removedString):
    with open(fileString, "r") as myFile:
        fileData = myFile.read()
        myFile.close()
        IsMod = False
        for s in removedString:
            if removedString(s) in fileData:
                fileData = fileData.replace(removedString(s),"")
                IsMod = True
    if IsMod:
        with open(fileString,"w") as modFile:
            modFile.write(fileData)
            modFile.close()
    return IsMod

#CONTROLLER_SERVICE
m = appendString("/etc/xdg/lxsession/LXDE-pi/autostart",["controller_service /home/pi/PiHead/volume_encoder.ini", "controller_service /home/pi/PiHead/playback_encoder.ini"])

#CARPIHAT
##CarPiHat CanBus interface
m = changeString("/boot/config.txt", ["#dtparam=spi=on","#dtparam=i2c_arm=on"], ["dtparam=spi=on","dtparam=i2c_arm=on"])
m = appendString("/boot/config.txt",["#CarPiHat","dtparam=spi=on","dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23","dtoverlay=spi-bcm2835-overlay"])
m = appendString("/etc/rc.local",["#CarPiHat", "/sbin/ip link set can0 up type can bitrate 100000"], "exit 0")

#CarPiHat real time clock
m = appendString("/etc/rc.local",["#CarPiHat", "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s"], "exit 0")
m = appendString("/etc/modules",["#CarPiHat","rtc-ds1307"])

#Safe Shutdown
m = appendString("/boot/config.txt",["#CarPiHat","dtoverlay=gpio-poweroff,gpiopin=25,active_low"])

#Run CarPiHat service
import CarPiHat