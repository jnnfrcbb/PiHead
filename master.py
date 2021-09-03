#use this as a master script that loads all other scripts
#instead of having to get loads of stuff to run, just need to set this master script to autorun on boot
#can easily change the master script list and install to / update from pi using git
#add reference in /etc/rc.local

import os
fileString = "/etc/xdg/lxsession/LXDE-pi/autostart"
with open(fileString, "a+") as myFile:
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "controller_service /home/pi/PiHead/volume_encoder.ini" in fileData:
        myFile.write("controller_service /home/pi/PiHead/volume_encoder.ini")       #ENC1
    if not "controller_service /home/pi/PiHead/playback_encoder.ini" in fileData:
        myFile.write("\ncontroller_service /home/pi/PiHead/playback_encoder.ini")     #ENC2
    myFile.close()


#CARPIHAT
##CarPiHat CanBus interface
os.system ("/sbin/ip link set can0 up type can bitrate 100000")

fileString = "/boot/config.txt"
with open(fileString, "a") as myFile:
    fileData = myFile.read()
    myFile.close()
    fileMod = False
    if "#dtparam=spi=on" in fileData: 
        fileData = fileData.replace("#dtparam=spi=on","dtparam=spi=on")
        fileMod = True 
    if "#dtparam=i2c_arm=on" in fileData: 
        fileData = fileData.replace("#dtparam=i2c_arm=on","dtparam=i2c_arm=on")
        fileMod = True
    if fileMod is True:
        with open(fileString, "w+") as modFile:
            modFile.write(fileData)
            modFile.close()

fileString = "/boot/config.txt"
with open(fileString, "a+") as myFile: #then add new params
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "#CarPiHat" in fileData:
        myFile.write("#CarPiHat\n")
    if not "dtparam=spi=on" in fileData:
        myFile.write("dtparam=spi=on \n")
    if not "dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23" in fileData:
        myFile.write("dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=23 \n")
    if not "dtoverlay=spi-bcm2835-overlay" in fileData:
        myFile.write("dtoverlay=spi-bcm2835-overlay")
    #if not "dtoverlay=spi0-cs,cs1_pin=24" in fileData:          #uncomment if reverse doesn't work when using CAN bus
    #    myFile.write("dtoverlay=spi0-cs,cs1_pin=24 \n")
    myFile.close()

fileString = "/etc/rc.local"
with open(fileString, "a+") as myFile:
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "#CarPiHat" in fileData:
        myFile.write("#CarPiHat\n")
    if not "/sbin/ip link set can0 up type can bitrate 100000" in fileData:
        myFile.write("/sbin/ip link set can0 up type can bitrate 100000")
    myFile.close()

##CarPiHat real time clock
fileString = "/etc/rc.local"
with open(fileString, "a+") as myFile:
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "#CarPiHat" in fileData:
        myFile.write("#CarPiHat\n")
    if not "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s" in fileData:
        myFile.write("echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device hwclock -s")
    myFile.close()

fileString = "/etc/modules"
with open(fileString, "a+") as myFile:
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "#CarPiHat" in fileData:
        myFile.write("#CarPiHat\n")
    if not "rtc-ds1307" in fileData:
        myFile.write("rtc-ds1307")
    myFile.close()

##CarPiHat safeshutdown
fileString = "/boot/config.txt"
with open(fileString, "a+") as myFile:
    fileData = myFile.read()
    if len(fileData)> 0:
        myFile.write("\n")
    if not "#CarPiHat" in fileData:
        myFile.write("#CarPiHat\n")
    if not "dtoverlay=gpio-poweroff,gpiopin=25,active_low" in fileData:
        myFile.write("dtoverlay=gpio-poweroff,gpiopin=25,active_low")
    myFile.close()

import CarPiHat #run last