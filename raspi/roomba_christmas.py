#roomba_christmas.py

import time
import board
import neopixel
import roomba_pi
from espeakng import ESpeakNG

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D10

# The number of NeoPixels
num_pixels = 33

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
color = (255, 0, 0)


#sing we wish you a merry christmas and perform a dance
esng = ESpeakNG() #initialize singing voice
bot = roomba_pi.Robot() #initialize roomba
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)

def mix_it_up():
    global color
    for i in range(0, num_pixels, 11):
        for j in range(i, i+11):
            pixels[j] = color
        if(color == (255, 0, 0)):
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

def sound(note, duration):
    #note is the midi note id.
    #duration is in seconds
    bot.send_uart(140) #create song
    bot.send_uart(1) #song number
    bot.send_uart(1) #song length
    bot.send_uart(note) #note to play
    bot.send_uart(round(duration * 64))
    time.sleep(.1)
    bot.send_uart(141)
    bot.send_uart(1) #play song 1

def forward():
    bot.drive(102, 32768)
    
def left():
    bot.drive(102, 1)

def stop():
    bot.stop()
    
def right():
    bot.drive(102, -1)
    
def backward():
    bot.drive(-102, 32768)
    
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
    
#sing "we wish you" while driving forward and turn leds red
forward()

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 50
esng.speed = 130

#bot.drive(102, 32768)
esng.say("we")
sound(72, 1) #C

time.sleep(1)
#bot.stop()

pixels.fill((0, 255, 0)) 
pixels.show()
esng.pitch = 70
esng.say("wish")
sound(77, 1) #F

time.sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 70
esng.speed = 150
esng.say("you")
sound(77, .5) #F

time.sleep(.5)

stop()
backward()

mix_it_up()
       
pixels.show()
esng.pitch = 80
esng.speed = 170
esng.say("a")
sound(79, .5) #G

time.sleep(.5)

mix_it_up()
       
pixels.show()
esng.pitch = 70
esng.speed = 170
esng.say("Mair")
sound(77, .5) #F

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 60
esng.speed = 170
esng.say("ee")
sound(76, .5) #F

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("chris")
sound(74, 1) #D

time.sleep(1)


mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("mus")
sound(74, 1) #D

stop()
right()

time.sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 60
esng.speed = 130

#bot.drive(102, 32768)
esng.say("we")
sound(74, 1) #D

time.sleep(1)
#bot.stop()

pixels.fill((0, 255, 0)) 
pixels.show()
esng.pitch = 80
esng.say("wish")
sound(79, 1) #G

time.sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 80
esng.speed = 150
esng.say("you")
sound(79, .5) #G

time.sleep(.5)

stop()
left()

color = (255, 0, 0)


mix_it_up()
       
pixels.show()
esng.pitch = 90
esng.speed = 170
esng.say("a")
sound(81, .5) #A

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 70
esng.speed = 170
esng.say("Mair")
sound(79, .5) #G

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 60
esng.speed = 170
esng.say("ee")
sound(77, .5) #F

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("chris")
sound(76, 1) #E

time.sleep(1)


mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("mus")
sound(76, 1) #E


time.sleep(1)

stop()
bot.drive(102, 200) #forward circle

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 65
esng.speed = 130

#bot.drive(102, 32768)
esng.say("we")
sound(76, 1) #E

time.sleep(1)
#bot.stop()

pixels.fill((0, 255, 0)) 
pixels.show()
esng.pitch = 90
esng.say("wish")
sound(81, 1) #A

time.sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 90
esng.speed = 150
esng.say("you")
sound(81, .5) #A

time.sleep(.5)
color = (255, 0, 0)


mix_it_up()
       
pixels.show()
esng.pitch = 99
esng.speed = 170
esng.say("a")
sound(83, .5) #B

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 90
esng.speed = 170
esng.say("Mair")
sound(81, .5) #G

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 80
esng.speed = 170
esng.say("ee")
sound(79, .5) #G

time.sleep(.5)


mix_it_up()
       
pixels.show()
esng.pitch = 70
esng.speed = 150
esng.say("chris")
sound(77, 1) #E

time.sleep(1)


mix_it_up()
       
pixels.show()
esng.pitch = 60
esng.speed = 150
esng.say("mus")
sound(74, 1) #D

time.sleep(1)

stop()
bot.drive(-102, 200) #backward circle

mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("and")
sound(72, .5) #C

time.sleep(.5)

mix_it_up()
       
pixels.show()
esng.pitch = 50
esng.speed = 150
esng.say("a")
sound(72, .5) #C

time.sleep(.5)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 60
esng.speed = 150
esng.say("hap")
sound(74, 1) #D

time.sleep(1)

pixels.fill((0, 255, 0)) 
pixels.show()
esng.pitch = 70
esng.speed = 150
esng.say("pee")
sound(79, 1) #G

time.sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
esng.pitch = 65
esng.speed = 150
esng.say("new")
sound(76, 1) #E

time.sleep(1)

pixels.fill((0, 255, 0)) 
pixels.show()
esng.pitch = 70
esng.speed = 150
esng.say("YEAR")
sound(77, 2) #F

time.sleep(2)

stop()
right()

#some kind of led razzle dazzle here
for i in range(5):
    rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step

time.sleep(5)


esng.pitch = 50
esng.say("Merry Christmas Tallia")

pixels.fill((0, 0, 0))
pixels.show()
stop()




