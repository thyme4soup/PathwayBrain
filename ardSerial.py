#!/usr/bin/python
import serial
import struct
import sys
import time
import math
import numpy as np


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

def tups_to_angles(angles):
  lst = [0] * 16
  for servo, angle in angles:
    lst[servo] = angle
  return lst

    
'''
Joint references:
  0: ?
  1: head pitch
  2: tail
  3: 
'''
if __name__ == '__main__':

  print("Starting ardSerial...")
  write_read('k',"sit")
  time.sleep(1)
  write_read('k', "zero")
  time.sleep(1)
  
  for i in range(4):
    joint = 0
    for a in np.arange(0, 2 * math.pi, 0.2):
      angle = math.sin(a) * 30
      write_read('m', "{} {}".format(joint, angle))
      time.sleep(0.04)

  print("ardSerial finished")
            
            