from guizero import App, PushButton
import roomba_pi

bot = roomba_pi.Robot()

app = App(title="Roomba Control", width=190, height=120, layout="grid")

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
    
#add widgets here
button_forward = PushButton(app, command=forward, text="forward", grid=[1,0])
button_left = PushButton(app, command=left, text="left", grid=[0,1])
button_stop = PushButton(app, command=stop, text="stop", grid=[1,1])
button_right = PushButton(app, command=right, text="right", grid=[2,1])
button_backward = PushButton(app, command=backward, text="backward", grid=[1,2])

app.display()