import board
import neopixel

##neopixel library: "sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel"

pixelCount = 8

pixels = neopixel.NeoPixel(board.D18, pixelCount, brightness=0.5)
pixels.fill((255, 165, 0))