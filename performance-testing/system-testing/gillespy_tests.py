#! /usr/bin/python3

import sys, os, csv
sys.path.append('../GillesPy2')
sys.path.append('../GillesPy2/test')
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
from SBMLexport import export

# Read args
# order: run a geometric series using system size in range 2^0 * system - 2^x * system
try:
    order = int(sys.argv[1])
except:
    order = 1
# realizations: number of samples at each order input
try:
    realizations = int(sys.argv[2])
except:
    realizations = 1

# Get the original system size
def get_system_size(m):
    size = len(m.listOfSpecies)+len(m.listOfParameters)+len(m.listOfReactions)
    return size

# Create list of sample points
models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
system_sizes = [str([get_system_size(m) * 2**i for m in models]) for i in range(order)]
s = 'GillesPy2'

# Populate models and dict for dataframe
times = {m.name:[] for m in models}
times['system_sizes'] = system_sizes
print('Size of the Systems: {}'.format(system_sizes))
times['Solver'] = [s]*len(system_sizes)

# Loop over order and models
for i, m in enumerate(models):
    for o in tqdm(range(order), desc='Model: {}, Solver: {}'.format(m.name, s)):
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
        solver = SSACSolver(m)
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            m.run(solver=solver)
            end = time()
            all_times[j] = end-start
        times[m.name].append(np.average(all_times))
print(times)
# Generate and store results as dataframe
df = pd.DataFrame(times, index=[times['Solver'], times['system_sizes']], columns=[m.name for m in models])
print(df)
df.to_pickle('/home/brumsey/system-testing/gillespy-times.p')

