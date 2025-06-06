#!/usr/bin/python3 -u

#Based on code from this thread by PlasmaFlow: https://bluewavestudio.io/community/showthread.php?tid=672

import smbus
from time import sleep
import RPi.GPIO as GPIO

#INIT VALUES----------------------------------------------------------------------

#Default brightness level
BRIGHT_LVL = 125

#Minimum brightness level [min 0]
BRIGHT_MIN = 15

#Maximum brightness level [max 255]
BRIGHT_MAX = 255

#Curve value for brightness [1 = linear lux:brightness ratio]
BRIGHT_CRV = 0.4

#Time to average readings over [seconds]
AVG_TIME=10

#Number of readings to average over
AVG_COUNT=20

#Switch to night mode level
DAYNIGHT = 85

#GPIO pin to output day/night signal [-1 = GPIO output disabled]
DAYNIGHT_PIN = 15     

#If using day/night signal, setup GPIO
if DAYNIGHT_PIN != -1:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DAYNIGHT_PIN, GPIO.OUT)


#LUX READING----------------------------------------------------------------------

#i2c setup
BUS = 1
TSL2561_ADDR = 0x39     #the addresss of TSL2561 can be 0x29, 0x39 or 0x49

i2cBus = smbus.SMBus(BUS)

# Start messure with 402 ms
# (scale factor 1)
i2cBus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)

# Function for getting lux
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

    print(round(Lux,1))
    #return rounded lux value
    return round(Lux,1)


#LUX AVERAGING--------------------------------------------------------------------

#Setup empty list for lux values
LUX_VALUES=[]

#populate list with default brightness
i = 0
while i < AVG_COUNT:
    LUX_VALUES.append(BRIGHT_LVL)
    i+=1

#function for averaging lux
def avgLux(luxVal):
    #check if we have a full set of readings to average over
    if len(LUX_VALUES) == AVG_COUNT:
        #if so, delete oldest reading (otherwise, let it work up to AVG_COUNT)
        LUX_VALUES.pop(0)

    #add new lux value
    LUX_VALUES.append(luxVal)

    #return average of stored readings
    return sum(LUX_VALUES)/len(LUX_VALUES)


#SETTING BRIGHTNESS---------------------------------------------------------------

#function to calculate brightness
def calcBrightness(newLux):
    return(int(((BRIGHT_MAX-BRIGHT_MIN)*((avgLux(newLux)/400)**BRIGHT_CRV))+BRIGHT_MIN))

#function to set brightness
def setBrightness(newBright):
    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
    file.write(str(newBright))
    file.close()

    if DAYNIGHT_PIN != -1:
        if newBright <= DAYNIGHT:
            GPIO.output(DAYNIGHT_PIN, 1) #output night mode GPIO
        else:
            GPIO.output(DAYNIGHT_PIN, 0) #output day mode GPIO
    
    return newBright

#initial brightness
BRIGHT_LVL = setBrightness(calcBrightness(getLux()))


#START LOOPING--------------------------------------------------------------------

while True:
    
    BRIGHT_NEW = calcBrightness(getLux())

    print(BRIGHT_NEW)
    
    if BRIGHT_NEW != BRIGHT_LVL:

        BRIGHT_LVL = setBrightness(BRIGHT_NEW)

    sleep(AVG_TIME/AVG_COUNT)