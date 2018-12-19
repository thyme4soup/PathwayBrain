
import PathwayHandling
from PathwayHandling import PathwayHandler

sight_node = 'raw_sight_updated'

wall_detected_node = "wall_detected"
face_detected_node = "face_detected"

class Sight:

  def __init__(self, pathways, memory):
    self.pathways = pathways
    self.memory = memory

    self.pathways.connectToNode(sight_node, self.handle_sight)
    
    # Every raw_sight_updated notification will reset the node
    def x(data):
      pass
    self.pathways.connectToNode(sight_node, x, refractory_period=0, reset_on=True)

  def handle_sight(self, data):
    # Act on raw data (only if notified by raw_sight_updated
    if data == 'raw_sight_updated':
      x = self.memory[data]
      face_detected = x == 1
      wall_detected = x == 2 
    else:
      face_detected = False
      wall_detected = False
    
    # Act on parsed data
    if face_detected:
      self.pathways.modifyValue(face_detected_node, PathwayHandling.ego_uptick)
      print("face detected")
    if wall_detected:
      self.pathways.modifyValue(wall_detected_node, PathwayHandling.id_uptick)
      print("wall detected")

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


