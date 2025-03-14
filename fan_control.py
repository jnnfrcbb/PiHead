##PWM control based on Michael Klements's code found here: https://github.com/mklements/PWMFanControl/blob/main/FanProportional.py
##RPM reading based on DriftKingTW's code found here: https://blog.driftking.tw/en/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

minTemp = 25
maxTemp = 80
defSpeed = 50
minSpeed = 0
maxSpeed = 100

pwmGPIO = 18 ##GPIO 12, 13, 18, 19 = hardware PWM


# Setup PWM pin
GPIO.setup(pwmGPIO,GPIO.OUT)
fan = GPIO.PWM(pwmGPIO,100)
fan.start(defSpeed)


# Read CPU temperature and return it as a float in degrees celcius
def get_temp():                             
    output = open('/sys/class/thermal/thermal_zone0/temp', 'r')
    defSpeed = int(output.read())/1000
    output.close()

    return defSpeed


# Scale the read temperature to the fan speed range
def renormalize(n, range1, range2):         
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]


while True:
    
    temp =  get_temp()                       # Get the current CPU temperature

    if temp < minTemp:                      # Constrain temperature to set range limits
        temp = minTemp
    elif temp > maxTemp:
        temp = maxTemp
    newSpeed = int(renormalize(temp, [minTemp, maxTemp], [minSpeed, maxSpeed]))

    print(str(temp) + " : " + str(newSpeed))
            
    fan.ChangeDutyCycle(newSpeed)    # Set fan duty based on temperature, from minSpeed to maxSpeed

    time.sleep(5)