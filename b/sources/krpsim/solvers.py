import random
import time

from krpsim.utils import check
import numpy as np


class Solver(object):
  def __init__(self, sim, **kwargs):
    self.sim = sim
    self.sim.filter_processes()

    self.begin = time.time()
    self.delay = kwargs['delay']
    self.cycle = kwargs['cycle'] or np.Inf
    self.verbose = kwargs['verbose']
    self.seed = kwargs['seed']
    self.file = open(kwargs['file'], "w")

    random.seed(self.seed)

    Rbounds = {}
    for process in self.sim.elligibles:
      for need, amount in process.needs.items():
        if need in Rbounds:
          Rbounds[need] = max(Rbounds[need], amount)
        else:
          Rbounds[need] = amount
    for optimize in self.sim.optimizing:
      if optimize in Rbounds:
        del Rbounds[optimize]
    self.Rbounds = Rbounds

  def run(self):
    pass

  def manage_output(self, string):
    if self.verbose:
      print(string)
    print(string, file=self.file)

  def ouput(self, path, tg):
    self.manage_output("# Main walk")
    for cycle, proc in path:
      self.manage_output(f"{cycle}:{proc}")
    self.manage_output(f"# No more process doable at cyle {tg + 1}")
    self.sim.print_stocks(file=self.file)
    if self.verbose:
      self.sim.print_stocks()

################################################################################
################################################################################
# .d8888.  d888b  .d8888.
# 88'  YP 88' Y8b 88'  YP
# `8bo.   88      `8bo.
#   `Y8b. 88  ooo   `Y8b.
# db   8D 88. ~8~ db   8D
# `8888Y'  Y888P  `8888Y'
################################################################################
################################################################################


class ParallelSGS(Solver):
  """Parallel Shedule Generation Scheme

  Parameters
  ----------
  sim: Simulation
    Current simulation to evaluate
  delay: int
    Max running time for simulation

  Attributes
  ----------
  begin: float
    Time at which the simulation started
  """
  def __init__(self, sim, **kwargs):
    super().__init__(sim, **kwargs)

    self.theorical_stocks = {}
    for key, values in self.sim.stocks.items():
      self.theorical_stocks[key] = values

  def minimum_finished_time(self, Ag, F):
    minF = np.Inf
    for _, job in Ag:
      key = job.name
      if F[key] < minF:
        minF = F[key]
    return minF if minF != np.Inf else 0

  def update_jobs(self, Cg, Ag, F, tg):
    to_remove = []
    for cycle, job in Ag:
      key = job.name
      if F[key] <= tg:
        self.sim.update_stocks(job.results)
        Cg.append((cycle, job.name))
        to_remove.append((cycle, job))
    for remove in to_remove:
      Ag.remove(remove)

    self.theorical_stocks = {}
    for key, values in self.sim.stocks.items():
      self.theorical_stocks[key] = values
    return Cg, Ag

  def update_stocks(self, job):
    self.sim.update_stocks(job.needs, remove=True)
    for key, value in job.needs.items():
      self.theorical_stocks[key] -= value
    for key, value in job.results.items():
      self.theorical_stocks[key] += value

  def h_select(self, Eg):
    """Heurisitic based selection"""
    for job in Eg:
      for key in job.results:
        if key in self.sim.optimizing:
          return job

    for job in Eg:
      for key in job.results:
        if key in self.Rbounds:
          if self.theorical_stocks[key] >= self.Rbounds[key]:
            continue
        return job

    return None

  def is_finished(self, Ag, tg):
    if time.time() - self.begin > self.delay:
      return True
    if tg >= self.cycle:
      return True
    if tg != 0 and len(Ag) == 0:
      return True
    return False

  def run(self):
    """Main Algorithm for ParallelSGS
    Attributes
    ----------
    g : Depth
    tg: Time at depth g
    Ag: Active jobs at depth g
    Cg: Completed jobs until depth g
    F : Finished times for jobs
    Eg: Elligibles jobs at depth g
    j : Current job
    """
    g = 0
    tg = 0
    Ag = []
    Cg = []
    F = {}
    while not self.is_finished(Ag, tg):
      g += 1
      tg = self.minimum_finished_time(Ag, F)
      Cg, Ag = self.update_jobs(Cg, Ag, F, tg)
      Eg = self.sim.get_elligibles()
      while len(Eg) > 0:
        j = self.h_select(Eg)
        if j is None:
          break
        F[j.name] = tg + j.delay
        Ag.append((tg, j))
        self.update_stocks(j)
        Eg = self.sim.get_elligibles()

    for _, job in Ag:
      self.sim.update_stocks(job.needs)
    Cg.sort(key=lambda j: j[0])
    self.ouput(Cg, tg)

