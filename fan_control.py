##Based on Michael Klements's code found here: https://github.com/mklements/PWMFanControl/blob/main/FanProportional.py

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

fanGPIO = 18 ##GPIO 12, 13, 18, 19 = hardware PWM

GPIO.setup(fanGPIO,GPIO.OUT)
fan = GPIO.PWM(fanGPIO,100)
fan.start(50)

minTemp = 25
maxTemp = 80
minSpeed = 0
maxSpeed = 100

def get_temp():                             # Function to read in the CPU temperature and return it as a float in degrees celcius
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        return int(maxTemp)
        #raise RuntimeError('Could not get temperature')
    
def renormalize(n, range1, range2):         # Function to scale the read temperature to the fan speed range
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]

while True:                                    # Execute loop forever
    temp = get_temp()                       # Get the current CPU temperature
    if temp < minTemp:                      # Constrain temperature to set range limits
        temp = minTemp
    elif temp > maxTemp:
        temp = maxTemp
    newSpeed = int(renormalize(temp, [minTemp, maxTemp], [minSpeed, maxSpeed]))
    print(temp + " : " + newSpeed)
    fan.ChangeDutyCycle(newSpeed)               # Set fan duty based on temperature, from minSpeed to maxSpeed
    time.sleep(5)                           # Sleep for 5 seconds