
'''
TODO:

'''

import threading

class BaseControl:

  def __init__(self, action_callbacks):
    self.action_callbacks = action_callbacks
    self.queued_actions = []
    self.action_id_counter = 0
    self.action_id_graveyard = ([], threading.Lock())
    self.structure_lock = threading.Lock()

  def get_action_id(self):
    if len(self.action_id_graveyard[0]):
      self.action_id_graveyard[1].acquire()
      action_id = self.action_id_graveyard[0].pop(0)
      self.action_id_graveyard[1].release()
    else:
      action_id = self.action_id_counter
      self.action_id_counter += 1
    return action_id

  # queue_action takes in an action and a callback method. returns an id for book-keeping
  def queue_action(self, action, callback=None, priority=0.5, forget_timeout=0.5):
    assert(priority <= 1.0 and priority >= 0.0)

    action_id = self.get_action_id()

    index = 0
    while index < len(self.queued_actions) and self.queued_actions[index][0] >= priority:
      index += 1

    # maintains sorted list, highest to lowest
    self.structure_lock.acquire()
    self.queued_actions.insert(index, (priority, action, action_id, callback))
    self.structure_lock.release()

    # add and start removal mechanism
    def remove_expired_action():
      self.structure_lock.acquire()
      self.queued_actions = list(filter(lambda a: a[2] != action_id, self.queued_actions))
      self.structure_lock.release()

      self.action_id_graveyard[1].acquire()
      self.action_id_graveyard[0].append(action_id)
      self.action_id_graveyard[1].release()

    threading.Timer(forget_timeout, remove_expired_action).start()

    # identifier allows for chaining actions (callback method will have id passed in)
    return action_id

  def pop_next_action(self):
    # select largest item from collection, form is (priority, action, id, callback)
    self.structure_lock.acquire()

    if len(self.queued_actions) > 0:
      action = self.queued_actions.pop(0)
      self.structure_lock.release()
      return action

    else:
      self.structure_lock.release()
      return None

  def iter(self):
    action = self.pop_next_action()

    if action:
      def undefined():
        print("undefined action {}".format(action[1]))

      # call action from dictionary
      self.action_callbacks.get(action[1], undefined)()

      # perform callback for followup actions, passing in identifier
      if action[3]:
        action[3](action[2])


if __name__ == '__main__':
  import sys
  import Sight
  from BigBrain import BigBrain
  from time import sleep
  
  arena_name = 'arena1.txt'
  
  with open(arena_name, 'r') as arena_txt:
    arena = [[c for c in line] for line in arena_txt]
  
  assert(arena)

  def get_next(c, o):
    if o == 0:
      return (c[0], c[1] - 1)
    if o == 1:
      return (c[0] + 1, c[1])
    if o == 2:
      return (c[0], c[1] + 1)
    if o == 3:
      return (c[0] - 1, c[1])
  
  pchars = ['^', '>', 'v', '<']
  
  coords = (1, 1)
  orientation = 1
  
  def turn_right():
    global orientation
    orientation = (orientation + 1) % len(pchars)
    return 0
  
  def turn_left():
    global orientation
    orientation = (orientation - 1) % len(pchars)
    return 0

  def fwd():
    global coords
    old = coords
    coords = get_next(coords, orientation)

    if arena[coords[1]][coords[0]] != '.':
      print("collision! {}".format(coords))
      coords = old
      return -1
    return 0

  def balk():
    pass

  action_callbacks = {
    'tr' : turn_right,
    'tl' : turn_left,
    'b' : balk,
    'f' : fwd
  }

  def get_sight():
    cur = coords
    dist = 0
    while arena[cur[1]][cur[0]] == '.':
      cur = get_next(cur, orientation)
      dist += 1
    return (arena[cur[1]][cur[0]], dist - 1)
  
  def print_arena():
    print('\n\n')
    for y, row in enumerate(arena):
      row_cpy = [c for c in row]
      if coords[1] == y:
        row_cpy[coords[0]] = pchars[orientation]
      line = ' '.join(row_cpy)
      print(line)
    print(coords, orientation)
  
  control = BaseControl(action_callbacks)
  brain = BigBrain()
  sight = Sight.Sight(brain.pathway_handler, brain.memory, control)
  
  while(True):
    brain.memory[Sight.sight_node] = get_sight()
    brain.pathway_handler.modifyValue(Sight.sight_node, 1.0)
    print(control.queued_actions)
    control.iter()
    print_arena()
    print(get_sight())
    sleep(1)


