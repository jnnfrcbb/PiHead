import board
from analogio import AnalogIn
#import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time
import neopixel
import adafruit_dotstar as dotstar

red = 255
green = 75 #35
blue = 0

#####################
## SETUP RGB STRIP ##
#####################

rgbCount = 10

rgb = neopixel.NeoPixel(board.D2, rgbCount, brightness=0.25) #0.33)
rgb.fill((red, green, blue))


#######################
## SETUP ONBOARD LED ##
#######################

led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
led[0] = (255,0,0)


#########################
## SETUP ANALOG INPUTS ##
#########################

analog0in = AnalogIn(board.D0)
analog1in = AnalogIn(board.D1)

led[0] = (0,255,0)


####################
## SETUP KEYBOARD ##
####################

kbd = Keyboard() #usb_hid.devices)

led[0] = (0,0,255)


##########################
## SETUP VOLTAGE READER ##
##########################

def getVoltage(pin):
    return float((pin.value * 3.3) / 65536)
  
led[0] = (255,255,255)


####################
## PROCESS INPUTS ##
####################

while True:

  rgb.fill((red, green, blue))

  led[0] = (0,0,0)

  VD0 = getVoltage(analog0in) #AD
  VD1 = getVoltage(analog1in) #SHIFT

  bButton = False

  print(VD0)

  if VD1 > 1:
    print("SHIFT: FALSE")
    if VD0 < 0.1:
      print("BUTTON: OFF")
      kbd.send(Keycode.H)  #HOME
      bButton = True
    elif VD0 < 0.7:
      print("BUTTON: SOURCE")
      kbd.send(Keycode.M)  #VOICE
      bButton = True
    elif VD0 < 0.7:
      print("BUTTON: SOURCE")
      kbd.send(Keycode.M)  #VOICE
      bButton = True
    elif VD0 < 1.1:
      print("BUTTON: ATT")
      kbd.send(Keycode.CONTROL, Keycode.F3) #SWITCH MODE      
      bButton = True
    elif VD0 < 1.4:
      print("BUTTON: LIST")
      kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
      bButton = True
    elif VD0 < 1.65:
      print("BUTTON: SEEK+")
      kbd.send(Keycode.N)  #NEXT TRACK
      bButton = True
    elif VD0 < 1.9:
      print("BUTTON: SEEK-")
      kbd.send(Keycode.V)  #PREVIOUS TRACK
      bButton = True
    elif VD0 < 2.15:
      print("BUTTON: VOL+")
      kbd.send(Keycode.F8) #VOLUME up
      bButton = True
    elif VD0 < 2.4:
      print("BUTTON: VOL-")
      kbd.send(Keycode.F7) #VOLUME DOWN
      bButton = True
    elif VD0 < 2.6:
      print("BUTTON: SEL")
      kbd.send(Keycode.B)  #PLAY/PAUSE
      bButton = True
    elif VD0 < 2.8:
      print("BUTTON: MODE")
      kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
      bButton = True
  elif VD1 < 1:
    print("SHIFT: TRUE")
    if VD0 < 1.6:
      print("BUTTON: SHIFTUP")
      kbd.send(Keycode.J)  #LAUNCH MEDIA
      bButton = True
    elif VD0 < 1.9:      
      print("BUTTON: SHIFTDOWN")
      kbd.send(Keycode.F) #LAUNCH NAVIGATION
      bButton = True

  if bButton == True:
    led[0] = (red, green, blue)

  time.sleep(0.1)