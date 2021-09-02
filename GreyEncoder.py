from encoder import PIN_A, PIN_B
import RPi.GPIO as GPIO

PIN_A = 17
PIN_B = 27
PIN_SW = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW,GPIO.IN,pull_up_down=GPIO.PUD_UP)