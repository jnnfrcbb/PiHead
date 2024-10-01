import board
import time
import digitalio
import rotaryio

enable_dev = True

rot_timeout = 10
btn_timeout = 4
btn_long_press = 10

#set up encoders
enc_3v = [board.GP12, board.GP8] #3V in
enc_sw = [board.GP13, board.GP9] #button pin
enc_clk = [board.GP15,board.GP11] #rotary pin 1
enc_dt = [board.GP14,board.GP10] #rotary pin 2

enc_rot_limit = [1,2] #number of clicks to trigger

#set up data structures
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

i = 0

while i < len(enc_3v):
    enc_pwr.append (digitalio.DigitalInOut(enc_3v[i]))
    enc_pwr[i].direction = digitalio.Direction.OUTPUT
    enc_pwr[i].value = True

    enc_rot.append (rotaryio.IncrementalEncoder(enc_clk[i], enc_dt[i]))
    enc_rot_limit.append(1)
    enc_rot_pos.append(0)
    enc_rot_last_pos.append(0)
    enc_rot_direction.append(0)
    enc_rot_count.append(0)
    enc_rot_timeout.append(-1)

    enc_btn.append (digitalio.DigitalInOut(enc_sw[i]))
    enc_btn[i].direction = digitalio.Direction.INPUT
    enc_btn_state.append(None)
    enc_btn_dbl.append(False)
    enc_btn_count.append(-1)
    enc_btn_long.append(-1)

    enc_out.append (-1)

    i+=1

while True:
    
    i = 0
    
    while i < len(enc_3v):
        
        enc_out[i] = -1

        enc_rot_pos[i] = enc_rot[i].position
        if enc_rot_pos[i] != enc_rot_last_pos[i]:
            if enc_rot_pos[i] > enc_rot_last_pos[i]:
                if enc_rot_direction[i] == -1:
                    enc_rot_count[i] = 1
                else:
                    enc_rot_count[i] += 1
                if enc_rot_count[i] == enc_rot_limit[i]:
                    enc_rot_count[i] = 0
                    enc_rot_direction[i] = 0
                    enc_rot_timeout[i] = -1
                    if enable_dev == True:
                        print("enc rot " + str(i) + " right")
                    else:
                        enc_out[i] = 2
                else:
                    enc_rot_timeout[i] = 0
                    enc_rot_direction[i] = 1
                enc_rot_last_pos[i] = enc_rot_pos[i]
            elif enc_rot_pos[i] < enc_rot_last_pos[i]:
                if enc_rot_direction[i] == 1:
                    enc_rot_count[i] = 1
                else:
                    enc_rot_count[i] +=1
                if enc_rot_count[i] == enc_rot_limit[i]:
                    enc_rot_count[i] = 0
                    enc_rot_direction[i] = 0
                    enc_rot_timeout[i] = -1
                    if enable_dev == True:
                        print("enc rot " + str(i) + " left")
                    else:
                        enc_out[i] = 1
                else:
                    enc_rot_timeout[i] = 0
                    enc_rot_direction[i] = -1
                enc_rot_last_pos[i] = enc_rot_pos[i]
        
        if enc_rot_timeout[i] >= 0 and enc_rot_timeout[i] < rot_timeout:
            enc_rot_timeout[i] +=1
        elif enc_rot_timeout[i] == rot_timeout:
            enc_rot[i].position = 0
            enc_rot_last_pos[i] = 0
            enc_rot_count[i] = 0
            enc_rot_timeout[i] = -1
            if enable_dev == True:
                print ("enc rot " + str(i) + " timeout")

        if not enc_btn[i].value and enc_btn_state[i] is None:
            enc_btn_state[i] = "pressed"
            enc_btn_long[i] = 0
        elif enc_btn[i].value and enc_btn_state == -1:
            enc_btn_state[i] = None
        if enc_btn[i].value and enc_btn_state[i] == "pressed":
            if enc_btn_dbl[i] == False:
                enc_btn_dbl[i] = True
                enc_btn_count[i] = 0
            elif enc_btn_dbl[i] == True:
                if enable_dev == True:
                    print ("enc btn " + str(i) + " double")
                else:
                    enc_out[i] = 3
                enc_btn_dbl[i] = False
                enc_btn_count[i] = -1
                enc_btn_long[i] = -1
            enc_btn_state[i] = None
    
        if enc_btn_count[i] >= 0 and enc_btn_count[i] < btn_timeout:
            enc_btn_count[i] += 1
            print (enc_btn_count[i])
        elif enc_btn_count[i] == btn_timeout:
            if enable_dev == True:
                print ("enc btn " + str(i) + " single")
            else:
                enc_out[i] = 2
            enc_btn_state[i] = None
            enc_btn_dbl[i] = False
            enc_btn_count[i] = -1
            enc_btn_long[i] = -1

        if enc_btn_long[i] >= 0 and enc_btn_long[i] < enc_btn_long[i]:
            enc_btn_long[i] += 1
            if enc_btn_long[i] == btn_long_press:
                enc_btn_state[i] = -1
                enc_btn_dbl[i] = False
                enc_btn_count[i] = -1
                enc_btn_long[i] = -1
                if enable_dev == True:
                    print ("enc btn " + str(i) + " long")
                else:
                    enc_out[i] = 4
                    
        time.sleep(0.5)
    
    print(enc_out[1])
