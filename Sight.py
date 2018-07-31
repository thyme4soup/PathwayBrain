
from PathwayHandling import PathwayHandler

wall_detected_node = "wall_detected"
face_detected_node = "face_detected"

class Sight:

  def __init__(self, pathways, memory):
    self.pathways = pathways
    self.memory = memory

    self.pathways.connectToNode("raw_sight_updated", self.handle_sight)

  def handle_sight(self, data):
    print("handling sight")
    face_detected = True
    wall_detected = False
    if face_detected:
      self.pathways.modify_value(face_detected_node, pathways.ego_uptick)
    if wall_detected:
      self.pathways.modify_value(wall_detected_node, pathways.id_uptick)

if __name__ == '__main__':

  print("Sight Testing")