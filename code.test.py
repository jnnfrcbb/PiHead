import board
from analogio import AnalogIn
import time

#setup onboard led
led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
led[0] = (0,0,0)

#setup analog inputs
analog0in = AnalogIn(board.D0)
analog1in = AnalogIn(board.D1)

#setup voltage reader
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

while True:

  VD0 = getVoltage(analog0in) #AD
  VD1 = getVoltage(analog1in) #SHIFT

  bButton = False

  if VD1 > 1:
    #print("SHIFT: FALSE")
    if VD0 < 0.1:
      print("BUTTON: OFF")
      bButton = True
    elif VD0 < 0.7:
      print("BUTTON: SOURCE")
      bButton = True
    elif VD0 < 1.1:
      print("BUTTON: ATT")
      bButton = True
    elif VD0 < 1.4:
      print("BUTTON: LIST")
      bButton = True
    elif VD0 < 1.65:
      print("BUTTON: SEEK+")
      bButton = True
    elif VD0 < 1.9:
      print("BUTTON: SEEK-")
      bButton = True
    elif VD0 < 2.15:
      print("BUTTON: VOL+")
      bButton = True
    elif VD0 < 2.4:
      print("BUTTON: VOL-")
      bButton = True
    elif VD0 < 2.6:
      print("BUTTON: SEL")
      bButton = True
    elif VD0 < 2.8:
      print("BUTTON: MODE")
      bButton = True
  elif VD1 < 1:
    if VD0 < 1.6:
      print("BUTTON: SHIFTUP")
      bButton = True
    elif VD0 < 1.9:
      print("BUTTON: SHIFTDOWN")
      bButton = True

  if bButton == True:
    led[0] = (255,35,0)

  time.sleep(0.25)

  led[0] = (0,0,0)