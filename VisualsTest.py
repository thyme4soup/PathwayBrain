
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
    self.dirtied = []

    for r in range(rows):
      for c in range(cols):
        self.dirty(r, c)

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
      self.dirtied.append((r, c))
      return 0

  def index_to_coords(self, r, c):
    return (
      c * self.yaw_step + self.yaw_min,
      r * self.pitch_step + self.pitch_min
    )
  def coords_to_index(self, y, p):
    return (
      (y - self.yaw_min) // self.yaw_step,
      (p - self.pitch_min) // self.pitch_step
    )

  def get_next_target(self, cur_yaw, cur_pitch):
    if len(self.dirtied) > 0:
      r, c = self.dirtied.pop(0)
      return self.index_to_coords(r, c)
    else:
      r, c = self.cov
      return self.index_to_coords(r, c)

  def update_val(self, cur_yaw, cur_pitch, distance):
    r, c = self.coords_to_index(cur_yaw, cur_pitch)
    old = self.fov[r][c]
    if old and abs(distance - old) > self.repaint_tolerance:
      for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        self.dirty(nr, nc)
    self.fov[r][c] = distance


if __name__ == '__main__':
  vt = VisionTracker((-5, 5), (-5, 5))
  vt.visualize()
  vt.fov[3][3] = 1

  ny, np = vt.get_next_target(0, 0)
  for i in range(100):
    vt.update_val(ny, np, random.randint(1, 5))
    ny, np = vt.get_next_target(ny, np)
    vt.visualize()
    time.sleep(0.2)

