
import math
import random
import time

class VisionTracker:

  def __init__(self,
               yaw_limits,
               pitch_limits,
               yaw_step = 1,
               pitch_step = 1,
               repaint_tolerance = 3):

    # Required inputs
    self.yaw_min, self.yaw_max = yaw_limits
    self.pitch_min, self.pitch_max = pitch_limits

    # Optionals
    self.yaw_step = yaw_step
    self.pitch_step = pitch_step
    self.repaint_tolerance = repaint_tolerance

    #Globals setup
    rows = ((self.pitch_max - self.pitch_min) // self.pitch_step)
    cols = ((self.yaw_max - self.yaw_min) // self.yaw_step)
    self.fov = [[None for j in range(cols)] for i in range(rows)]
    self.cov = (rows/2, cols/2)
    self.dirtied = ([], [])

    self.dirty_all()

  # For debugging
  def visualize(self):
    for row in self.fov:
      print(' '.join(['x' if x == None else str(x) for x in row]))
    print()

    
  # Dirty a coord (r, c). Internally handles out of bounds
  def dirty(self, r, c):
    if r < 0 or r >= len(self.fov) or c < 0 or c >= len(self.fov[r]):
      return 1
    else:
      y, p = self.index_to_coords(r, c)
      self.dirtied[self.is_prio(y, p)].append((r, c))
      return 0

  def dirty_all(self):
    for row in range(len(self.fov)):
      for col in range(len(self.fov[row])):
        self.dirty(row, col)

  def index_to_coords(self, r, c):
    return (
      c * self.yaw_step + self.yaw_min,
      r * self.pitch_step + self.pitch_min
    )
  def coords_to_index(self, y, p):
    return (
      int((p - self.pitch_min) // self.pitch_step),
      int((y - self.yaw_min) // self.yaw_step),
    )

    
  def get_next_target(self, cur_yaw, cur_pitch):
    def dist(c1, c2):
      return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
    def get_closest(c1, lst):
      closest = []
      for c2 in lst:
        if not closest or dist(c1, c2) < dist(c1, closest[0]):
          closest = [c2]
        elif dist(c1, c2) == dist(c1, closest[0]):
          closest.append(c2)
      
      return closest
      
    # prio
    if len(self.dirtied[1]) > 0:
      closest = get_closest(self.coords_to_index(cur_yaw, cur_pitch), self.dirtied[1])
      r, c = random.choice(closest)
      self.dirtied[1].remove((r,c ))
      return self.index_to_coords(r, c)
    # non-prio
    if len(self.dirtied[0]) > 0:
      closest = get_closest(self.coords_to_index(cur_yaw, cur_pitch), self.dirtied[0])
      r, c = random.choice(closest)
      self.dirtied[0].remove((r, c))
      return self.index_to_coords(r, c)
    else:
      r, c = self.cov
      return self.index_to_coords(r, c)

  def update_val(self, cur_yaw, cur_pitch, distance):
    print(cur_pitch, cur_yaw)
    r, c = self.coords_to_index(cur_yaw, cur_pitch)
    print(r, c)
    old = self.fov[r][c]
    if old and abs(distance - old) > self.repaint_tolerance:
      for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        self.dirty(nr, nc)
    self.fov[r][c] = distance

  def is_prio(self, yaw, pitch):
    real_cov = self.index_to_coords(self.cov[0], self.cov[1])
    # Priority coords are either in an ellipse around the cov or the ground in front of us (pitch below a certain line)
    f_y = (yaw - real_cov[0]) ** 2 / (0.5 * (self.yaw_max - self.yaw_min)) ** 2
    f_p = (pitch - real_cov[1]) ** 2 / (0.15 * (self.pitch_max - self.pitch_min)) ** 2
    f_yp = f_y + f_p
    return f_yp <= 1 or pitch <= (self.yaw_max - self.yaw_min) / 8 + self.yaw_min

if __name__ == '__main__':
  vt = VisionTracker((-10, 10), (-10, 10), repaint_tolerance=2)
  vt.visualize()

  ny, np = vt.get_next_target(0, 0)
  for i in range(1000):
    vt.update_val(ny, np, random.randint(1, 5))
    ny, np = vt.get_next_target(ny, np)
    vt.visualize()
    time.sleep(0.2)

