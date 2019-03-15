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
    instrStr = instrStr.encode()
  elif token == 'l':  # use binary to reduce packet size
    ser.write(('l' + str(len(var))).encode())
    print(var)
    instrStr = struct.pack('b' * len(var), *[int(x) for x in var])
  elif token == 'w' or token == 'k' or token == 'm':
    instrStr = (token + var + "\n").encode()
  else:
    instrStr = token.encode()
  ser.write(instrStr)
    
def write_read(token, var=""):
  serialWriteByte(token, var)
  time.sleep(0.1)
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

def dist_from_resp(resp):
  words = resp.split(' ')
  if "Distance:" in words[0]:
    return int(words[1])
  else:
    return 0

    
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

  from VisualsTest import VisionTracker
  import random
  
  vt = VisionTracker(
    (-30, 30),
    (-30, 30),
    yaw_step = 5,
    pitch_step = 5,
    repaint_tolerance=0)

  ny, np = vt.get_next_target(0, 0)
  for i in range(150):
    resp = write_read('e', "")
    print(resp)
    dist = dist_from_resp(resp)
    vt.update_val(ny, np, dist)
    ny, np = vt.get_next_target(ny, np)
    write_read('m', "{} {}".format(0, ny))
    write_read('m', "{} {}".format(1, np))
    # vt.visualize()
    time.sleep(0.1)
  
  vt.visualize()
  import png
  png.from_array(vt.fov, 'L').save("fov.png")
      
  print("ardSerial finished")
            
            