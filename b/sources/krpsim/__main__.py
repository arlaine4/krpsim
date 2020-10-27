#!/usr/bin/env python3
import argparse

from krpsim.parser import parse_config
from krpsim.solvers import GeneticAlgorithm, ParallelSGS

SOLVERS = {
  "sgs": ParallelSGS,
  "genetic": GeneticAlgorithm,
}

CHOICES = SOLVERS.keys()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('file', action="store", type=str, default=None,
                      help="Name of the configuration file.")
  parser.add_argument('delay', action="store", type=float, default=10,
                      help="Maximum time that the solver can use.")
  parser.add_argument('-a', "--algorithm",
                      type=str, default="sgs",
                      choices=CHOICES,
                      help="Algorithm for the optimization.")
  parser.add_argument('-c', "--cycle", type=int, default=None,
                      help="Maximum cycle at which the solver will stop.")
  parser.add_argument('-v', "--verbose", action="store_true", default=False,
                      help="Enable verbose mode.")
  parser.add_argument('-s', "--seed", type=int, default=None,
                      help="Initialize the random number generator.")
  parser.add_argument("--sample", type=int, default=None,
                      help="Number of sample for initial population.")
  parser.add_argument("--mutation", type=int, default=None,
                      help="Number of mutations (only for -a genetic).")
  parser.add_argument("--gen", type=int, default=None,
                      help="Number max generation (only for -a genetic).")
  parser.add_argument("--size", type=int, default=None,
                      help="Size of population (only for -a genetic).")

  args = parser.parse_args()
  KrpSim = parse_config(args.file)

  if KrpSim is None:
    exit(1)

  print(KrpSim)
  file = args.file + '.log'
  kwargs = {
    'delay': args.delay,
    'cycle': args.cycle,
    'file': file,
    'verbose': args.verbose,
    'seed': args.seed,
  }

  if args.sample is not None:
    kwargs['sample'] = args.sample
  if args.mutation is not None:
    kwargs['mutation'] = args.mutation
  if args.gen is not None:
    kwargs['gen'] = args.gen
  if args.size is not None:
    kwargs['size'] = args.size
  solver = SOLVERS[args.algorithm](KrpSim, **kwargs)
  solver.run()
