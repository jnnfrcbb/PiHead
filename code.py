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

slp_time = 0.025 #sleep time for loop

######################
## SETUP RGB STRIPS ##
######################

if enable_rgb == True:

    pins=[board.GP16,board.GP17,board.GP18,board.GP19]
    rgb_count=[9,10,10,10]
    bright_day=[0.5,0.5,0.5,0.5]
    bright_night=[0.25,0.1,0.1,0.1]

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

def call_key(key):

    ##SYSTEM
    if key == 0:                    #REBOOT
        if enable_dev == False:
            kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.R) 
        else:
            print("reboot")
    elif key == 1:                  #SCREEN POWER TOGGLE
        if enable_dev == False:
            kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.B) 
        else:
            print("toggle screen")
    elif key == 2:                  #HOME
        if enable_dev == False:
            kbd.send(Keycode.H)  
        else:
            print("home")
    elif key == 3:                  #SWITCH MODE
        if enable_dev == False:
            kbd.send(Keycode.CONTROL, Keycode.F3)   
        else:
            print("switch mode")
    elif key == 4:                  #LAUNCH MEDIA
        if enable_dev == False:
            kbd.send(Keycode.J)  
        else:
            print("show media")
    elif key == 5:                  #LAUNCH NAVIGATION
        if enable_dev == False:
            kbd.send(Keycode.F) 
        else:
            print("show navigation")
    elif key == 6:                  #PHONE
        if enable_dev == False:
            kbd.send(Keycode.P)  
        else:
            print("show phone")
    elif key == 7:                  #PHONE
        if enable_dev == False:
            kbd.send(Keycode.F2)  
        else:
            print("toggle night")
    elif key == 9:                  #VOICE
        if enable_dev == False:
            kbd.send(Keycode.M)  
        else:
            print("voice")

    ##PLAYBACK
    elif key == 10:                 #PLAY/PAUSE
        if enable_dev == False:
            kbd.send(Keycode.B)  
        else:
            print("play/pause")
    elif key == 11:                 #PREVIOUS TRACK
        if enable_dev == False:
            kbd.send(Keycode.V)  
        else:
            print("previous track")
    elif key == 12:                 #NEXT TRACK
        if enable_dev == False:
            kbd.send(Keycode.N)  
        else:
            print("next track")

    ##VOLUME
    elif key == 20:                 #TOGGLE MUTE
        if enable_dev == False:
            kbd.send(Keycode.CONTROL, Keycode.F11) 
        else:
            print("volume mute")
    elif key == 21:                 #VOLUME DOWN
        if enable_dev == False:
            kbd.send(Keycode.F7) 
        else:
            print("volume down")
    elif key == 22:                 #VOLUME UP
        if enable_dev == False:
            kbd.send(Keycode.F8) 
        else:
            print("volume up")


###########################
## SETUP ROTARY ENCODERS ##
###########################

