from tkinter import *
import socket as sock
from datetime import datetime
import struct

cmd_name = ['set_red', 'set_green', 'set_blue']

# Network related objects and tasks.
sock.setdefaulttimeout(2)

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

def send_cmd(cmd, duty):
    s = sock.socket()
    connect(s)
    # Pack the message into a bytes object with network formatting.
    bmsg = my_struct.pack(cmd+1, float(duty))
    # Send the message.
    sent = s.send(bmsg)
    print(f'Client \'{s.getsockname()}\' sent {sent:d} bytes of data to server \'{addr[0]}:{addr[1]:d}\'.')
    print(f'Command sent:\t{cmd_name[cmd]}({float(duty):.03f}).')
    s.close()

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
        send_cmd(0, duty)

    def updateGreen(self, duty):
        # rgb.set_green(float(duty))
        send_cmd(1, duty)

    def updateBlue(self, duty):
        # rgb.set_blue(float(duty))
        send_cmd(2, duty)

root = Tk()
root.wm_title('RGB LED Control')
app = App(root)
root.geometry("200x150+0+0")
root.mainloop()