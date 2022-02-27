
# Originally Used in Crankshaft.
# Kudos to the guys at Crankshaft for giving me a headstart for controlling the  brightness using the TSL2561
#
# GPIO Trigger for Day/Night
# GPIO wich triggers Day (open gpio)/Night (closed to gnd) of GUI
# To disable set to 0
# If enabled it overrides lightsensor!
DAYNIGHT_PIN=0

### Screen ###
# Brightness related stuff
# brightness file (default for rpi display: /sys/class/backlight/rpi_backlight/brightness)
BRIGHTNESS_FILE=/sys/class/backlight/rpi_backlight/brightness

# brightness values
BR_MIN=25
BR_MAX=255
BR_STEP=25
BR_DAY=255
BR_NIGHT=25

# Custom brightness control
# Note: this command is called after every brightness change - can slow down for example the brightness
# slider depending on execution speed - the process is called with "&" so call is not waiting for exit!
# Sample call which will be executed on request: "CUSTOM_BRIGHTNESS_COMMAND brightnessvalue &"
#
# Note: To allow backup and restore your command must be located on /boot/crankshaft/custom/
# otherwise it will not be transfered during updates!
#
# To disable leave empty
CUSTOM_BRIGHTNESS_COMMAND=

# Auto brightness control based on tsl2561 light sensor
# Check interval sensor 5,10,15,20,25,30
TSL2561_CHECK_INTERVAL=5
# Switch to night on this level or lower (0 = disabled / 1-10)
TSL2561_DAYNIGHT_ON_STEP=5
# Switch levels for brightness sensor in lux
LUX_LEVEL_1=0.1     #5
LUX_LEVEL_2=0.5     #20
LUX_LEVEL_3=1       #80
LUX_LEVEL_4=20      #180
LUX_LEVEL_5=50      #250
LUX_LEVEL_6=100     #300
LUX_LEVEL_7=150     #350
LUX_LEVEL_8=200     #400
LUX_LEVEL_9=300     #450
LUX_LEVEL_10=400    #500
# Set this display brightness by switch levels
DISP_BRIGHTNESS_1=25 #30
DISP_BRIGHTNESS_2=40 #90
DISP_BRIGHTNESS_3=70 #150
DISP_BRIGHTNESS_4=105 #210
DISP_BRIGHTNESS_5=135 #255
DISP_BRIGHTNESS_6=160
DISP_BRIGHTNESS_7=185
DISP_BRIGHTNESS_8=210
DISP_BRIGHTNESS_9=235
DISP_BRIGHTNESS_10=255