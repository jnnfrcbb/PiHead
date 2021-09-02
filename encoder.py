import math
import threading
import time
import RPi.GPIO as GPIO

PIN_A = 17
PIN_B = 27
PIN_SW = 22



class BasicEncoder:

    def __init__(self, a_pin, b_pin):
        self.a_pin = a_pin
        self.b_pin = b_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.a_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.a_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.last_delta = 0
        self.r_seq = self.rotation_sequence()

        self.steps_per_cycle = 4
        self.remainder = 0

    def rotation_sequence(self):

        a_state = GPIO.input(self.a_pin)
        b_state = GPIO.input(self.a_pin)
        r_seq = (a_state ^ b_state | b_state << 1)
        return r_seq

    def get_delta(self):
        delta = 0
        r_seq = self.rotation_sequence()
        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4
            if delta==3:
                delta = -1
            elif delta==2:
                delta = int(math.copysign(delta, self.last_delta))

            self.last_delta = delta
            self.r_seq = r_seq

        return delta

    def get_cycles(self):
        self.remainder += self.get_delta()
        cycles = self.remainder // self.steps_per_cycle
        self.remainder %= self.steps_per_cycle
        return cycles

    def get_switchstate(self):
        return 0

class SwitchEncoder(BasicEncoder):

    def __init__(self, a_pin, b_pin, sw_pin):
        BasicEncoder.__init__(self, a_pin, b_pin)

        self.sw_pin = sw_pin
        GPIO.setup(self.sw_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        
    def get_switchstate(self):
        return GPIO.input(self.sw_pin)

class EncoderWorker(threading.Thread):
    def __init__(self, encoder):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.stopping = False
        self.encoder = encoder
        self.daemon = True
        self.delta = 0
        self.delay = 0.001
        self.lastSwitchState = False
        self.upEvent = False
        self.downEvent = False

    def run(self):
        self.LastSwitchState = self.encoder.get_switchstate()
        while not self.stopping:
            delta = self.encoder.get_cycles()
            with self.lock:
                self.delta += delta 

                self.switchstate = self.encoder.get_switchstate()
                if (not self.lastSwitchState) and (self.switchstate):
                    self.upEvent = True
                if (self.lastSwitchState) and (not self.switchstate):
                    self.downEvent = True
                self.lastSwitchState = self.switchstate

    def get_delta(self):
        with self.lock:
            delta = self.delta
            self.delta = 0
        return delta

    def get_upEvent(self):
        with self.lock:
            delta = self.upEvent
            self.upEvent = False
        return delta

    def get_downEvent(self):
        with self.lock:
                delta = self.downEvent
                self.downEvent = False
        return delta

def switch_demo():
    value = 0

    encoder = EncoderWorker(SwitchEncoder(PIN_A, PIN_B, PIN_SW))
    encoder.start()

    while 1:
        delta = encoder.get_delta()
        if delta!=0:
            value = value + delta
            #print ("value", value)

        if encoder.get_upEvent():
            print ("up!")

        if encoder.get_downEvent():
            print ("down!")

if __name__ == "__main__":
    switch_demo()