import board
import time
import usb_hid
import neopixel
import digitalio
from analogio import AnalogIn
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

######################
## SETUP RGB STRIPS ##
######################

pins=[board.GP16,board.GP17,board.GP18,board.GP19]
rgb_count=[9,10,10,10]
bright_day=[0.25,0.25,0.5,0.5]
bright_night=[0.1,0.1,0.1,0.1]

colour=[255,40,0]

#DAY NIGHT SWITCH
dn_switch = digitalio.DigitalInOut(board.GP22)
dn_switch.switch_to_input(pull=digitalio.Pull.DOWN)

#LIGHTING
i=0

#populate strips
pixels=[]
while i<len(pins):
    pixels.append(neopixel.NeoPixel(pins[i], rgb_count[i]))
    i=i+1


####################
## SETUP KEYBOARD ##
####################

kbd = Keyboard(usb_hid.devices)

#########################
## SETUP ANALOG INPUTS ##
#########################

analog0in = AnalogIn(board.GP26)
analog1in = AnalogIn(board.GP27)


##########################
## SETUP VOLTAGE READER ##
##########################

boardVCC = 3.3

def getVoltage(pin):
    return float((pin.value * boardVCC) / 65536)


####################
## PROCESS INPUTS ##
####################

while True:

  VD0 = getVoltage(analog0in) #AD
  VD1 = getVoltage(analog1in) #SHIFT

  print(VD0)

  if VD1 > 1:
    #print("SHIFT: FALSE")
    if VD0 < 0.1:
      print("BUTTON: MODE (SWITCH MODE)")
      kbd.send(Keycode.CONTROL, Keycode.F3)  #SWITCH MODE
    elif VD0 < 0.7:
      print("BUTTON: SOURCE (VOICE)")
      kbd.send(Keycode.M)  #VOICE
    elif VD0 < 1.1:
      print("BUTTON: ATT (HOME)")
      kbd.send(Keycode.H) #HOME
    elif VD0 < 1.4:
      print("BUTTON: LIST (MUTE)")
      kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
    elif VD0 < 1.65:
      print("BUTTON: SEEK+ (NEXT)")
      kbd.send(Keycode.N)  #NEXT TRACK
    elif VD0 < 1.9:
      print("BUTTON: SEEK- (PREVIOUS)")
      kbd.send(Keycode.V)  #PREVIOUS TRACK
    elif VD0 < 2.15:
      print("BUTTON: VOL+ (VOLUME UP)")
      kbd.send(Keycode.F8) #VOLUME up
    elif VD0 < 2.4:
      print("BUTTON: VOL- (VOLUME DOWN)")
      kbd.send(Keycode.F7) #VOLUME DOWN
    elif VD0 < 2.6:
      print("BUTTON: SEL (PLAY/PAUSE)")
      kbd.send(Keycode.B)  #PLAY/PAUSE
    elif VD0 < 2.8:
      print("BUTTON: OFF (SCREEN)")
      kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
  elif VD1 < 1:
    print("SHIFT: TRUE")
    if VD0 >= 1.4 and VD0 < 1.6:
      print("BUTTON: SHIFTUP (MEDIA)")
      kbd.send(Keycode.J)  #LAUNCH MEDIA
    elif VD0 < 1.9:      
      print("BUTTON: SHIFTDOWN (NAVIGATION)")
      kbd.send(Keycode.F) #LAUNCH NAVIGATION
    
  #light strips
  i=0
  while i<len(pins):
      if dn_switch.value:
          pixels[i].brightness = bright_night[i]
      else:
          pixels[i].brightness = bright_day[i]
      pixels[i].fill((colour[0], colour[1], colour[2]))
      i=i+1

  time.sleep(0.15)