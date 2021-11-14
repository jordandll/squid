from tkinter import *
import socket as sock
from datetime import datetime
import struct

# Network related objects and tasks.
sock.setdefaulttimeout(2)
s = sock.socket()
my_struct = struct.Struct('!Bd')

# Default remote address.
host = '127.0.0.1'
port = 9002
addr = (host, port)

def connect(s):
    try:
        s.connect(addr)
    except ConnectionRefusedError:
        print(f'ERROR {str(datetime.today())[:-3]}:\tConnection with remote socket at \'{addr[0]}:{addr[1]:d}\' \
         refused.')

class App:
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        Label(frame, text='Red').grid(row=0, column=0)
        Label(frame, text='Green').grid(row=1, column=0)
        Label(frame, text='Blue').grid(row=2, column=0)
        scaleRed = Scale(frame, from_=0, to=100,
              orient=HORIZONTAL, command=self.updateRed)
        scaleRed.grid(row=0, column=1)
        scaleGreen = Scale(frame, from_=0, to=100,
              orient=HORIZONTAL, command=self.updateGreen)
        scaleGreen.grid(row=1, column=1)
        scaleBlue = Scale(frame, from_=0, to=100,
              orient=HORIZONTAL, command=self.updateBlue)
        scaleBlue.grid(row=2, column=1)


    def updateRed(self, duty):
        # rgb.set_red(float(duty))
        connect(s)
        # Pack the message into a bytes object with network formatting.
        bmsg = my_struct.pack(1, float(duty))
        # Send the message.
        sent = s.send(bmsg)
        s.close()

    def updateGreen(self, duty):
        # rgb.set_green(float(duty))
        connect(s)
        bmsg = my_struct.pack(2, float(duty))
        # Send the message.
        sent = s.send(bmsg)
        s.close()

    def updateBlue(self, duty):
        # rgb.set_blue(float(duty))
        connect(s)
        bmsg = my_struct.pack(3, float(duty))
        # Send the message.
        sent = s.send(bmsg)
        s.close()

root = Tk()
root.wm_title('RGB LED Control')
app = App(root)
root.geometry("200x150+0+0")
root.mainloop()