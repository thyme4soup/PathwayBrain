
from PathwayHandling import PathwayHandler

class BigBrain:

  def __init__(self):
    self.pathway_handler = PathwayHandler()
    self.memory = {}


if __name__ == '__main__':

  from Sight import Sight
  
  print("Brain Testing")
  brain = BigBrain()
  sight_module = Sight(brain.pathway_handler, brain.memory)



