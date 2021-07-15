#! /usr/bin/python3

import sys, os, csv
sys.path.append('../GillesPy2')
sys.path.append('../GillesPy2/test')
import pickle
import gillespy2
from gillespy2 import SSACSolver
from example_models import *
from time import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from gillespy2.solvers.stochkit import *

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

# Create list of sample points
trajectories = [2**i for i in range(order)]
s = 'GillesPy2'

# Populate models and dict for dataframe
models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
times = {m.name:[] for m in models}
times['trajectories'] = []
print('Number of Trajectories: {}'.format(trajectories))
times['Solver'] = [s]*len(trajectories)
times['trajectories'].extend(trajectories)

# Loop over models and trajectories (by order)
for i, m in enumerate(models):
    solver = SSACSolver(m)
    for t in tqdm(trajectories, desc='Model: {}, Solver: {}'.format(m.name, s)):
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            m.run(solver=solver, number_of_trajectories=t)
            end = time()
            all_times[j] = end-start
        times[m.name].append(np.average(all_times))
# Generate and store results as dataframe
df = pd.DataFrame(times, index=[times['Solver'], times['trajectories']], columns=[m.name for m in models])
print(df)
df.to_pickle('/home/smatthe2/performance-testing/gillespy-times.p')

