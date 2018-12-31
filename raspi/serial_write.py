#!/usr/bin/env python
import time
import serial
          
      
ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0
          
      
while 1:
    print("sending: ", counter)
    ser.write(str.encode('Write counter: %d \n'%(counter)))
    time.sleep(.1)
    counter += 1