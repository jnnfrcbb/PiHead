import board
import time
import usb_hid
import neopixel
import digitalio
import rotaryio
from analogio import AnalogIn
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


enable_dev= False
enable_enc = True
enable_whl = True
enable_rgb = True

######################
## SETUP RGB STRIPS ##
######################

if enable_rgb == True:

    pins=[board.GP16,board.GP17,board.GP18,board.GP19]
    rgb_count=[9,10,10,10]
    bright_day=[0.25,0.25,0.5,0.5]
    bright_night=[0.1,0.1,0.1,0.1]

    colour=[255,40,0]

    #DAY NIGHT SWITCH
    dn_switch = digitalio.DigitalInOut(board.GP22)
    dn_switch.switch_to_input(pull=digitalio.Pull.DOWN)

    #LIGHTING
    i=0

    #populate strips
    pixels=[]
    while i<len(pins):
        pixels.append(neopixel.NeoPixel(pins[i], rgb_count[i]))
        i=i+1
    
    
####################
## SETUP KEYBOARD ##
####################

kbd = Keyboard(usb_hid.devices)


###########################
## SETUP ROTARY enable_enc ##
###########################

if enable_enc == True:

    rot_timeout = 10
    btn_timeout = 4
    btn_long_press = 10

    #volume encoder
    vol_out = digitalio.DigitalInOut(board.GP12)
    vol_out.direction = digitalio.Direction.OUTPUT
    vol_out.value = True

    vol_enc = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
    vol_rot_limit = 1 #number of clicks to send command
    vol_last_pos = 0
    vol_direction = 0
    vol_rot_count = 0
    vol_timeout = -1

    vol_btn = digitalio.DigitalInOut(board.GP13) 
    vol_btn.direction = digitalio.Direction.INPUT
    vol_btn.direction = digitalio.Direction.INPUT

    vol_btn_state = None
    vol_btn_dbl = False
    vol_btn_count = -1
    vol_btn_long = -1

    #playback encoder
    pb_out = digitalio.DigitalInOut(board.GP8)
    pb_out.direction = digitalio.Direction.OUTPUT
    pb_out.value = True

    pb_enc = rotaryio.IncrementalEncoder(board.GP11, board.GP10)
    pb_rot_limit = 2 #number of clicks to send command
    pb_last_pos = 0
    pb_direction = 0
    pb_rot_count = 0
    pb_timeout = -1

    pb_btn = digitalio.DigitalInOut(board.GP9)
    pb_btn.direction = digitalio.Direction.INPUT
    pb_btn.direction = digitalio.Direction.INPUT

    pb_btn_state = None
    pb_btn_dbl = False
    pb_btn_count = -1
    pb_btn_long = -1

#########################
## SETUP ANALOG INPUTS ##
#########################

if enable_whl == True:

    analog0in = AnalogIn(board.GP26)
    analog1in = AnalogIn(board.GP27)


##########################
## SETUP VOLTAGE READER ##
##########################

if enable_whl == True:

    boardVCC = 3.3

    def getVoltage(pin):
        return float((pin.value * boardVCC) / 65536)


####################
## PROCESS INPUTS ##
####################

