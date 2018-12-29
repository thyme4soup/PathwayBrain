
import time
from PathwayHandling import PathwayHandler
from Sight import Sight

RAW_SIGHT_NODE = "raw_sight_updated"
RAW_DIST_NODE = "raw_distance_updated"
RAW_AUDIO_NODE = "raw_audio_updated"

class BigBrain:

  def __init__(self):
    self.pathway_handler = PathwayHandler()
    self.memory = {}
    self.serial = open("serial_feed.txt", "r")

  def loop(self):
    serial_message = self.serial.readline().strip()
    if(serial_message):
      serial_message = self.serial.readline().strip()

      self.memory["raw_sight"] = int(serial_message)
      self.pathway_handler.setValue(RAW_SIGHT_NODE, 1)

      print(">{}".format(serial_message))
    else:
      self.serial.seek(0)

    self.pathway_handler.degrade()

  def __deinit__(self):
    self.serial.close()

if __name__ == '__main__':

  from Sight import Sight
  
  print("Brain Testing")
  brain = BigBrain()
  sight_module = Sight(brain.pathway_handler, brain.memory)

  while True:
    brain.loop()
    time.sleep(0.1)