if enable_enc == True:

    ## set parameters
    rot_timeout = 60
    btn_timeout = 20
    btn_long_press = 60

    ## set up encoders
    ## 0 = volume; 1 = playback
    enc_3v = [board.GP12, board.GP8] #3V in
    enc_sw = [board.GP13, board.GP9] #button pin
    enc_clk = [board.GP15,board.GP11] #rotary pin 1
    enc_dt = [board.GP14,board.GP10] #rotary pin 2

    enc_rot_limit = [1,2] #number of clicks to trigger
            
    ## set up encoder variable arrays
    enc_pwr = []

    enc_rot = []
    enc_rot_pos = []
    enc_rot_last_pos = []
    enc_rot_direction = []
    enc_rot_count = []
    enc_rot_timeout = []

    enc_btn = []
    enc_btn_state = []
    enc_btn_dbl = []
    enc_btn_count = []
    enc_btn_long = []

    enc_out = []

    e = 0

    while e < len(enc_3v):
        enc_pwr.append (digitalio.DigitalInOut(enc_3v[e]))
        enc_pwr[e].direction = digitalio.Direction.OUTPUT
        enc_pwr[e].value = True

        enc_rot.append(rotaryio.IncrementalEncoder(enc_clk[e], enc_dt[e]))
        enc_rot_pos.append(0)
        enc_rot_last_pos.append(0)
        enc_rot_direction.append(0)
        enc_rot_count.append(0)
        enc_rot_timeout.append(-1)

        enc_btn.append (digitalio.DigitalInOut(enc_sw[e]))
        enc_btn[e].direction = digitalio.Direction.INPUT
        enc_btn[e].pull = digitalio.Pull.UP
        enc_btn_state.append(None)
        enc_btn_dbl.append(False)
        enc_btn_count.append(-1)
        enc_btn_long.append(-1)

        enc_out.append(0)

        e+=1

    ## set up encoder outputs
    def enc_proc(enc_index, enc_value):
        proc = None
        if enc_index == 0:                                      #volume encoder
            if enc_value == 1:                                  #rot_left
                proc = "enc rot " + str(enc_index) + " left"    
                call_key(21)                                    #volume down
            elif enc_value == 2:                                #rot_right
                proc = "enc rot " + str(enc_index) + " right"   
                call_key(22)                                    #volume up
            elif enc_value == 3:                                #btn_single
                proc = "enc btn " + str(enc_index) + " single"  
                call_key(20)                                    #toggle mute
            elif enc_value == 4:                                #btn_double
                proc = "enc btn " + str(enc_index) + " double"  
                call_key(1)                                     #toggle screen
            elif enc_value == 5:                                #btn_long
                proc = "enc btn " + str(enc_index) + " long"
                call_key(0)                                     #reboot
        elif enc_index == 1:                                    #playback encoder
            if enc_value == 1:                                  #rot_left
                proc = "enc rot " + str(enc_index) + " left"
                call_key(11)                                    #previous track
            elif enc_value == 2:                                #rot_right
                proc = "enc rot " + str(enc_index) + " right"
                call_key(12)                                    #next track
            elif enc_value == 3:                                #btn_single
                proc = "enc btn " + str(enc_index) + " single"
                call_key(10)                                    #play/pause
            elif enc_value == 4:                                #btn_double
                proc = "enc btn " + str(enc_index) + " double"
                call_key(4)                                     #launch media
            elif enc_value == 5:                                #btn_long
                proc = "enc btn " + str(enc_index) + " long"
                call_key(9)                                     #voice
        return proc


#########################
## SETUP ANALOG INPUTS ##
#########################

if enable_whl == True:

    analog0in = AnalogIn(board.GP26)
    analog1in = AnalogIn(board.GP27)

    boardVCC = 3.3

    def getVoltage(pin):
        ret = float((pin.value * boardVCC) / 65536)
        print ("pin: " + pin + " | " + ret)
        return ret

    def whl_input():
        ret = False
        VD0 = getVoltage(analog0in)
        VD1 = getVoltage(analog1in)
        if VD0 <= 2.8 or VD1 < 1:
            return True
        return ret

    def whl_proc(VD0, VD1, exec):
        ret = 0 #0 = no input; 1 = press; 2 = hold
        whl_v[0] = VD0
        whl_v[1] = VD1
        if VD1 > 1:
            if VD0 < 0.03: #BUTTON: MODE (SWITCH MODE)
                if exec == True:
                    call_key(3)
                ret = 1
            elif VD0 > 0.5 and VD0 < 0.62: #BUTTON: SOURCE (VOICE)
                if exec == True:
                    call_key(9)
                ret = 1
            elif VD0 > 1 and VD0 < 1.05: #BUTTON: ATT (HOME)
                if exec == True:
                    call_key(2)
                ret = 1
            elif VD0 >1.3 and VD0 < 1.35: #BUTTON: LIST (MUTE)
                if exec == True:
                    call_key(20)
                ret = 1
            elif VD0 > 1.5 and VD0 < 1.6: #BUTTON: SEEK+ (NEXT)"
                if exec == True:
                    call_key(12)
                ret = 1
            elif VD0 > 1.8 and VD0 < 1.85: #BUTTON: SEEK- (PREVIOUS)
                if exec == True:
                    call_key(11)
                ret = 1
            elif VD0 > 2 and VD0 < 2.1: #BUTTON: VOL+ (VOLUME UP)
                if exec == True:
                    call_key(22)
                ret = 2
            elif VD0 > 2.3 and VD0 < 2.35: #BUTTON: VOL- (VOLUME DOWN)
                if exec == True:
                    call_key(21)
                ret = 2
            elif VD0 > 2.5 and VD0 < 2.55: #BUTTON: SEL (PLAY/PAUSE)
                if exec == True:
                    call_key(10)
                ret = 1
            elif VD0 > 2.7 and VD0 < 2.75: #BUTTON: OFF (SCREEN)
                if exec == True:
                    call_key(1)
                ret = 1
        elif VD1 < 1:
            if VD0 > 1:
                if VD0 >= 1.5 and VD0 < 1.6: #BUTTON: SHIFTUP (MEDIA)
                    if exec == True:
                        call_key(4)
                    ret = 1
                elif VD0 > 1.8 and VD0 < 1.85: #BUTTON: SHIFTDOWN (NAVIGATION)
                    if exec == True:
                        call_key(5)
                    ret = 1
        return ret

    #whl_state = None
    whl_state = 0

    whl_v = [-1, -1]

