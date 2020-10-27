#!/usr/bin/env python3
import argparse

from krpsim.parser import parse_config, parse_trace
from krpsim.utils import check


def verif(sim, trace):
  """Checks that the execution runs correctly, or output the cycle/process that
  causes trouble"""
  S = []
  for t, j in trace:
    S.append((t, sim.get_process(j)))
  idx = check(0, sim.stocks, S, verbose=True)
  if idx != -1:
    t, name = trace[idx]
    j = sim.get_process(name)
    print("====== Error detected")
    print(f"at {t}:{j.name} stock insufficient")
    print("======= Exiting...")
    return False
  return True


if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('file', action="store", type=str, default=None,
                      help="Name of the configuration file.")
  parser.add_argument('result', action="store", type=str, default=None,
                      help="Path to result.")

  args = parser.parse_args()
  KrpSim, trace = parse_config(args.file), parse_trace(args.result)

  if KrpSim is None or trace is None:
    exit(1)

  print(KrpSim)
  if verif(KrpSim, trace):
    print("Trace completed, no error detected.")
