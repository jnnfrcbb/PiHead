#!/usr/bin/python3 -u

from inspect import modulesbyfile
import smbus
import os
import subprocess
from time import sleep
import RPi.GPIO as GPIO

## For auto day/night mode switching ##
# configure BCM mode so all numbers are GPIO pin number, not board pin number
GPIO.setmode(GPIO.BCM)
# setup GPIO15 to be an output
GPIO.setup(15, GPIO.OUT)
## use a jumper cable to connect output pin to OAP night mode detection pin



# Originally Used in Crankshaft.
# Kudos to the guys at Crankshaft for giving me a headstart for controlling the  brightness using the TSL2561
#
# This file was re written to write the brightness variable in /sys/class/backlight/rpi_backlight/brightness
# re written by PlasmaFlow 1/22/19

def get_var(varname):
    try:
        CMD = 'echo $(source /opt/lightsensor/lightsensor_env.sh; echo $%s)' % varname
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        return int(p.stdout.readlines()[0].strip())
    except:
        CMD = 'echo $(source /opt/lightsensor/lightsensor_default_env.sh; echo $%s)' % varname
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        return int(p.stdout.readlines()[0].strip())
# ---------------------------------
# the addresss of TSL2561 can be
# 0x29, 0x39 or 0x49
BUS = 1
TSL2561_ADDR = 0x39

daynight_gpio = get_var('DAYNIGHT_PIN')
# ---------------------------------
i2cBus = smbus.SMBus(BUS)

# Start messure with 402 ms
# (scale factor 1)
i2cBus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)
lastvalue = 0

while True:
# read global brightness read low byte
  LSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8C)
# read high byte
  MSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8D)
  Ambient = (MSB << 8) + LSB
#print ("Ambient: {}".format(Ambient))
# read infra red read low byte
  LSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8E)
# read high byte
  MSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8F)
  Infrared = (MSB << 8) + LSB
#print ("Infrared: {}".format(Infrared))
# Calc visible spectrum
  Visible = Ambient - Infrared
#print ("Visible: {}".format(Visible))
# Calc factor Infrared/Ambient
  Ratio = 0
  Lux = 0
  if Ambient != 0:
    Ratio = float(Infrared)/float(Ambient)
    #print ("Ratio: {}".format(Ratio))
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
    #Set display brigthness
#  if Luxrounded <= get_var('LUX_LEVEL_1'):
#    #os.system("xbacklight -set " + str(get_var('DISP_BRIGHTNESS_1')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write(str(get_var('DISP_BRIGHTNESS_1')))
#    file.close()
#    step = 1
#  elif Luxrounded > get_var('LUX_LEVEL_1') and Luxrounded <= get_var('LUX_LEVEL_2'):
#    #os.system("xbacklight -set " + str(get_var('DISP_BRIGHTNESS_2')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write(str(get_var('DISP_BRIGHTNESS_2')))
#    file.close()
#    step = 2
#  elif Luxrounded > get_var('LUX_LEVEL_2') and Luxrounded <= get_var('LUX_LEVEL_3'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_3')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write(str(get_var('DISP_BRIGHTNESS_3')))
#    file.close()
#    step = 3
#  elif Luxrounded > get_var('LUX_LEVEL_3') and Luxrounded <= get_var('LUX_LEVEL_4'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_4')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_4')))
#    file.close()
#    step = 4
#  elif Luxrounded > get_var('LUX_LEVEL_4') and Luxrounded <= get_var('LUX_LEVEL_5'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_5')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_5')))
#    file.close()
#    step = 5
#  elif Luxrounded > get_var('LUX_LEVEL_5') and Luxrounded <= get_var('LUX_LEVEL_6'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_6')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_6')))
#    file.close()
#    step = 6
#  elif Luxrounded > get_var('LUX_LEVEL_6') and Luxrounded <= get_var('LUX_LEVEL_7'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_7')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_7')))
#    file.close()
#    step = 7
#  elif Luxrounded > get_var('LUX_LEVEL_7') and Luxrounded <= get_var('LUX_LEVEL_8'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_8')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_8')))
#    file.close()
#    step = 8
#  elif Luxrounded > get_var('LUX_LEVEL_8') and Luxrounded <= get_var('LUX_LEVEL_9'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_9')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write( str(get_var('DISP_BRIGHTNESS_9')))
#    file.close()
#    step = 9
#  elif Luxrounded > get_var('LUX_LEVEL_9'):
#    #os.system("xbacklight -set  " + str(get_var('DISP_BRIGHTNESS_10')) + " &")
#    file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
#    file.write(str(get_var('DISP_BRIGHTNESS_10')))
#    file.close()
#    step = 10

  if Luxrounded <= get_var('LUX_LEVEL_1'):
    step = 1
  elif Luxrounded > get_var('LUX_LEVEL_1') and Luxrounded <= get_var('LUX_LEVEL_2'):
    step = 2
  elif Luxrounded > get_var('LUX_LEVEL_2') and Luxrounded <= get_var('LUX_LEVEL_3'):
    step = 3
  elif Luxrounded > get_var('LUX_LEVEL_3') and Luxrounded <= get_var('LUX_LEVEL_4'):
    step = 4
  elif Luxrounded > get_var('LUX_LEVEL_4') and Luxrounded <= get_var('LUX_LEVEL_5'):
    step = 5
  elif Luxrounded > get_var('LUX_LEVEL_5') and Luxrounded <= get_var('LUX_LEVEL_6'):
    step = 6
  elif Luxrounded > get_var('LUX_LEVEL_6') and Luxrounded <= get_var('LUX_LEVEL_7'):
    step = 7
  elif Luxrounded > get_var('LUX_LEVEL_7') and Luxrounded <= get_var('LUX_LEVEL_8'):
    step = 8
  elif Luxrounded > get_var('LUX_LEVEL_8') and Luxrounded <= get_var('LUX_LEVEL_9'):
    step = 9
  elif Luxrounded > get_var('LUX_LEVEL_9'):
    step = 10

  file = open("/sys/class/backlight/rpi_backlight/brightness", "w")
  brightLevel = str(get_var('DISP_BRIGHTNESS_' + step))
  file.write(brightLevel)
  file.close()
    
  writeValue(Luxrounded,brightLevel,step)

  if daynight_gpio == 0:
    if step <= get_var('TSL2561_DAYNIGHT_ON_STEP'):
      print("Lux = {} | ".format(Luxrounded) + "Level " + str(step) + " -> trigger night")
      os.system("touch /tmp/night_mode_enabled >/dev/null 2>&1")
      GPIO.output(15, 1) ## output signal on GPIO15 to say night mode should activate
    else:
      if step > get_var('TSL2561_DAYNIGHT_ON_STEP'):
        print("Lux = {} | ".format(Luxrounded) + "Level " + str(step) + " -> trigger day")
        os.system("sudo rm /tmp/night_mode_enabled >/dev/null 2>&1")
        GPIO.output(15, 0) ## output signal on GPIO15 to say day mode should activate
  sleep (get_var('TSL2561_CHECK_INTERVAL'))

  def writeValue(newLux,newBrightness,newStep):
    file = open("log.txt", "w")
    fileData = "Lux:" + newLux + " Step: " + newStep + "Value: " + newBrightness
    file.write(fileData)
    file.close()

