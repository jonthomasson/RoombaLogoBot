#roomba.py

import time
import machine
from machine import UART

class Robot:
    def __init__(self, bus = 1, baud = 57600, dd = 5):
        self._uart = UART(bus, 57600)
        self._uart.init(57600, bits=8, parity=None, stop=1)
        self._dd = machine.Pin(dd, machine.Pin.OUT)
        
        #wake roomba up
        self.wake_up()

        #send start command 128
        self._buf = 128
        self._uart.write(bytearray([self._buf]))
        time.sleep(.1)

        #send control command 130
        self._buf = 130
        self._uart.write(bytearray([self._buf]))
        time.sleep(.1)

        #set full control 132
        self._buf = 132
        self._uart.write(bytearray([self._buf]))
        time.sleep(.1)

    def vacuum(self, onoff):
        self._buf = 138
        self._uart.write(bytearray([self._buf]))
        self._buf = onoff
        self._uart.write(bytearray([self._buf]))

    def turn_off(self):
        self.wake_up()
        self._buf = 133
        self._uart.write(bytearray([self._buf]))

    def wake_up(self):
        self._dd.value(0)
        time.sleep(.1)
        self._dd.value(1)
        time.sleep(2)
        