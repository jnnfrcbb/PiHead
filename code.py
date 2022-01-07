import board
from analogio import AnalogIn
##import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time
import neopixel

#setup RGB strip
pixelCount = 10
pixels = neopixel.NeoPixel(board.D2, pixelCount, brightness=0.75)
pixels.fill((255, 50, 0))

#setup analog inputs
analog0in = AnalogIn(board.D0)
analog1in = AnalogIn(board.D1)

#setup keyboard
kbd = Keyboard()#usb_hid.devices)

#setup voltage reader
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

while True:

  VD0 = getVoltage(analog0in) #AD
  VD1 = getVoltage(analog1in) #SHIFT

  if VD1 > 1:
    #print("SHIFT: FALSE")
    if VD0 < 0.1:
      print("BUTTON: OFF")
      kbd.send(Keycode.H)  #HOME
    elif VD0 < 0.7:
      print("BUTTON: SOURCE")
      kbd.send(Keycode.M)  #VOICE
    elif VD0 < 1.1:
      print("BUTTON: ATT")
      kbd.send(Keycode.CONTROL, Keycode.F3) #SWITCH MODE      
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
      kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #todo: run python script to turn screen off and on / alternatively: switch day-night mode
  elif VD1 < 1:
    #print("SHIFT: TRUE")
    if VD0 < 1.6:
      print("BUTTON: SHIFTUP")
      kbd.send(Keycode.J)  #LAUNCH MEDIA
    elif VD0 < 1.9:
      print("BUTTON: SHIFTDOWN")
      kbd.send(Keycode.F) #LAUNCH NAVIGATION

  time.sleep(0.25)