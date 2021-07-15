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

if 'STOCHKIT_HOME' not in os.environ:
    os.environ['STOCHKIT_HOME'] = "/home/smatthe2/StochKit"

# Read args
# order: run a geometric series using number_of_trajectories in range 2^0 - 2^x
order = int(sys.argv[1])
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
s = 'StochKit'

models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
times = {m.name:[] for m in models}
times['trajectories'] = []
print('Number of Trajectories: {}'.format(trajectories))
times['Solver'] = [s]*len(trajectories)
times['trajectories'].extend(trajectories)
for i, m in enumerate(models):
    for t in tqdm(trajectories, desc='{} - {}'.format(s, m.name)):
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            m.run(solver=StochKitSolver(), number_of_trajectories=t)
            end = time()
            all_times[j] = end-start
        times[m.name].append(np.average(all_times))

df = pd.DataFrame(times, index=[times['Solver'], times['trajectories']], columns=[m.name for m in models])
print(df)
df.to_pickle('/home/smatthe2/performance-testing/stochkit-times.p')


