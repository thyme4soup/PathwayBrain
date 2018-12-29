import random

print("hello")
MAX = 5
MIN = 0

with open("serial_feed.txt", "w+") as f:

  n = 0
  
  for i in range(500):
    f.write("{}\n".format(n))
    n = max(MIN, min(MAX, n + random.randint(-1,1)))

