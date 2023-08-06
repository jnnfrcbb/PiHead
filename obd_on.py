import sys
import RPi.GPIO as GPIO
import time

time.sleep(10)

GPIO.output(sys.argv[1], 1)