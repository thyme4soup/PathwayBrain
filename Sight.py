
'''
Establish convention for data passage,
may need mutexes if can't narrow each pathway to one output
'''


import PathwayHandling
import random
from PathwayHandling import PathwayHandler

sight_node = 'raw_sight_updated'

wall_detected_node = "wall_detected"
face_detected_node = "face_detected"
clear_floor_node = "clear_detected"

class Sight:

  def __init__(self, pathways, memory, control):
    self.pathways = pathways
    self.memory = memory
    self.control = control
    self.pathways.connectToNode(sight_node, self.handle_sight)
    
    # Every raw_sight_updated notification will reset the node
    def x(data):
      pass
    self.pathways.connectToNode(sight_node, x, refractory_period=0, reset_on=True)

    self.pathways.connectToNode(sight_node, self.handle_sight, refractory_period=0.05)
    self.pathways.connectToNode(face_detected_node, self.face_handler, refractory_period=10)
    self.pathways.connectToNode(wall_detected_node, self.wall_handler, refractory_period=0.1)
    self.pathways.connectToNode(clear_floor_node, self.clear_handler, refractory_period=0.1)

  def handle_sight(self, data):
    # Act on raw data (only if notified by raw_sight_updated
    if data == 'raw_sight_updated':
      x = self.memory[data][0]
      face_detected = x == 'f'
      wall_detected = x == 'w' or face_detected
      dist = self.memory[data][1]
    else:
      face_detected = False
      wall_detected = False
      dist = -1

    if face_detected:
      self.pathways.modifyValue(face_detected_node, PathwayHandling.ego_uptick)

    if wall_detected:
      self.pathways.modifyValue(wall_detected_node, PathwayHandling.id_uptick)
    
    if dist > 0:
      self.pathways.modifyValue(clear_floor_node, PathwayHandling.id_uptick)

  def clear_handler(self, data):
    dec = random.choice([1,2,3,4,5,6])
    if dec == 1:
      pass
    elif dec == 2:
      self.control.queue_action('tr', priority=0.1)
    elif dec == 3:
      self.control.queue_action('tl', priority=0.1)
    else:
      self.control.queue_action('f', priority=0.1)

  def face_handler(self, data):
    print("hello!")
    self.pathways.resetValue(face_detected_node)

  def wall_handler(self, data):
    print("wall!")
    self.pathways.resetValue(wall_detected_node)
    dist = self.memory.get(sight_node, (0, 0))[1]

    # If the way is perceived as blocked, balk
    if dist == 0:
      self.control.queue_action('b', priority=0.4)

    # If approaching a wall, consider turning
    if dist <= 2:
      dec = random.choice([1,2,3,4])
      if dec == 1:
        self.control.queue_action('tr', priority=0.5)
      elif dec == 2:
        self.control.queue_action('tl', priority=0.5)

if __name__ == '__main__':

  print("Sight Testing")
  
  from BigBrain import BigBrain
  from time import sleep

  brain = BigBrain()
  sight = Sight(brain.pathway_handler, brain.memory)
  
  with open('SightTesting.txt', 'r') as f:
    for line in f:
      brain.memory[sight_node] = int(line)
      brain.pathway_handler.modifyValue('raw_sight_updated', 1.0)
      sleep(0.5)


