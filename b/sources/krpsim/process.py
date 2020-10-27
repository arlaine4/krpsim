class Process(object):
  def __init__(self, name, delay):
    self.name = name
    self.needs = {}
    self.results = {}
    self.score = {}
    self.delay = delay

  def __str__(self):
    rep = f"{self.name}: ("
    for name, quantity in self.needs.items():
      rep += f"{name}: {quantity};"
    rep = rep[:-1] + "): ("
    for name, quantity in self.results.items():
      rep += f"{name}: {quantity};"
    rep = rep[:-1] + f"): {self.delay}"
    return rep

  def need(self, name, quantity):
    self.needs[name] = quantity
    if name in self.score:
      self.score[name] -= (quantity / self.delay)
    else:
      self.score[name] = -(quantity / self.delay)
    return self

  def result(self, name, quantity):
    self.results[name] = quantity
    if name in self.score:
      self.score[name] += (quantity / self.delay)
    else:
      self.score[name] = (quantity / self.delay)
    return self