while True:

    ############################
    ## STEERING WHEEL CONTROL ##
    ############################

    if enable_whl == True:

        VD0 = getVoltage(analog0in) #AD
        VD1 = getVoltage(analog1in) #SHIFT
        
        if enable_dev == True:
            print(VD0)

        if VD1 > 1:
            if VD0 < 0.03: #< 0.1:
                if enable_dev== True:
                    print("BUTTON: MODE (SWITCH MODE)")
                else:
                    kbd.send(Keycode.CONTROL, Keycode.F3)  #SWITCH MODE
            elif VD0 > 0.5 and VD0 < 0.62: #< 0.7:
                if enable_dev== True:
                    print("BUTTON: SOURCE (VOICE)")
                else:
                    kbd.send(Keycode.M)  #VOICE
            elif VD0 > 1 and VD0 < 1.05: #1.1:
                if enable_dev== True:
                    print("BUTTON: ATT (HOME)")
                else:
                    kbd.send(Keycode.H) #HOME
            elif VD0 >1.3 and VD0 < 1.35: #< 1.4:
                if enable_dev== True:
                    print("BUTTON: LIST (MUTE)")
                else:
                    kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
            elif VD0 > 1.5 and VD0 < 1.6: #< 1.65:
                if enable_dev== True:
                    print("BUTTON: SEEK+ (NEXT)")
                else:
                    kbd.send(Keycode.N)  #NEXT TRACK
            elif VD0 > 1.8 and VD0 < 1.85: #< 1.9:
                if enable_dev== True:
                    print("BUTTON: SEEK- (PREVIOUS)")
                else:
                    kbd.send(Keycode.V)  #PREVIOUS TRACK
            elif VD0 > 2 and VD0 < 2.1: #< 2.15:
                if enable_dev== True:
                    print("BUTTON: VOL+ (VOLUME UP)")
                else:
                    kbd.send(Keycode.F8) #VOLUME UP
            elif VD0 > 2.3 and VD0 < 2.35: #< 2.4:
                if enable_dev== True:
                    print("BUTTON: VOL- (VOLUME DOWN)")
                else:
                    kbd.send(Keycode.F7) #VOLUME DOWN
            elif VD0 > 2.5 and VD0 < 2.55: #< 2.6:
                if enable_dev== True:
                    print("BUTTON: SEL (PLAY/PAUSE)")
                else:
                    kbd.send(Keycode.B)  #PLAY/PAUSE
            elif VD0 > 2.7 and VD0 < 2.75: #< 2.8:
                if enable_dev== True:
                    print("BUTTON: OFF (SCREEN)")
                else:
                    kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
        elif VD1 < 1:
            if VD0 > 1:
                print("SHIFT: TRUE")
                if VD0 >= 1.5 and VD0 < 1.6:
                    if enable_dev== True:
                        print("BUTTON: SHIFTUP (MEDIA)")
                    else:
                        kbd.send(Keycode.J)  #LAUNCH MEDIA
                elif VD0 > 1.8 and VD0 < 1.85: #< 1.9:
                    if enable_dev== True: 
                        print("BUTTON: SHIFTDOWN (NAVIGATION)")
                    else:
                        kbd.send(Keycode.F) #LAUNCH NAVIGATION
    
    ##############
    ## ENCODERS ##
    ##############

    if enable_enc == True:
    
        #volume encoder
        
        vol_pos = vol_enc.position
        if vol_pos != vol_last_pos:
            if vol_pos > vol_last_pos:
                if vol_direction == -1: #reset direction if changed
                    vol_rot_count = 1
                else:
                    vol_rot_count +=1
                if vol_rot_count == vol_rot_limit:
                    vol_rot_count = 0
                    vol_direction = 0
                    vol_timeout = -1
                    if enable_dev== True:
                        print ("volume up")
                    else:
                        kbd.send(Keycode.F8) #VOLUME UP
                else:
                    vol_timeout = 0
                    vol_direction = 1
                vol_last_pos = vol_pos
            elif vol_pos < vol_last_pos:
                if vol_direction == 1: #reset direction if changed
                    vol_rot_count = 1
                else:
                    vol_rot_count +=1
                if vol_rot_count == vol_rot_limit:
                    vol_rot_count = 0
                    vol_direction = 0
                    vol_timeout = -1
                    if enable_dev== True:
                        print ("volume down")
                    else:
                        
                        kbd.send(Keycode.F7) #VOLUME DOWN
                else:
                    vol_timeout = 0
                    vol_direction = -1
                vol_last_pos = vol_pos
            
        if vol_timeout >= 0 and vol_timeout < rot_timeout:
            vol_timeout +=1
        elif vol_timeout == rot_timeout:
            vol_enc.position = 0
            vol_last_pos = 0
            vol_rot_count = 0
            vol_timeout = -1
            if enable_dev== True:
                print("timeout vol rotary")
          
        if not vol_btn.value and vol_btn_state is None:
            vol_btn_state = "pressed"
            vol_btn_long = 0
        elif vol_btn.value and vol_btn_state == -1:
            vol_btn_state = None
        if vol_btn.value and vol_btn_state == "pressed":
            if vol_btn_dbl == False:
                vol_btn_dbl = True
                vol_btn_count = 0
            elif vol_btn_dbl == True:
                if enable_dev== True:
                    print("vol_double")
                else:              
                    kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
                vol_btn_dbl = False
                vol_btn_count = -1
                vol_btn_long = -1
            vol_btn_state = None

        if vol_btn_count >= 0 and vol_btn_count < btn_timeout:
            vol_btn_count += 1
            if enable_dev== True:
                print(vol_btn_count)
        elif vol_btn_count == btn_timeout:
            if enable_dev== True:
                print ("vol_single")        
            else:                 
                kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
            vol_btn_state = None
            vol_btn_dbl = False
            vol_btn_count = -1
            vol_btn_long = -1
            
        if vol_btn_long >= 0 and vol_btn_long < btn_long_press:
            vol_btn_long +=1
            if enable_dev == True:
                print(vol_btn_long)
            if vol_btn_long == btn_long_press:
                vol_btn_state = -1
                vol_btn_dbl = False
                vol_btn_count = -1                
                vol_btn_long = -1
                if enable_dev == True:
                    print("vol long press")
                else:
                    kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.R) #REBOOT
        
        #playback encoder
        
        pb_pos = pb_enc.position
        if pb_pos != pb_last_pos:
            if pb_pos > pb_last_pos:
                if pb_direction == -1: #reset direction if changed
                    pb_rot_count = 1
                else:
                    pb_rot_count +=1
                if pb_rot_count == pb_rot_limit:
                    pb_rot_count = 0
                    pb_direction = 0
                    pb_timeout = -1
                    if enable_dev== True:
                        print ("next") 
                    else:
                        kbd.send(Keycode.N)  #NEXT TRACK
                else:
                    pb_timeout = 0
                    pb_direction = 1
                pb_last_pos = pb_pos
            elif pb_pos < pb_last_pos:
                if pb_direction == 1: #reset direction if changed
                    pb_rot_count = 1
                else:
                    pb_rot_count +=1
                if pb_rot_count == pb_rot_limit:
                    pb_rot_count = 0
                    pb_direction = 0
                    pb_timeout = -1
                    if enable_dev== True:
                        print ("previous")
                    else:
                        kbd.send(Keycode.V)  #PREVIOUS TRACK
                else:
                    pb_timeout = 0
                    pb_direction = -1
                pb_last_pos = pb_pos
            
        if pb_timeout >= 0 and pb_timeout < rot_timeout:
            pb_timeout +=1
        elif pb_timeout == rot_timeout:
            pb_enc.position = 0
            pb_last_pos = 0
            pb_rot_count = 0
            pb_timeout = -1
            if enable_dev== True:
                print("timeout pb rotary")
          
        if not pb_btn.value and pb_btn_state is None:
            pb_btn_state = "pressed"
            pb_btn_long = 0
        elif pb_btn.value and pb_btn_state == -1:
            pb_btn_state = None
        if pb_btn.value and pb_btn_state == "pressed":
            if pb_btn_dbl == False:
                pb_btn_dbl = True
                pb_btn_count = 0
            elif pb_btn_dbl == True:
                if enable_dev== True:
                    print("pb_double")
                else:
                    kbd.send(Keycode.J)  #LAUNCH MEDIA
                pb_btn_dbl = False
                pb_btn_count = -1
                pb_btn_long = -1
            pb_btn_state = None

        if pb_btn_count >= 0 and pb_btn_count < btn_timeout:
            pb_btn_count += 1
            if enable_dev== True:
                print(pb_btn_count)
        elif pb_btn_count == btn_timeout:
            if enable_dev== True:
                print ("pb_single")    
            else:
                kbd.send(Keycode.B)  #PLAY/PAUSE
            pb_btn_state = None
            pb_btn_dbl = False
            pb_btn_count = -1
            pb_btn_long = -1
            
        if pb_btn_long >= 0 and pb_btn_long < btn_long_press:
            pb_btn_long +=1
            if enable_dev == True:
                print(pb_btn_long)
            if pb_btn_long == btn_long_press:
                pb_btn_state = -1
                pb_btn_dbl = False
                pb_btn_count = -1                
                pb_btn_long = -1
                if enable_dev == True:
                    print("pb long press")
    
    
    ##################
    ## LIGHT STRIPS ##
    ##################
        
    if enable_rgb == True:

        i=0
        while i<len(pins):
            if dn_switch.value:
                pixels[i].brightness = bright_night[i]
            else:
                pixels[i].brightness = bright_day[i]
            pixels[i].fill((colour[0], colour[1], colour[2]))
            i=i+1
    
    #########
    ## END ##
    #########
        
    time.sleep(0.1)