################################################################################
################################################################################
#  d888b   .d8b.
# 88' Y8b d8' `8b
# 88      88ooo88
# 88  ooo 88~~~88
# 88. ~8~ 88   88
#  Y888P  YP   YP
################################################################################
################################################################################


class Node(object):
  def __init__(self, j, T, R, tg, F):
    self.R = R
    self.j = j
    self.T = T
    self.tg = tg
    self.F = F
    self.children = []
    self.out = f"{T}:{j.name}" if j is not None else ""

  def append(self, j):
    R = {}
    for T, stock in self.R.items():
      R[T] = dict(stock)

    for k, amount in j.needs.items():
      R[self.tg][k] -= amount

    Fj = self.tg + j.delay
    if Fj not in R:
      R[Fj] = {}
    for k, amount in j.results.items():
      if k not in R[Fj]:
        R[Fj][k] = 0
      R[Fj][k] += amount

    child1 = Node(j, self.tg, R, self.tg, self.F | {Fj})
    self.children.append(child1)

    remove = set()
    R2 = {}
    for T, stock in R.items():
      R2[T] = dict(stock)

    for T in self.F:
      if T < Fj:
        remove.add(T)
        for k, amount in R2[T].items():
          if k not in R2[Fj]:
            R2[Fj][k] = 0
          R2[Fj][k] += amount

    child2 = Node(j, self.tg, R2, Fj, (self.F ^ remove) | {Fj})
    self.children.append(child2)
    return (child1, child2)

  def update_R(self):
    Fj = sorted(self.F)[0]
    if self.tg == Fj:
      self.F.remove(Fj)
      return self

    for k, amount in self.R[self.tg].items():
      if k not in self.R[Fj]:
        self.R[Fj][k] = 0
      self.R[Fj][k] += amount

    self.tg = Fj
    return self

  def stocks(self):
    return self.R[self.tg]

  def __str__(self, depth=-1):
    ret = ""
    if self.j is not None:
      ret += "|\t"*depth + f"{self.out}\n"
    for child in self.children:
        ret += child.__str__(depth + 1)
    return ret

  def to_list(self):
    S = [self]
    dS = [[]]
    lists = []
    while len(S) > 0:
      node = S.pop()
      d = dS.pop()
      if len(node.children) == 0:
        lists.append(d + [node])
      for child in node.children:
        S.append(child)
        dS.append(d + [node])
    return lists

  def fitness(self, priority, Rbound):
    score = 0
    tg = 1
    R = self.R[self.tg]
    for k, idx in priority.items():
      if k == 'time':
        tg = max(tg, self.tg)
        continue
      prod = R[k]
      if k in Rbound:
        bound = Rbound[k]
        val = min(prod / bound, 1)
        malus = (prod / bound) - val
        score += (val - malus) * (1 / (10 ** idx))
      else:
        score += prod * (1 / (10 ** idx))
    return score / tg


SAMPLE = 10
MUTATION = 1
GEN = 100
SIZE = 25
TIME_RATIO = 0.1


