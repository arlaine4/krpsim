import numpy as np


class Simulation(object):
  def __init__(self):
    self.stocks = {}
    self.processes = []
    self.optimizing = []
    self.elligibles = []
    self.priority = {}

  def __str__(self):
    rep = f"# Simulation description:\n"
    rep += f"# {len(self.processes)} processes, "
    rep += f"# {len(self.stocks.keys())} stocks, "
    rep += f"# {len(self.optimizing)} to optimize\n"
    rep += f"# === Stocks:\n"
    for name, quantity in self.stocks.items():
      rep += f"# {name}: {quantity}\n"
    rep += f"# === Processes:\n"
    for process in self.processes:
      rep += f"# {process}\n"
    rep += f"# === Optimizing:\n"
    for name in self.optimizing:
      rep += f"# {name}\n"
    return rep

  def stock(self, name, quantity):
    if name in self.stocks:
      self.stocks[name] += quantity
    else:
      self.stocks[name] = quantity
    return self

  def update_stocks(self, new_stocks, remove=False):
    for key, value in new_stocks.items():
      sign = -1 if remove else 1
      if key in self.stocks:
        self.stocks[key] += sign * value
      else:
        self.stocks[key] = sign * value
    return self

  def print_stocks(self, file=None):
    print("# Stock :", file=file)
    for key, value in self.stocks.items():
      print(f"#  {key} => {value}", file=file)

  def process(self, process):
    self.processes.append(process)
    return self

  def optimize(self, name):
    self.optimizing.append(name)
    return self

  def _filter_process(self, optimizing, seen, depth):
    for p in self.processes:
      for r in p.results:
        if r in optimizing:
          for n in p.needs:
            if n not in self.priority:
              self.priority[n] = depth
            self.priority[n] = min(self.priority[n], depth)
          if p in seen:
            continue
          seen.append(p)
          seen = self._filter_process(p.needs.keys(), seen, depth + 1)
    return seen

  def filter_processes(self):
    self.elligibles = self._filter_process(self.optimizing, [], 0)
    for o in self.optimizing:
      self.priority[o] = -2
    return self

  def _can_pay(self, process, R):
    for key, value in process.needs.items():
      if R[key] < value:
        return False
    return True

  def _get_elligibles(self, R):
    elligibles = []
    for process in self.elligibles:
      if self._can_pay(process, R):
        elligibles.append(process)
    return elligibles

  def get_elligibles(self):
    elligibles = self._get_elligibles(self.stocks)

    def keyfunc(x):
      sort_keys = []
      for optimize in self.optimizing:
        o_score = x.score[optimize] if optimize in x.score else -np.Inf
        score = 0
        for key in x.score:
          if key == optimize:
            continue
          score += x.score[key]
        sort_keys.append(o_score)
        sort_keys.append(score)
      return sort_keys

    elligibles.sort(key=keyfunc, reverse=True)
    return elligibles

  def get_process(self, name):
    for process in self.processes:
      if process.name == name:
        return process
    return None
