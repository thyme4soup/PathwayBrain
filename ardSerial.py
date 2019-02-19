#!/usr/bin/python
import logging
logging.basicConfig(filename='ardSerial.log',level=logging.DEBUG)

try:
    import serial
    import struct
    import sys
    import time
    import math
    import numpy as np
except Exception as e:
    logging.debug('Error importing during library imports:\n{}'.format(str(e)))


ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


def serialWriteByte(token, var=""):

    if token == 'c' or token == 't':  # data
        instrStr = token + str(var[0]) + ',' + str(var[1]) + '\n'
    elif token == 'l':  # use binary to reduce packet size
        ser.write(('l' + str(len(var))).encode())
        print(var)
        instrStr = struct.pack('b' * len(var), *[int(x) for x in var])
    elif token == 'w' or token == 'k' or token == 'm':
        instrStr = (token + var + "\n").encode()
    else:
        instrStr = token
    ser.write(instrStr)
    
def write_read(token, var=""):
    serialWriteByte(token, var)
    s = ""
    while ser.in_waiting:
        x = ser.readline()
        if x != "":
            s += "\n"
    return s


if __name__ == '__main__':
    serialWriteByte('k', "zero")
    time.sleep(1)
    serialWriteByte('k',"sit")
    time.sleep(1)
    
    for i in range(3):
        joint = 0
        for a in np.arange(0, 2 * math.pi, 0.2):
            logging.debug(write_read('m', "{} {}".format(joint, math.cos(a) * 30)))
            time.sleep(0.04)
            
    logging.debug("Successfully terminated")
            
            