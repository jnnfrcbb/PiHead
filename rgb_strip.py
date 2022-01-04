import board
import neopixel

##neopixel library: "sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel"

pixelCount = 8

pixels = neopixel.NeoPixel(board.D18, 8) ##number = pixel count
pixels.fill((255, 165, 0))