#roomba.py

import time
import machine
from machine import UART

class Robot:
    def __init__(self, bus = 1, baud = 57600, dd = 5):
        self._uart = UART(bus, 19200)
        self._uart.init(19200, bits=8, parity=None, stop=1)
        self._dd = machine.Pin(dd, machine.Pin.OUT)
        
        #wake roomba up
        self.wake_up()

        #pulse device detect three times to set baud 19200
        for i in range(3):
            self._dd.value(0)
            time.sleep(.25)
            self._dd.value(1)
            time.sleep(.25)

        #send start command 128
        self.send_uart(128)
        time.sleep(.1)

        #send control command 130
        self.send_uart(130)
        time.sleep(.1)

        #set full control 132
        self.send_uart(132)
        time.sleep(.1)

    def vacuum(self, onoff):
        self.send_uart(138)
        self.send_uart(onoff)

    def turn_off(self):
        self.wake_up()
        self.send_uart(133)

    def wake_up(self):
        self._dd.value(0)
        time.sleep(.1)
        self._dd.value(1)
        time.sleep(2)

    def send_uart(self, command):
        self._buf = command
        self._uart.write(bytearray([self._buf]))

    def drive(self, velocity, radius):
        #first send drive command
        self.send_uart(137)
        time.sleep(.1)
        #next send velocity
        high = (velocity >> 8) & 0xff
        low = velocity & 0xff
        self.send_uart(high) #high byte first
        self.send_uart(low) #low byte

        #finally send radius
        high = (radius >> 8) & 0xff
        low = radius & 0xff
        self.send_uart(high) #high byte first
        self.send_uart(low) #low byte
    
    def stop(self):
        self.drive(0, 0)

    def forward(self, distance):
        #we want distance to be in inches more or less
        #at 102mm/s we go 1 inch in appx .25 seconds
        time_to_wait = distance / 4 #4 inches per second
        self.drive(102, 32768)
        time.sleep(time_to_wait)
        self.stop()

    def right(self, degree):
        #at 102mm/s we go appx 45 degrees per second
        time_to_wait = degree / 45
        self.drive(102, -1)
        time.sleep(time_to_wait)
        self.stop()

    def left(self, degree):
        #at 102mm/s we go appx 45 degrees per second
        time_to_wait = degree / 45
        self.drive(102, 1)
        time.sleep(time_to_wait)
        self.stop()

    def backward(self, distance):
        #we want distance to be in inches more or less
        #at 102mm/s we go 1 inch in appx .25 seconds
        time_to_wait = distance / 4 #4 inches per second
        self.drive(-102, 32768)
        time.sleep(time_to_wait)
        self.stop()

        