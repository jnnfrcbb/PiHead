import board
from analogio import AnalogIn
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time
import neopixel
import adafruit_dotstar as dotstar

red = 255
green = 40
blue = 0

fpanelBrightness = 0.3
doorBrightness = 0.25


#######################
## SETUP ONBOARD LED ##
#######################

led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
led[0] = (red,green,blue)


#################################
## SETUP FRONT PANEL RGB STRIP ##
#################################

rgbCount = 10

rgb = neopixel.NeoPixel(board.D2, rgbCount, brightness=fpanelBrightness)
rgb.fill((red, green, blue))


####################
## SETUP KEYBOARD ##
####################

kbd = Keyboard() #usb_hid.devices)


#########################
## SETUP ANALOG INPUTS ##
#########################

analog0in = AnalogIn(board.D0)
analog1in = AnalogIn(board.D1)


##########################
## SETUP VOLTAGE READER ##
##########################

def getVoltage(pin):
    return float((pin.value * 3.3) / 65536)


####################
## PROCESS INPUTS ##
####################

while True:

  VD0 = getVoltage(analog0in) #AD
  VD1 = getVoltage(analog1in) #SHIFT

  print(VD0)

  if VD1 > 1:
    print("SHIFT: FALSE")
    if VD0 < 0.1:
      print("BUTTON: OFF")
      kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
    elif VD0 < 0.7:
      print("BUTTON: SOURCE")
      kbd.send(Keycode.M)  #VOICE
    elif VD0 < 1.1:
      print("BUTTON: ATT")
      kbd.send(Keycode.H) #HOME
    elif VD0 < 1.4:
      print("BUTTON: LIST")
      kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
    elif VD0 < 1.65:
      print("BUTTON: SEEK+")
      kbd.send(Keycode.N)  #NEXT TRACK
    elif VD0 < 1.9:
      print("BUTTON: SEEK-")
      kbd.send(Keycode.V)  #PREVIOUS TRACK
    elif VD0 < 2.15:
      print("BUTTON: VOL+")
      kbd.send(Keycode.F8) #VOLUME up
    elif VD0 < 2.4:
      print("BUTTON: VOL-")
      kbd.send(Keycode.F7) #VOLUME DOWN
    elif VD0 < 2.6:
      print("BUTTON: SEL")
      kbd.send(Keycode.B)  #PLAY/PAUSE
    elif VD0 < 2.8:
      print("BUTTON: MODE")
      kbd.send(Keycode.CONTROL, Keycode.F3)  #SWITCH MODE
  elif VD1 < 1:
    print("SHIFT: TRUE")
    if VD0 >= 1.4 and VD0 < 1.6:
      print("BUTTON: SHIFTUP")
      kbd.send(Keycode.J)  #LAUNCH MEDIA
    elif VD0 < 1.9:      
      print("BUTTON: SHIFTDOWN")
      kbd.send(Keycode.F) #LAUNCH NAVIGATION
    
  time.sleep(0.275)