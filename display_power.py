import os


#turn screen on:
os.system("sudo bash -c echo 0 > /sys/class/backlight/rpi_backlight/bl_power")

#turn screen off:
os.system("sudo bash -c echo 255 > /sys/class/backlight/rpi_backlight/bl_power")

#todo: read current state pause; playback when screen off; bind hotkey to run script