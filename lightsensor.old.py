#!/usr/bin/python3 -u

#Based on code from this thread by PlasmaFlow: https://bluewavestudio.io/community/showthread.php?tid=672

import smbus
import os
from time import sleep
import RPi.GPIO as GPIO


#BRIGHTNESS CONSTANTS-------------------------------------------------------------

# Switch levels for brightness sensor in lux
LUX_LEVEL = [0.1, 0.5, 1, 20, 50, 100, 150, 200, 300, 400]

# Set this display brightness by switch levels
DISP_BRIGHTNESS = [17, 27, 40, 65, 90, 115, 140, 165, 195, 225, 255]

# Starting step level
step = DISP_BRIGHTNESS[5]


#DAY/NIGHT SWITCHING--------------------------------------------------------------

#Switch to night mode on this level or lower
DAYNIGHT_STEP = 4

#GPIO pin to output day/night signal (-1 = GPIO output disabled)
DAYNIGHT_PIN = 15     

#If using day/night signal, setup GPIO
if DAYNIGHT_PIN != -1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DAYNIGHT_PIN, GPIO.OUT)


#I2C SETUP------------------------------------------------------------------------
BUS = 1
TSL2561_ADDR = 0x39     #the addresss of TSL2561 can be 0x29, 0x39 or 0x49

i2cBus = smbus.SMBus(BUS)

# Start messure with 402 ms
# (scale factor 1)
i2cBus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)


#LUX AVERAGING--------------------------------------------------------------------

#Time to average readings over in seconds
AVG_TIME=10

#Number of readings to average over
AVG_COUNT=20

#Setup empty list for lux values
READ_VALUES=[]

# Function for getting and averaging lux
def getLux():
    # read global brightness read low byte
    LSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8C)
    # read high byte
    MSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8D)
    Ambient = (MSB << 8) + LSB
    # read infra red read low byte
    LSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8E)
    # read high byte
    MSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8F)
    Infrared = (MSB << 8) + LSB
    # Calc factor Infrared/Ambient
    Ratio = 0
    Lux = 0
    if Ambient != 0:
        Ratio = float(Infrared)/float(Ambient)
        # Calc lux based on data sheet TSL2561T T, FN, and CL Package
    if 0 < Ratio <= 0.50:
        Lux = 0.0304*float(Ambient) - 0.062*float(Ambient)*(Ratio**1.4)
    elif 0.50 < Ratio <= 0.61:
        Lux = 0.0224*float(Ambient) - 0.031*float(Infrared)
    elif 0.61 < Ratio <= 0.80:
        Lux = 0.0128*float(Ambient) - 0.0153*float(Infrared)
    elif 0.80 < Ratio <= 1.3:
        Lux = 0.00146*float(Ambient) - 0.00112*float(Infrared)
    else:
        Lux = 0

    #round lux value
    luxRounded = round(Lux,1)

    #check if we have a full set of readings to average over
    if len(READ_VALUES) == AVG_COUNT:
        #if so, delete oldest reading (otherwise, let it work up to AVG_COUNT)
        READ_VALUES.pop(0)

    #add new lux value
    READ_VALUES.append(luxRounded)
    os.system("echo {} > /tmp/tsl2561".format(luxRounded))

    #return average of stored readings
    return sum(READ_VALUES)/len(READ_VALUES)


#CALCULATING AND SETTING BRIGHTNESS-----------------------------------------------

# Function for calculating step
def getStep(luxValue):
    for luxLevel in LUX_LEVEL:
        if luxValue <= luxLevel:
            break
    return LUX_LEVEL.index(luxLevel)

# Function for writing brightness to file
def writeStep(newStep):
    
    if newStep != step:

        file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
        file.write(str(DISP_BRIGHTNESS[newStep]))
        file.close()

        if DAYNIGHT_PIN != -1:
            if newStep <= DAYNIGHT_STEP:
                #print("Lux = {} | ".format(AVG_LUX) + "Level " + str(newStep) + " -> trigger night")
                os.system("touch /tmp/night_mode_enabled >/dev/null 2>&1")
                GPIO.output(DAYNIGHT_PIN, 1) ## output signal on GPIO to say night mode should activate
            else:
                #print("Lux = {} | ".format(AVG_LUX) + "Level " + str(newStep) + " -> trigger day")
                os.system("sudo rm /tmp/night_mode_enabled >/dev/null 2>&1")
                GPIO.output(DAYNIGHT_PIN, 0) ## output signal on GPIO to say day mode should activate
    
        step = newStep
    
    
#START LOOPING--------------------------------------------------------------------

while True:

    #AVG_LUX = getLux()
    #writeStep(getStep(AVG_LUX))
    
    writeStep(getStep(getLux))

    sleep(AVG_TIME/AVG_COUNT) #0.25)