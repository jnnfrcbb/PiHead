import board
import neopixel

pixelCount = 8

pixels = neopixel.NeoPixel(board.D18, 8) ##number = pixel count
pixels.fill((0, 255, 0))