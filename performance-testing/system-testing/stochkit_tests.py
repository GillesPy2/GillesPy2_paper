#! /usr/bin/python3

import sys, os, csv
sys.path.insert(0, '../GillesPy2')
sys.path.insert(1, '../GillesPy2/test')
import pickle
import gillespy2
from gillespy2 import Species, Parameter, Reaction
from gillespy2 import SSACSolver
from example_models import *
from time import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from gillespy2.solvers.stochkit import *

if 'STOCHKIT_HOME' not in os.environ:
    os.environ['STOCHKIT_HOME'] = "/home/brumsey/StochKit"

# Read args
# order: run a geometric series using number_of_trajectories in range 2^0 - 2^x
try:
    order = int(sys.argv[1])
except:
    order = 1
# realizations: number of samples at each order input
try:
    realizations = int(sys.argv[2])
except:
    realizations = 1

# get the system size of a model
def get_system_size(m):
    return len(m.listOfSpecies)+len(m.listOfParameters)+len(m.listOfReactions)

# Create list of sample points
models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
system_sizes = [str([get_system_size(m)*2**i for m in models]) for i in range(order)]
s = 'StochKit'

times = {m.name:[] for m in models}
times['system_sizes'] = system_sizes
print('Size of the Systems: {}'.format(system_sizes))
times['Solver'] = [s]*len(system_sizes)

for i, m in enumerate(models):
    for o in tqdm(range(order), desc='{} - {}'.format(s, m.name)):
        if o > 0:
            n_s = [Species(name=f"{n}_{o}", initial_value=s.initial_value, mode=s.mode) for n, s in m.listOfSpecies.items()]
            m.add_species(n_s)
            n_p = [Parameter(name=f"{n}_{o}", expression=p.expression) for n, p in m.listOfParameters.items()]
            m.add_parameter(n_p)
            n_r = []
            for n, r in m.listOfReactions.items():
                reactants = {f"{species.name}_{o}": ratio for species, ratio in r.reactants.items()}
                products = {f"{species.name}_{o}": ratio for species, ratio in r.products.items()}
                rate = m.listOfParameters[f"{r.marate.name}_{o}"]
                n_r.append(Reaction(name=f"{n}_{o}", reactants=reactants, products=products, rate=rate))
            m.add_reaction(n_r)
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            m.run(solver=StochKitSolver())
            end = time()
            all_times[j] = end-start
        times[m.name].append(np.average(all_times))

df = pd.DataFrame(times, index=[times['Solver'], times['system_sizes']], columns=[m.name for m in models])
print(df)
df.to_pickle('/home/brumsey/system-testing/stochkit-times.p')