class GeneticAlgorithm(Solver):
  def __init__(self, sim, **kwargs):
    super().__init__(sim, **kwargs)
    self.sample = SAMPLE if 'sample' not in kwargs else kwargs['sample']
    self.mut = MUTATION if 'mutation' not in kwargs else kwargs['mutation']
    self.gen = GEN if 'gen' not in kwargs else kwargs['gen']
    self.size = SIZE if 'size' not in kwargs else kwargs['size']
    print("# Genetic Algorithm parameters:")
    print(f"# Random Sample: {self.sample}")
    print(f"# Number of Mutations: {self.mut}")
    print(f"# Number of Generations: {self.gen}")
    print(f"# Population Size: {self.size}\n")

  def sgs_finished(self, tg):
    if time.time() - self.begin > self.delay * TIME_RATIO:
      return True
    if tg >= self.cycle:
      return True
    return False

  def SGS(self, node):
    stack = [node]
    while len(stack) > 0:
      if self.sgs_finished(node.tg):
        return
      node = stack.pop()
      Eg = self.sim._get_elligibles(node.stocks())
      while len(Eg) == 0 and len(node.F) > 0:
        node.update_R()
        Eg = self.sim._get_elligibles(node.stocks())
      if len(Eg) == 0:
        continue
      for _ in range(self.sample):
        if len(Eg) == 0:
          continue
        choice = random.choice(Eg)
        node.append(choice)
        Eg.remove(choice)
      for child in node.children:
        stack.append(child)

  def is_finished(self, g):
    if time.time() - self.begin > self.delay:
      return True
    if g >= self.gen:
      return True
    return False

  def inherit(self, mother, father):
    child = []
    upper = min(len(mother), len(father)) - 1
    Q = random.randint(0, upper)
    for i in range(Q):
      node = mother[i]
      R = {}
      for T, stock in node.R.items():
        R[T] = dict(stock)
      child.append(Node(node.j, node.T, R, node.tg, set(node.F)))
    for j in range(Q, len(father)):
      node = father[j]
      R = {}
      for T, stock in node.R.items():
        R[T] = dict(stock)
      child.append(Node(node.j, node.T, R, node.tg, set(node.F)))
    return child

  def crossover(self, pop):
    children = []
    size = int(self.size / 2)
    for i in range(size):
      mother = pop[2 * i]
      father = pop[2 * i + 1]
      children.append(self.inherit(mother, father))
      children.append(self.inherit(father, mother))
    return children

  def mutation(self, child):
    for _ in range(self.mut):
      S = [(n.T, n.j) for n in child[1:]]

      if len(child) < 2:
        break

      idx = check(child[1].T, child[0].stocks(), S)
      if idx == -1:
        idx = random.randint(1, len(child))

      Fj = child[-1].tg if self.cycle == np.Inf else self.cycle
      child = child[:idx]
      node = child[-1]
      while node.tg < Fj:
        Eg = self.sim._get_elligibles(node.stocks())
        while len(Eg) == 0 and len(node.F) > 0:
          node.update_R()
          Eg = self.sim._get_elligibles(node.stocks())
        if len(Eg) == 0:
          break
        choice = random.choice(Eg)
        new_children = node.append(choice)
        child.append(random.choice(new_children))
        node = child[-1]

    return child

  def fitness(self, individual):
    score = 0
    prevS = 0
    priority = self.sim.priority
    Rbounds = self.Rbounds
    size = len(individual)
    for i in range(size):
      node = individual[i]
      scale = max(i / size, 1e-2)
      S = node.fitness(priority, Rbounds)
      if S < prevS:
        score += scale * (S - prevS)
      else:
        score += scale * S
      prevS = S

    return score / size

  def run(self):
    R = {0: dict(self.sim.stocks)}

    # TODO: Can use ParallelSGS with random selection for initial population
    root = Node(None, 0, R, 0, {0})
    self.SGS(root)
    pop = root.to_list()
    while len(pop) < self.size:
      pop.append(random.choice(pop))
    pop = pop[:self.size]

    g = 1
    pop.sort(key=lambda x: self.fitness(x), reverse=True)
    while not self.is_finished(g):
      if (g - 1) % 10 == 0:
        print(f"Generation {g - 1}")
      g += 1
      children = self.crossover(pop)
      for i in range(len(children)):
        children[i] = self.mutation(children[i])
      pop.extend(children)
      pop.sort(key=lambda x: self.fitness(x), reverse=True)
      pop = pop[:self.size]

    best = pop[0]
    while len(best[-1].F) > 0:
      best[-1].update_R()
    Cg = [(node.T, node.j.name) for node in best[1:]]
    tg = best[-1].tg
    self.sim.stocks = best[-1].stocks()
    self.ouput(Cg, tg)
