


class Action:

  # action types: voice, head, body
  def __init__(self, action_type = "", data = {}, priority = 0.1):
      self.priority = priority
      self.data = data
      self.action_type = action_type
  def serialize(self):
      return "{} {}".format(action_types)