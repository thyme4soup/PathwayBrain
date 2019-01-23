import time
import random
import threading
from EmitHandling import Handler

degrade_delta = 0.03

id_uptick = 2.0
id_threshold = 1.0

ego_uptick = 0.5
ego_threshold = 3.0

superego_uptick = 0.2
superego_threshold = 4.0

'''
The pathway handler is a vague implementation of neuron pathways.
This allows for general inputs (sight, touch, thought, etc) to be whittled down
into specific outputs. It allows pathways to hook into each other at different times,
i.e., if you had a pathway that classified objects you could pull that raw classification as
an input to your own pathway, such as a reflex to spiders or something.
The handler differs from neural pathways in a couple ways. Firstly, we can design functions
to handle things that might take many, many neurons. We can utilize machine learning mimic
heuristics, or wifi to access higher knowledge, all in one 'node'. Secondly, we can implement
negative feedback using pathway terminals rather than constructing a backwards loop.
For example, if I could mimic reflexive scratching with an 'itch_detection' node listening
to the termination of the 'scratch' node (the scratch being performed).
The idea is to streamline the coding of an explicit general AI. It may take a lot of code but with good
design should quickly become natural.
'''


class PathwayHandler:

  def __init__(self):
    self.pathway_nodes = Handler()
    self.node_values = {}
    self.in_refractory_period = {}

  # Connect a pathway to a node with given threshold and refractory period
  # Pathway should take in a single string, specifying the node that notified the pathway
  def connectToNode(self, node, pathway, threshold=1.0, refractory_period=1.0, reset_on=None):
    self.node_values[node] = self.node_values.get(node, 0)
    self.in_refractory_period[pathway] = False

    def refractory_reset():
      self.in_refractory_period[pathway] = False
      
    def resetter(_data):
      self.resetValue(node)

    def notify(value):
      if threshold <= value and not self.in_refractory_period[pathway]:
        pathway(node)
        self.in_refractory_period[pathway] = True
        threading.Timer(refractory_period, refractory_reset).start()

    if reset_on != None:
      self.pathway_nodes.listen(reset_on, resetter)
    self.pathway_nodes.listen(node, notify)

  # Modify activity value at node
  def modifyValue(self, node, delta):
    self.node_values[node] = max(self.node_values.get(node, 0) + delta, 0)
    self.pathway_nodes.emit(node, data=self.node_values[node])

  # Reset activity value at a node
  def resetValue(self, node):
    self.setValue(node, 0)

  # Set activity value at a node
  def setValue(self, node, value):
    self.node_values[node] = value
    self.pathway_nodes.emit(node, data=self.node_values[node])

  # Signal termination of a pathway
  def emitPathwayTerminal(self, terminal):
    self.pathway_nodes.emit(terminal)

  # Degrade node towards inactivity
  def degrade(self, node):
    self.modifyValue(node, -1 * degrade_delta)

  # General degrade
  def degrade(self):
    for node, value in self.node_values.items():
      self.degrade(node)

  def degrade(self, node=None):
    if node:
      self.modifyValue(node, -1 * degrade_delta)
    else:
      for node, value in self.node_values.items():
        self.degrade(node=node)

if __name__ == '__main__':

  print("Pathway Testing")

  x = PathwayHandler()
  see_person_node = "saw_person"
  get_greeted_node = "greeted"
  greet_node = "greet"

  greet_terminal = "person_greeted"

  def see_person():
    print(see_person_node)
    x.modifyValue(greet_node, ego_uptick)
  def get_greeted():
    print(get_greeted_node)
    x.modifyValue(greet_node, id_uptick)
  def greet():
    print("hiya!")
    x.emitPathwayTerminal(greet_terminal)


  x.connectToNode(
    see_person_node,
    see_person,
    threshold=id_threshold,
    refractory_period=1.0,
    reset_on=greet_terminal
  )
  x.connectToNode(
    get_greeted_node,
    get_greeted,
    threshold=ego_threshold,
    refractory_period=1.0,
    reset_on=greet_terminal
  )
  x.connectToNode(greet_node,
    greet,
    threshold=ego_threshold,
    refractory_period=1.0,
    reset_on=greet_terminal
  )

  for i in range(10 ** 3):
    if random.randint(1,10) == 1:
      x.modifyValue(see_person_node, id_uptick)
    if random.randint(1,5) == 1:
      x.modifyValue(get_greeted_node, id_uptick)
    time.sleep(0.1)