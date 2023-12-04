#use this as a master script that loads all other scripts etc
#instead of having to get loads of stuff to run, just need to set this master script to autorun on boot
#can easily change the master script list and install to / update from pi using git
#add reference in /etc/rc.local

import os
import RPi.GPIO as GPIO
from subprocess import call
import time

def appendString(fileString,writingString,signOff=""):
    if signOff is not "":
        signOffRemoved = removeString(fileString,signOff)
    with open(fileString, "a+") as editFile:
        fileData = editFile.read()
        IsMod = False
        if not writingString in fileData:
            if len(fileData)> 0:
                editFile.write("\n")
            editFile.write(writingString)
            IsMod = True
        editFile.close()
        if signOff is not "":
            if signOffRemoved:
                m = appendString(fileString,signOff)
    return IsMod

def replaceString(fileString,beforeString,afterString):
    with open(fileString, "r") as editFile:
        fileData = editFile.read()
        editFile.close()
        IsMod = False
        if beforeString in fileData and not afterString in fileData:
            fileData = fileData.replace(beforeString,afterString)
            IsMod = True
    if IsMod:
        with open(fileString, 'w') as modFile:
            modFile.write(fileData)
            modFile.close()
    return IsMod

def removeString(fileString,removedString):
    with open(fileString, "r") as editFile:
        fileData = editFile.read()
        editFile.close()
        IsMod = False
        if removedString in fileData:
            fileData = fileData.replace(removedString,"")
            IsMod = True
    if IsMod:
        with open(fileString,"w") as modFile:
            modFile.write(fileData)
            modFile.close()
    return IsMod


#########################
## GENERAL PREPARATION ##
#########################

GPIO.setmode(GPIO.BCM)


#####################
## SET PERMISSIONS ##
#####################

os.system("sudo chmod a+rw /boot/config.txt")
os.system("sudo chmod a+rw /etc/xdg/lxsession/LXDE-pi/autostart")
os.system("sudo chmod -R a+rw /usr/share/openautopro")


########################
## LIGHT SENSOR SETUP ##
########################

os.system("sudo python /home/pi/PiHead/lightsensor.py &")


###################
## TRINKET SETUP ##
###################

os.system("sudo python /home/pi/PiHead/trinket_setup.py &")


########################
## CONTROLLER_SERVICE ##
########################

m = appendString("/etc/xdg/lxsession/LXDE-pi/autostart","controller_service /home/pi/PiHead/volume_encoder.ini")
m = appendString("/etc/xdg/lxsession/LXDE-pi/autostart","controller_service /home/pi/PiHead/playback_encoder.ini")


##############################
## HOTKEY FOR DISPLAY POWER ##
##############################

m = replaceString("/etc/xdg/openbox/lxde-pi-rc.xml","<chainQuitKey>C-g</chainQuitKey>",'<chainQuitKey>C-g</chainQuitKey><keybind key="C-A-b"><action name="bl_toggle"><command>/home/pi/PiHead/bl_toggle.sh</command></action></keybind>')
os.system("sudo chmod a+x /home/pi/PiHead/bl_toggle.sh")


##################
## SPLASH SETUP ##
##################

m = replaceString("/etc/systemd/system/openautopro.splash.service","/usr/share/openautopro/splash1.h264","/home/pi/PiHead/Media/splash1.h264")
m = replaceString("/etc/systemd/system/openautopro.splash.service","/usr/share/openautopro/splash2.h264","/home/pi/PiHead/Media/splash2.h264")


#################
## TURN ON AMP ##
#################

AMP_PIN=22

GPIO.setup(AMP_PIN,GPIO.OUT)
GPIO.output(AMP_PIN, 1)


########################
## TURN ON OBD READER ##
########################

OBD_PIN=27

GPIO.setup(OBD_PIN,GPIO.OUT)
GPIO.output(OBD_PIN, 1)


##############
## CARPIHAT ##
##############

## CarPiHat CanBus interface ##
#m = appendString("/etc/rc.local", "/sbin/ip link set can0 up type can bitrate 100000")

m = replaceString("/boot/config.txt", "#dtparam=spi=on", "dtparam=spi=on")
m = replaceString("/boot/config.txt", "#dtparam=i2c_arm=on","dtparam=i2c_arm=on")

#m = appendString("/boot/config.txt","#CarPiHat")
#m = appendString("/boot/config.txt","dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23")
#m = appendString("/boot/config.txt","dtoverlay=spi-bcm2835-overlay")

# CarPiHat real time clock ##
m = removeString("/etc/rc.local","exit 0")
m = appendString("/etc/rc.local", "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s")
m = appendString("/etc/rc.local","exit 0")
m = appendString("/etc/modules","#CarPiHat")
m = appendString("/etc/modules","rtc-ds1307")


###################
## SAFE SHUTDOWN ##
###################

m = appendString("/boot/config.txt","#CarPiHat")
m = appendString("/boot/config.txt","dtoverlay=gpio-poweroff,gpiopin=25,active_low")

IGN_PIN = 12
EN_POWER_PIN = 25
IGN_LOW_TIME = 5

GPIO.setup(IGN_PIN, GPIO.IN)
GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(EN_POWER_PIN, 1)

ignLowCounter = 0

while ignLowCounter < (IGN_LOW_TIME + 1):
    if GPIO.input(IGN_PIN) !=1:
        GPIO.output(OBD_PIN, 0)
        time.sleep(1)
        ignLowCounter += 1
        print(ignLowCounter)
        if ignLowCounter > IGN_LOW_TIME:
            GPIO.output(AMP_PIN, 0)
            print("Shutting Down")
            call("sudo shutdown -h now", shell=True)
    else:
        print("Shutdown aborted")
        ignLowCounter = 0
        GPIO.output(AMP_PIN, 1)
        GPIO.output(OBD_PIN, 1)