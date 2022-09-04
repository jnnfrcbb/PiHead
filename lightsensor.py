#!/usr/bin/python3 -u

#Based on code from this thread by PlasmaFlow: https://bluewavestudio.io/community/showthread.php?tid=672

from inspect import modulesbyfile
import smbus
import os
import subprocess
from time import sleep
import RPi.GPIO as GPIO


#constants------------------------------------------------------------------------

# Switch levels for brightness sensor in lux
LUX_LEVEL_1=0.1     #5
LUX_LEVEL_2=0.5     #20
LUX_LEVEL_3=1       #80
LUX_LEVEL_4=20      #180
LUX_LEVEL_5=50      #250
LUX_LEVEL_6=100     #300
LUX_LEVEL_7=150     #350
LUX_LEVEL_8=200     #400
LUX_LEVEL_9=300     #450
LUX_LEVEL_10=400    #500

# Set this display brightness by switch levels
DISP_BRIGHTNESS_0=23 #30
DISP_BRIGHTNESS_1=46 #30
DISP_BRIGHTNESS_2=69 #90
DISP_BRIGHTNESS_3=92 #150
DISP_BRIGHTNESS_4=115 #210
DISP_BRIGHTNESS_5=138 #255
DISP_BRIGHTNESS_6=161
DISP_BRIGHTNESS_7=184
DISP_BRIGHTNESS_8=207
DISP_BRIGHTNESS_9=230
DISP_BRIGHTNESS_10=255

# Check interval sensor 5,10,15,20,25,30
TSL2561_CHECK_INTERVAL=5

# Switch to night on this level or lower (-1 = disabled / 0-10)
TSL2561_DAYNIGHT_ON_STEP=4


#day/night switching--------------------------------------------------------------

OUT_PIN = 15
DAYNIGHT_GPIO = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_PIN, GPIO.OUT)


#I2C setup------------------------------------------------------------------------

BUS = 1
TSL2561_ADDR = 0x39     #the addresss of TSL2561 can be 0x29, 0x39 or 0x49

i2cBus = smbus.SMBus(BUS)

# Start messure with 402 ms
# (scale factor 1)
i2cBus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)
lastvalue = 0


#---------------------------------------------------------------------------------

while True:
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
    # Calc visible spectrum
    Visible = Ambient - Infrared
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

    Luxrounded = round(Lux,1)
    if lastvalue != Luxrounded:
        print ("Lux = {}\n".format(Luxrounded))
        os.system("echo {} > /tmp/tsl2561".format(Luxrounded))
        lastvalue = Luxrounded

    if Luxrounded <= LUX_LEVEL_1:
        step = 0
        new_brightness = DISP_BRIGHTNESS_0
    elif Luxrounded > LUX_LEVEL_1 and Luxrounded <= LUX_LEVEL_2:
        step = 1
        new_brightness = DISP_BRIGHTNESS_1
    elif Luxrounded > LUX_LEVEL_2 and Luxrounded <= LUX_LEVEL_3:
        step = 2
        new_brightness = DISP_BRIGHTNESS_2
    elif Luxrounded > LUX_LEVEL_3 and Luxrounded <= LUX_LEVEL_4:
        step = 3
        new_brightness = DISP_BRIGHTNESS_3
    elif Luxrounded > LUX_LEVEL_4 and Luxrounded <= LUX_LEVEL_5:
        step = 4
        new_brightness = DISP_BRIGHTNESS_4
    elif Luxrounded > LUX_LEVEL_5 and Luxrounded <= LUX_LEVEL_6:
        step = 5
        new_brightness = DISP_BRIGHTNESS_5
    elif Luxrounded > LUX_LEVEL_6 and Luxrounded <= LUX_LEVEL_7:
        step = 6
        new_brightness = DISP_BRIGHTNESS_6
    elif Luxrounded > LUX_LEVEL_7 and Luxrounded <= LUX_LEVEL_8:
        step = 7
        new_brightness = DISP_BRIGHTNESS_7
    elif Luxrounded > LUX_LEVEL_8 and Luxrounded <= LUX_LEVEL_9:
        step = 8
        new_brightness = DISP_BRIGHTNESS_8
    elif Luxrounded > LUX_LEVEL_9 and Luxrounded <= LUX_LEVEL_10:
        step = 9
        new_brightness = DISP_BRIGHTNESS_9
    elif Luxrounded > LUX_LEVEL_9:
        step = 10
        new_brightness = DISP_BRIGHTNESS_10

    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
    file.write(str(new_brightness))
    file.close()

    if DAYNIGHT_GPIO == 0:
        if step <= TSL2561_DAYNIGHT_ON_STEP:
            print("Lux = {} | ".format(Luxrounded) + "Level " + str(step) + " -> trigger night")
            os.system("touch /tmp/night_mode_enabled >/dev/null 2>&1")
            GPIO.output(OUT_PIN, 1) ## output signal on GPIO to say night mode should activate
        else:
            if step > TSL2561_DAYNIGHT_ON_STEP:
                print("Lux = {} | ".format(Luxrounded) + "Level " + str(step) + " -> trigger day")
                os.system("sudo rm /tmp/night_mode_enabled >/dev/null 2>&1")
                GPIO.output(OUT_PIN, 0) ## output signal on GPIO to say day mode should activate

    sleep (TSL2561_CHECK_INTERVAL)