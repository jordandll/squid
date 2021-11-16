#!/usr/bin/python3
import socket as sock
from datetime import datetime
import squid
import struct

my_struct = struct.Struct('!Bd')

# Squid object.
rgb = squid.Squid(18, 23, 24)

"""In the following list of Squid object method names, the index of each method name is equal to the control code value
minus one* that must be invoked in the frontend script, 'front.py', in order for the corresponding method/command to be
executed by the backend script, 'backend.py'."""
# TODO:  *Look into simply invoking the indices 'as-is', which would mean a possible control code of zero being ...
# ... sent over a network connection.

cmd_name = ['set_red', 'set_green', 'set_blue']

# TODO:  Write code to parse the command line arguments for '--host' or '-h' and ...
# ... '--port' or '-p' options.  Assuming they are found, set the 'HOST' and 'PORT' ...
# ... variables accordingly.

# Default Address Info.
HOST = '127.0.0.1'
PORT = 9002
ADDR = (HOST, PORT)

# Create server socket bound to HOST and listening on port PORT.
ss = sock.socket()
ss.bind(ADDR)
ss.listen(5)

# Begin main server loop.
try:
    while True:
    # Accept new connections.
        s, addr = ss.accept()
        s.settimeout(2)
    # Receive message.
        try:
            msg = s.recv(9)
        except sock.timeout:
            print(f'ERROR {str(datetime.today())[:-3]}:\tConnection timeout error occurred with client \'{addr[0]}:{addr[1]:d}\'.') 
            s.close()
            continue
    # Reflect message back to client.
    #    sent = s.send(msg)
    # Print command name and arguments from client.
    # Note that the first element, 'cmd[0]', contains the control code of the command in the form of a one byte
    # unsigned integer, while the second contains the argument, the duty cycle, in the form of an 8 byte floating
    # point number.
        cmd = my_struct.unpack(msg)
        code, duty = cmd; idx = code - 1
        print(f'{str(datetime.today())[:-3]}:\tClient \'{addr[0]}:{addr[1]:d}\' sent the command \'{cmd_name[idx]}({duty:.03f})\'.')
        # Check duty cycle
        if 0.0 <= duty <= 100.0:
            vars(squid.Squid)[cmd_name[idx]](rgb, duty)
        else:
            print('ERROR:\tDuty cycle must be a non-negative number that is less than or equal to one hundred (percent).')
    # Cleanup
        s.close()
except KeyboardInterrupt:
    print('Server stopped by keyboard interrupt.')
    s.close(); ss.close()
    exit(0)
except Exception as e:
    print(e)
    s.close(); ss.close()
    exit(1)
