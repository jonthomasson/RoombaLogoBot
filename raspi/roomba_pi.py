#roomba_pi.py

import time
import serial
import RPi.GPIO as GPIO

class Robot:
    def __init__(self, dd = 12):
        self._uart = serial.Serial(
            port='/dev/serial0',
            baudrate = 19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2
        )
        
        self._dd = dd
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._dd, GPIO.OUT)
                
        #wake roomba up
        #GPIO.output(self._dd, GPIO.HIGH);
        self.wake_up()

        #pulse device detect three times to set baud 19200
        for i in range(3):
            GPIO.output(self._dd, GPIO.LOW);
            #self._dd.value(0)
            time.sleep(.25)
            GPIO.output(self._dd, GPIO.HIGH);
            #self._dd.value(1)
            time.sleep(.25)

        GPIO.output(self._dd, GPIO.LOW) #import to leave dd low here
        #send start command 128
        self.send_uart(128)
        time.sleep(.1)

        #send control command 130
        self.send_uart(130)
        time.sleep(.1)

        #set full control 132
        self.send_uart(132)
        time.sleep(.1)

        #change baud to match uart0 115200
        #self.send_uart(129)
        #self.send_uart(11)
        #time.sleep(.1)

        #send control command 130
        #self.send_uart(130)
        #time.sleep(.1)

        #set full control 132
        #self.send_uart(132)
        #time.sleep(.1)

        #reconnect to uart with higher baudrate
        #self._uart.init(115200, bits=8, parity=None, stop=1)
        
    def reset(self):
        self.send_uart(7)
        data = self._uart.read()
        print(data)
        
    def vacuum(self, onoff):
        self.send_uart(138)
        self.send_uart(onoff)

    def turn_off(self):
        self.wake_up()
        self.send_uart(133)

    def wake_up(self):
        GPIO.output(self._dd, GPIO.LOW);
        #self._dd.value(0)
        time.sleep(.1)
        GPIO.output(self._dd, GPIO.HIGH);
        #self._dd.value(1)
        time.sleep(2)

    def dock(self):
        #first set to spot mode
        self.send_uart(134)
        time.sleep(.1)

        #send dock command
        self.send_uart(143)
        time.sleep(.1)

       

    def send_uart(self, command):
        #uos.dupterm(self._uart, 1) #takeover uart from repl
        self._buf = command
        self._uart.write(bytearray([self._buf]))
        
        #uos.dupterm(None, 1) #give uart back to repl

    def recv_uart(self, num):
        #uos.dupterm(self._uart, 1) #takeover uart from repl
        #while not self._uart.any():   
        #    pass
        data = self._uart.read(num)
        #uos.dupterm(None, 1) #give uart back to repl
        return data

    def get_sensors(self):
        #uos.dupterm(self._uart, 1) #takeover uart from repl
        self.send_uart(142)
        self.send_uart(1)
        #print(self._uart.read())
        data = self.recv_uart(10)
        print(data)
        #uos.dupterm(None, 1) #give uart back to repl
        #for x in data:
         #   print(x)

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

    def sound(self, note, duration):
        #note is the midi note id.
        #duration is in seconds
        self.send_uart(140) #create song
        self.send_uart(1) #song number
        self.send_uart(1) #song length
        self.send_uart(note) #note to play
        self.send_uart(round(duration * 64))
        time.sleep(.1)
        self.send_uart(141)
        self.send_uart(1) #play song 1
        time.sleep(duration) #need to wait to give roomba time to play note
        
