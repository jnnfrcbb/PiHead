import RPi.GPIO as GPIO
import time
import threading

CLK = 16
DT = 20
SW = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW,GPIO.IN,pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(CLK)
dtLastState = GPIO.input(DT)

try:

    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)

        if clkState != clkLastState:
            if dtState !=clkState:
                print("down")
            else:
                print("up")
        
        clkLastState = clkState

        time.sleep(0.1)

except:
    print("An exception occurred")

finally:
    GPIO.cleanup()