while True:

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

    ############################
    ## STEERING WHEEL CONTROL ##
    ############################
 
    if enable_whl == True:
        if whl_input() == True and whl_state == 0:
            whl_state = whl_proc(getVoltage(analog0in),getVoltage(analog1in), False)
        elif whl_input() == True and whl_state == 2:
            whl_state = whl_proc(getVoltage(analog0in),getVoltage(analog1in), True)
            time.sleep(0.075)
        elif whl_input() == False and not whl_state == 0:
            w = whl_proc(whl_v[0], whl_v[1], True)
            whl_v[0] = -1
            whl_v[1] = -1
            whl_state = 0

    ##############
    ## ENCODERS ##
    ##############
    
    if enable_enc == True:
    
        while e < len(enc_3v):
            
            enc_out[e] = 0

            enc_rot_pos[e] = enc_rot[e].position
            if enc_rot_pos[e] != enc_rot_last_pos[e]:
                if enc_rot_pos[e] > enc_rot_last_pos[e]:
                    if enc_rot_direction[e] == -1:
                        enc_rot_count[e] = 1
                    else:
                        enc_rot_count[e] += 1
                    if enc_rot_count[e] == enc_rot_limit[e]:
                        enc_rot_count[e] = 0
                        enc_rot_direction[e] = 0
                        enc_rot_timeout[e] = -1
                        enc_out[e] = 2 #right
                    else:
                        enc_rot_timeout[e] = 0
                        enc_rot_direction[e] = 1
                    enc_rot_last_pos[e] = enc_rot_pos[e]
                elif enc_rot_pos[e] < enc_rot_last_pos[e]:
                    if enc_rot_direction[e] == 1:
                        enc_rot_count[e] = 1
                    else:
                        enc_rot_count[e] +=1
                    if enc_rot_count[e] == enc_rot_limit[e]:
                        enc_rot_count[e] = 0
                        enc_rot_direction[e] = 0
                        enc_rot_timeout[e] = -1
                        enc_out[e] = 1 #left
                    else:
                        enc_rot_timeout[e] = 0
                        enc_rot_direction[e] = -1
                    enc_rot_last_pos[e] = enc_rot_pos[e]
            
            if enc_rot_timeout[e] >= 0 and enc_rot_timeout[e] < rot_timeout:
                enc_rot_timeout[e] +=1
            elif enc_rot_timeout[e] == rot_timeout:
                enc_rot[e].position = 0
                enc_rot_last_pos[e] = 0
                enc_rot_count[e] = 0
                enc_rot_timeout[e] = -1
                if enable_dev == True:
                    print ("enc rot " + str(e) + " timeout")

            if not enc_btn[e].value and enc_btn_state[e] is None:
                enc_btn_state[e] = "pressed"
                enc_btn_long[e] = 0
            elif enc_btn[e].value and enc_btn_state[e] == -1:
                enc_btn_state[e] = None
            if enc_btn[e].value and enc_btn_state[e] == "pressed":
                if enc_btn_dbl[e] == False:
                    enc_btn_dbl[e] = True
                    enc_btn_count[e] = 0
                elif enc_btn_dbl[e] == True:
                    enc_out[e] = 4 #double
                    enc_btn_dbl[e] = False
                    enc_btn_count[e] = -1
                    enc_btn_long[e] = -1
                enc_btn_state[e] = None
        
            if enc_btn_count[e] >= 0 and enc_btn_count[e] < btn_timeout:
                enc_btn_count[e] += 1
                #print (enc_btn_count[e])
            elif enc_btn_count[e] == btn_timeout:
                enc_out[e] = 3 #single
                enc_btn_state[e] = None
                enc_btn_dbl[e] = False
                enc_btn_count[e] = -1
                enc_btn_long[e] = -1

            if enc_btn_long[e] >= 0 and enc_btn_long[e] < btn_long_press:
                enc_btn_long[e] += 1
                if enc_btn_long[e] == btn_long_press:
                    enc_btn_state[e] = -1
                    enc_btn_dbl[e] = False
                    enc_btn_count[e] = -1
                    enc_btn_long[e] = -1
                    enc_out[e] = 5 #long
            
            if enc_out[e] > 0:
                if enable_dev == True:
                    print(enc_proc(e, enc_out[e]))
                else:
                    enc_proc(e, enc_out[e])

            e += 1
            
        e = 0

    
    #########
    ## END ##
    #########

    time.sleep(slp_time)