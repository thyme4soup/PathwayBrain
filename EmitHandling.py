import threading
import time

class Handler:

  def __init__(self):
    self.listeners = {}

  def emit(self, notice, data = None):
    for task in self.listeners.get(notice, set()):
      threading.Thread(target=task, args=(data,)).start()

  def listen(self, notice, target):
    targets = self.listeners.get(notice, None)
    if targets != None:
      targets.add(target)
    else:
      self.listeners[notice] = set([target])

  def deafen(self, target, notice=None):
    if notice != None:
      targets = self.listeners.get(notice, [])
      targets.remove(target)
    else:
      for _, targets in self.listeners.items():
        targets.remove(target)


if __name__ == '__main__':
  print("Emitter Testing")