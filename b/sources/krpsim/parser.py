import re

from krpsim.process import Process
from krpsim.simulation import Simulation

REGEX = {
  1: re.compile(r"(.*?):(.*)"),
  2: re.compile(r"(.*?):(.*):+(.*)"),
  3: re.compile(r"\((.*?)\)"),
  4: re.compile(r"optimize:\((.*)\)"),
}


def parse_optimize(line, sim, config):
  p = REGEX[4]
  try:
    if len(sim.optimizing) > 0:
      raise Exception("Multiple optimize keyword found.")
    occurence = p.findall(line)[0]
    for optimize in occurence.split(';'):
      sim.optimize(optimize)
  except Exception:
    config['error'] = f"=====\n"
    config['error'] += f"Error while parsing `{line}`\n"
    config['error'] += f"=====\nExiting..."

  return config


def parse_process(line, sim, config):
  p = REGEX[2]

  try:
    occurence = p.findall(line)[0]
    name, materials, delay = occurence[0], occurence[1], int(occurence[2])
    if name == '':
      raise Exception("Empty process name.")
    process = Process(name, delay)

    p = REGEX[3]
    needs, results = p.findall(materials)

    p = REGEX[1]
    for need in needs.split(';'):
      if need == '':
        continue
      occurence = p.findall(need)[0]
      name, quantity = occurence[0], int(occurence[1])
      process.need(name, quantity)
      sim.stock(name, 0)

    for result in results.split(';'):
      if result == '':
        continue
      occurence = p.findall(result)[0]
      name, quantity = occurence[0], int(occurence[1])
      process.result(name, quantity)
      sim.stock(name, 0)

    sim.process(process)
    return config
  except Exception:
    config['process'] = False
    config['optimize'] = True

  return parse_optimize(line, sim, config)


def parse_stock(line, sim, config):
  p = REGEX[1]

  try:
    occurence = p.findall(line)[0]
    name, quantity = occurence[0], int(occurence[1])
    if name == '':
      raise Exception("Empty stock name.")
    sim.stock(name, quantity)
    return config
  except Exception:
    config['stock'] = False
    config['process'] = True
  return parse_process(line, sim, config)


def parse_config(file):
  config = {'stock': True, 'process': False, 'optimize': False, 'error': None}
  KrpSim = Simulation()

  try:
    with open(file, 'r') as f:
      raw = [re.sub('#.*', '', line.strip()) for line in f]
      for line in raw:
        if not line:
          continue

        if config['stock']:
          parse_stock(line, KrpSim, config)
        elif config['process']:
          parse_process(line, KrpSim, config)
        elif config['optimize']:
          parse_optimize(line, KrpSim, config)

        if config['error'] is not None:
          print(config['error'])
          return None
      if len(KrpSim.processes) == 0:
        raise Exception("Missing processes.")
  except Exception as e:
    if config['error'] is not None:
      print(config['error'])
    else:
      print("Error encontered while parsing.")
      print(f"=====\n{e}\n=====\nExiting...")
    return None

  return KrpSim


def parse_trace(file):
  trace = []

  try:
    with open(file, 'r') as f:
      raw = [re.sub('#.*', '', line.strip()) for line in f]
      raw = [line.split(':') for line in raw if line]
    for cycle, name in raw:
      trace.append((int(cycle), name))
  except Exception as e:
    print("Error encontered while parsing.")
    print(f"=====\n{e}\n=====\nExiting...")
    return None

  return trace
