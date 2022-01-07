#import os


#turn screen on:
#os.system("sudo bash -c echo 0 > /sys/class/backlight/rpi_backlight/bl_power")

backlight = open('/sys/class/backlight/rpi_backlight/bl_power', 'w')
print (backlight)
#backlight.write('1') # turn on
#backlight.write('0') # turn off


#turn screen off:
#os.system("sudo bash -c echo 255 > /sys/class/backlight/rpi_backlight/bl_power")

#todo: read current state pause; playback when screen off; bind hotkey to run script