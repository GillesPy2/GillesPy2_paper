#! /usr/bin/python3

import sys, os, csv
sys.path.append("../GillesPy2")
sys.path.append("../GillesPy2/test")
import roadrunner
import tellurium
import pickle
from time import time
from tqdm import tqdm
import numpy as np
import pandas as pd
from gillespy2 import Species, Parameter, Reaction
from example_models import *
from SBMLexport import export

try:
    order = int(sys.argv[1])
except:
    order = 1

try:
    realizations = int(sys.argv[2])
except:
    realizations = 1

def rr_run(mod, tspan):
    mod.reset()
    mod.gillespie(*tspan)

models = [VilarOscillator(), MichaelisMenten(), Dimerization()]
paths = {"VilarOscillator":'/home/brumsey/system-testing/Vilar_Oscillator.xml',
         "Michaelis_Menten":'/home/brumsey/system-testing/Michaelis_Menten.xml',
         "Dimerization":'/home/brumsey/system-testing/Dimerization.xml'}

def get_system_size(m):
    size = len(m.listOfSpecies)+len(m.listOfParameters)+len(m.listOfReactions)
    return size

def build_order_models(models, paths):
    # List of order paths for each model
    model_paths = []
    sizes = []
    for i, m in enumerate(models):
        # list of paths to a model with varying system sizes
        order_paths = []
        for o in range(order):
            if i <= 0:
                sizes.append([])
            if o > 0:
                # create a path for the model of the current order
                path = paths[m.name].replace('.xml', f'{o}.xml')
                # increase the system size of the model for this order
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
            else:
                path = paths[m.name]
            order_paths.append(path)
            # convert the gillespy model to an sbml file for this order
            if os.path.exists(path):
                os.remove(path)
            export(m, path=path)
            # add the system size to sizes
            sizes[o].append(get_system_size(m))
        # add the list of order paths to the model paths
        model_paths.append(order_paths)
    system_sizes = list(map(lambda s: str(s), sizes))
    return model_paths, system_sizes

models, system_sizes = build_order_models(models, paths)
m_names = ['VilarOscillator', 'Michaelis_Menten', 'Dimerization']
tspans = [(0, 200, 201), (0, 100, 101), (0, 100, 101)]
s = 'RoadRunnerGillesPie'
times = {m:[] for m in m_names}
times['Solver'] = [s]*len(system_sizes)
times['system_sizes'] = system_sizes
print('Size of the Systems: {}'.format(system_sizes))
for i, m in enumerate(models):
    for o in tqdm(range(order), desc='Model: {}, Solver: {}'.format(m_names[i], s)):
        rr = roadrunner.RoadRunner(m[o])
        all_times = np.zeros(realizations)
        for j in range(realizations):
            start = time()
            results = rr_run(rr, tspans[i])
            end = time()
            all_times[j] = end-start
        times[m_names[i]].append(np.average(all_times))

df = pd.DataFrame(times, index=[times['Solver'], times['system_sizes']],
                    columns=[m for m in m_names])
# print('arrangement 1')
print(df)
df.to_pickle('/home/brumsey/system-testing/rr-times.p')
# df = df.T
# print('\n\n')
# print('arrangement 2')
# print(df)


