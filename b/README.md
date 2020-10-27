# KrpSim

About
-----
>This project introduces us in solving a NP-hard problem.
>
>We had to create a program that generate a task schedule under time/resources constraints.

This is the second project of the Advanced Algorithm branch at School 42 Paris

Implemented Algorithms
----------------------
- [Parallel Schedule Generation Scheme](./images/Parallel_SGS.png/) as described in [1].

- [Genetic Algorithm Scheme](./images/Genetic_Algorithm_Scheme.png) as described in [1]

Installation
------------
Run `make install`

Usage
-----
`python3 -m krpsim [-h] [-a {sgs,genetic}] [-c CYCLE] [-v] [-s SEED] [--sample SAMPLE] [--mutation MUTATION] [--gen GEN] [--size SIZE] file delay`

Positional arguments:
  * file: Name of the configuration file.
  * delay: Maximum time that the solver can use.

Optional arguments:
  * -h: Show help message and exit.
  * -a {sgs, genetic}: Algorithm for the optimization.
  * -c CYCLE: Maximum cycle at which the solver will stop.
  * -v: Enable verbose mode.
  * -s SEED: Initialize the random number generator.
  * --sample SAMPLE: Number of sample for initial population.
  * --mutation MUTATION: Number of mutations (only for -a genetic).
  * --gen GEN: Number max generation (only for -a genetic).
  * --size SIZE: Size of population (only for -a genetic).


`python3 -m krpsim.verif [-h] file result`

Positional arguments:
  * file: Name of the configuration file.
  * result: Path to result.

Optional arguments:
  * -h: Show help message and exit

### Example

First we need a configuration file which look like this:
```
> cat examples/simple
#
# ultra simple demo - krpsim
#
# stock      name:quantity
euro:10
#
# process   name:(need1:qty1;need2:qty2;[...]):(result1:qty1;result2:qty2;[...]):delay
#
achat_materiel:(euro:8):(materiel:1):10
realisation_produit:(materiel:1):(produit:1):30
livraison:(produit:1):(client_content:1):20
#
# optimize time for no process possible (eating stock, produce all possible),
# or maximize some products over a long delay
# optimize:(time|stock1;time|stock2;...)
#
optimize:(time;client_content)
#
```
Then we can run `krpsim` to generate a schedule
```
> python3 -m krpsim examples/simple 1 -v
# Simulation description:
# 3 processes, # 4 stocks, # 2 to optimize
# === Stocks:
# euro: 10
# materiel: 0
# produit: 0
# client_content: 0
# === Processes:
# achat_materiel: (euro: 8): (materiel: 1): 10
# realisation_produit: (materiel: 1): (produit: 1): 30
# livraison: (produit: 1): (client_content: 1): 20
# === Optimizing:
# time
# client_content

# Main walk
0:achat_materiel
10:realisation_produit
40:livraison
# No more process doable at cyle 61
# Stock :
#  euro => 2
#  materiel => 0
#  produit => 0
#  client_content => 1
```
The generated schedule is then saved in a file named `example/simple.log`
```
> cat examples/simple.log
# Main walk
0:achat_materiel
10:realisation_produit
40:livraison
# No more process doable at cyle 61
# Stock :
#  euro => 2
#  materiel => 0
#  produit => 0
#  client_content => 1
```
We can then verify if the schedule is realisable with `krpsim.verif`
```
> python3 -m krpsim.verif examples/simple examples/simple.log
# Simulation description:
# 3 processes, # 4 stocks, # 2 to optimize
# === Stocks:
# euro: 10
# materiel: 0
# produit: 0
# client_content: 0
# === Processes:
# achat_materiel: (euro: 8): (materiel: 1): 10
# realisation_produit: (materiel: 1): (produit: 1): 30
# livraison: (produit: 1): (client_content: 1): 20
# === Optimizing:
# time
# client_content

Evaluating: 0:achat_materiel
Evaluating: 10:realisation_produit
Evaluating: 40:livraison
Trace completed, no error detected.
```

References
--------------
[1] Sonke Hartmann - Project Scheduling under Limited Resources (1999)

##### Project done in 2020
