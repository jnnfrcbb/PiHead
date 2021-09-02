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

counter =0

clkLastState = GPIO.input(CLK)
dtLastState = GPIO.input(DT)

try:

    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)

        if clkState != clkLastState:
            if dtState !=clkState:
                counter = -1
            else:
                counter = 1
            print (counter)
        
        clkLastState = clkState

        time.sleep(0.05)

except:
    print("An exception occurred")

finally:
    GPIO.cleanup()