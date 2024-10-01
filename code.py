import board
import time
import usb_hid
import neopixel
import digitalio
import rotaryio
from analogio import AnalogIn
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


######################
## SETUP RGB STRIPS ##
######################

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
## SETUP ROTARY ENCODERS ##
###########################

rot_timeout = 10
btn_timeout = 4

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

#########################
## SETUP ANALOG INPUTS ##
#########################

analog0in = AnalogIn(board.GP26)
analog1in = AnalogIn(board.GP27)


##########################
## SETUP VOLTAGE READER ##
##########################

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

    VD0 = getVoltage(analog0in) #AD
    VD1 = getVoltage(analog1in) #SHIFT

    #print(VD0)

    if VD1 > 1:
        #print("SHIFT: FALSE")
        if VD0 > 0 and VD0 < 0.1:
            print("BUTTON: MODE (SWITCH MODE)")
            #kbd.send(Keycode.CONTROL, Keycode.F3)  #SWITCH MODE
        elif VD0 < 0.7:
            print("BUTTON: SOURCE (VOICE)")
            #kbd.send(Keycode.M)  #VOICE
        elif VD0 < 1.1:
            print("BUTTON: ATT (HOME)")
            #kbd.send(Keycode.H) #HOME
        elif VD0 < 1.4:
            print("BUTTON: LIST (MUTE)")
            #kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
        elif VD0 < 1.65:
            print("BUTTON: SEEK+ (NEXT)")
            #kbd.send(Keycode.N)  #NEXT TRACK
        elif VD0 < 1.9:
            print("BUTTON: SEEK- (PREVIOUS)")
            #kbd.send(Keycode.V)  #PREVIOUS TRACK
        elif VD0 < 2.15:
            print("BUTTON: VOL+ (VOLUME UP)")
            #kbd.send(Keycode.F8) #VOLUME UP
        elif VD0 < 2.4:
            print("BUTTON: VOL- (VOLUME DOWN)")
            #kbd.send(Keycode.F7) #VOLUME DOWN
        elif VD0 < 2.6:
            print("BUTTON: SEL (PLAY/PAUSE)")
            #kbd.send(Keycode.B)  #PLAY/PAUSE
        elif VD0 < 2.8:
            print("BUTTON: OFF (SCREEN)")
            #kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
    elif VD1 < 1:
        if VD0 > 1:
            print("SHIFT: TRUE")
            if VD0 >= 1.4 and VD0 < 1.6:
                print("BUTTON: SHIFTUP (MEDIA)")
                #kbd.send(Keycode.J)  #LAUNCH MEDIA
            elif VD0 < 1.9:      
                print("BUTTON: SHIFTDOWN (NAVIGATION)")
                #kbd.send(Keycode.F) #LAUNCH NAVIGATION
    
    ##############
    ## ENCODERS ##
    ##############
    
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
                #kbd.send(Keycode.F8) #VOLUME UP
                print ("volume up")
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
                #kbd.send(Keycode.F7) #VOLUME DOWN
                print ("volume down")
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
        print("timeout vol rotary")
      
    if not vol_btn.value and vol_btn_state is None:
        vol_btn_state = "pressed"
    if vol_btn.value and vol_btn_state == "pressed":
        if vol_btn_dbl == False:
            vol_btn_dbl = True
            vol_btn_count = 0
        elif vol_btn_dbl == True:
            print("vol_double")
            #kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) #SCREEN POWER TOGGLE
            vol_btn_dbl = False
            vol_btn_count = -1
        vol_btn_state = None

    if vol_btn_count >= 0 and vol_btn_count < btn_timeout:
        vol_btn_count += 1
        print(vol_btn_count)
    elif vol_btn_count == btn_timeout:
        print ("vol_single")
        #kbd.send(Keycode.CONTROL, Keycode.F11) #TOGGLE MUTE
        vol_btn_state = None
        vol_btn_dbl = False
        vol_btn_count = -1
    
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
                #kbd.send(Keycode.N)  #NEXT TRACK
                print ("next")
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
                #kbd.send(Keycode.V)  #PREVIOUS TRACK
                print ("previous")
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
        print("timeout pb rotary")
      
    if not pb_btn.value and pb_btn_state is None:
        pb_btn_state = "pressed"
    if pb_btn.value and pb_btn_state == "pressed":
        if pb_btn_dbl == False:
            pb_btn_dbl = True
            pb_btn_count = 0
        elif pb_btn_dbl == True:
            print("pb_double")
            #kbd.send(Keycode.J)  #LAUNCH MEDIA
            pb_btn_dbl = False
            pb_btn_count = -1
        pb_btn_state = None

    if pb_btn_count >= 0 and pb_btn_count < btn_timeout:
        pb_btn_count += 1
        print(pb_btn_count)
    elif pb_btn_count == btn_timeout:
        print ("pb_single")
        #kbd.send(Keycode.B)  #PLAY/PAUSE
        pb_btn_state = None
        pb_btn_dbl = False
        pb_btn_count = -1
    
    
    ##################
    ## LIGHT STRIPS ##
    ##################
        
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