#! /usr/bin/python3

import sys, os, csv
import roadrunner
import tellurium
import pickle
from time import time
from tqdm import tqdm
import numpy as np
import pandas as pd

try:
    order = int(sys.argv[1])
except:
    order = 1

try:
    realizations = int(sys.argv[2])
except:
    realizations = 1

trajectories = [2**i for i in range(order)]

def rr_run(mod, n_traj, tspan):
    for i in range(n_traj):
        mod.reset()
        mod.gillespie(*tspan)

# models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
models = ['/home/smatthe2/performance-testing/Vilar_Oscillator.xml',
                '/home/smatthe2/performance-testing/Michaelis_Menten.xml',
                '/home/smatthe2/performance-testing/Dimerization.xml']
m_names = ['VilarOscillator', 'Michaelis_Menten', 'Dimerization']
tspans = [(0, 200, 201), (0, 100, 101), (0, 100, 101)]
s = 'RoadRunnerGillesPie'
times = {m:[] for m in m_names}
times['Solver'] = []
times['trajectories'] = []
print('Number of Trajectories: {}'.format(trajectories))
times['Solver'].extend([s]*len(trajectories))
times['trajectories'].extend(trajectories)
for i, m in enumerate(models):
    rr = roadrunner.RoadRunner(m)
    for t in tqdm(trajectories, desc='Model: {}, Solver: {}'.format(m_names[i], s)):
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            results = rr_run(rr, t, tspans[i])
            end = time()
            all_times[j] = end-start
        times[m_names[i]].append(np.average(all_times))

df = pd.DataFrame(times, index=[times['Solver'], times['trajectories']],
                    columns=[m for m in m_names])
# print('arrangement 1')
print(df)
df.to_pickle('/home/smatthe2/performance-testing/rr-times.p')
# df = df.T
# print('\n\n')
# print('arrangement 2')
# print(df)


