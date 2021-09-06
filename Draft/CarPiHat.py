import RPi.GPIO as GPIO # import our GPIO module
import time
from subprocess import call

GPIO.setmode(GPIO.BCM) # we are using BCM pin numbering

IGN_PIN = 12		# our 12V switched pin is BCM12
EN_POWER_PIN = 25	# our latch pin is BCM25

IGN_LOW_TIME = 10 # time (s) before a shutdown is initiated after power loss

GPIO.setup(IGN_PIN, GPIO.IN) # set our 12V switched pin as an input

GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH) # set our latch as an output

GPIO.output(EN_POWER_PIN, 1) # latch our power. We are now in charge of switching power off

ignLowCounter = 0

while ignLowCounter < (IGN_LOW_TIME+1):
	if GPIO.input(IGN_PIN) != 1:				# if our 12V switched is not disabled
		time.sleep(1)							# wait a second
		ignLowCounter += 1						# increment our counter
		print(ignLowCounter)
		if ignLowCounter > IGN_LOW_TIME:		# if it has been switched off for >10s
			print("Shutting Down")
			call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down
	else:
		ignLowCounter = 0 						# reset our counter, 12V switched is HIGH again