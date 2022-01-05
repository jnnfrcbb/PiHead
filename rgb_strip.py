import board #RPi.GPIO as GPIO
import neopixel

##neopixel library: "sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel"
##blinka library: "sudo python3 -m pip install --force-reinstall adafruit-blinka"

pixelCount = 8

pixels = neopixel.NeoPixel(board.18, pixelCount, brightness=0.5)
pixels.fill((255, 165, 0))