


if __name__ == '__main__':
  import sys
  from BigBrain import BigBrain
  from Sight import Sight
  from time import sleep
  
  arena_name = 'arena1.txt'
  
  with open(arena_name, 'r') as arena_txt:
    arena = [[c for c in line] for line in arena_txt]
  
  assert(arena)
  
  pchars = ['^', '>', 'v', '<']
  
  coords = (1, 1)
  orientation = 1
  
  def turn_right():
    orientation = (orientation + 1) % len(pchars)
  
  def turn_left():
    orientation = (orientation - 1) % len(pchars)
  
  def fwd():
    coords[orientation % 2] += (-1) ** ((orientation // 2) + 1)
  
  def print_arena():
    print('\n\n')
    for y, row in enumerate(arena):
      row_cpy = [c for c in row]
      if coords[1] == y:
        row_cpy[coords[0]] = pchars[orientation]
      line = ''.join(row_cpy)
      print(line)
  
  brain = BigBrain()
  sight = Sight(brain.pathway_handler, brain.memory)
  
  while(True):
    print_arena()
    sleep(0.5)
  