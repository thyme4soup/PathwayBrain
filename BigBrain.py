
from PathwayHandling import PathwayHandler

from Sight import Sight

class BigBrain:

  def __init__(self):
    self.pathway_handler = PathwayHandler()
    self.memory = {}


if __name__ == '__main__':

  print("Brain Testing")
  brain = BigBrain()

  sight = Sight(brain.pathway_handler, brain.memory)



