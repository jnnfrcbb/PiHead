#use this as a master script that loads all other scripts
#instead of having to get loads of stuff to run, just need to set this master script to autorun on boot
#can easily change the master script list and install to / update from pi using git
#add reference in /etc/rc.local

import os

#CONTROLLER_SERVICE
with open("/etc/xdg/lxsession/LXDE-pi/autostart", "a+") as myFile:
    if len(myFile)> 0:
        myFile.write("\n")
    if not "controller_service /home/pi/PiHead/volume_encoder.ini" in myFile:
        myFile.write("controller_service /home/pi/PiHead/volume_encoder.ini")       #ENC1
    if not "controller_service /home/pi/PiHead/playback_encoder.ini" in myFile:
        myFile.write("controller_service /home/pi/PiHead/playback_encoder.ini")     #ENC2
    myFile.close()

#CARPIHAT
##CarPiHat safeshutdown
import CarPiHat

with open("/boot/config.txt", "a+") as myFile:
    if len(myFile) > 0:
            myFile.write("\n")
    if not "#CarPiHat" in myFile:
        myFile.write ("#CarPiHat \n")
    if not "dtoverlay=gpio-poweroff,gpiopin=25,active_low" in myFile:
        myFile.write ("dtoverlay=gpio-poweroff,gpiopin=25,active_low")
    myFile.close()

##CarPiHat CanBus interface
os.system ("/sbin/ip link set can0 up type can bitrate 100000")

with open("/boot/config.txt", "a+") as myFile:
    if len(myFile) > 0:
            myFile.write("\n")
    if not "#CarPiHat" in myFile:
        myFile.write ("#CarPiHat \n")
    if not "dtparam=spi=on" in myFile:
        myFile.write ("dtparam=spi=on \n")
    if not "dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23" in myFile:
        myFile.write("dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23 \n")    
    if not "dtoverlay=spi-bcm2835-overlay" in myFile:
        myFile.write("dtoverlay=spi-bcm2835-overlay")
    #if not "dtoverlay=spi0-cs,cs1_pin=24" in myFile:    #uncomment if reverse doesn't work when using CAN bus
    #    myFile.write("\ndtoverlay=spi0-cs,cs1_pin=24")
    myFile.close()

with open("/etc/rc.local", "a+") as myFile:
    if len(myFile) > 0:
            myFile.write("\n")
    if not "/sbin/ip link set can0 up type can bitrate 100000" in myFile:
        myFile.write ("/sbin/ip link set can0 up type can bitrate 100000")
    myFile.close()

##CarPiHat real time clock
with open("/etc/rc.local", "a+") as myFile:
    if len(myFile) > 0:
            myFile.write("\n")
    if not "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s" in myFile:
        myFile.write ("echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s")
    myFile.close()

with open("/etc/modules", "a+") as myFile:
    if len(myFile) > 0:
            myFile.write("\n")
    if not "rtc-ds1307" in myFile:
        myFile.write ("rtc-ds1307")
    myFile.close()