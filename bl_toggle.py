bl_status = open("/sys/class/backlight/rpi_backlight/bl_power", "r")
bl_Status = (bl_status.read())
bl_status.close()

print(bl_Status)

if bl_Status == 0:
    backlight = open('/sys/class/backlight/rpi_backlight/bl_power', 'w')
    backlight.write('1') # turn on
    backlight.close()
elif bl_Status == 1:
    backlight = open('/sys/class/backlight/rpi_backlight/bl_power', 'w')
    backlight.write('0') # turn off
    backlight.close()