#! /usr/bin/python3

import pickle
import pandas as pd
import sys

biosimulator_times = pickle.load(open('bsjl-times.p', 'rb'))
gillespy_times = pickle.load(open('gillespy-times.p', 'rb'))
rr_times = pickle.load(open('rr-times.p', 'rb'))
stochkit_times = pickle.load(open('stochkit-times.p', 'rb'))

all_results = gillespy_times.append(rr_times).append(biosimulator_times).append(stochkit_times)
print(all_results)

from matplotlib import pyplot as plt
df = all_results
order = int(len(df['VilarOscillator'].index) / 4)
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
xlab = [x[1] for x in df['VilarOscillator'].index[0:order]]
ax1.set_title('Vilar Oscillator')
#ax1.set_xscale('log', basex=2)
l1, = ax1.plot(xlab, df['VilarOscillator'].values[0:order])
l2, = ax1.plot(xlab, df['VilarOscillator'].values[order:order*2])
l3, = ax1.plot(xlab, df['VilarOscillator'].values[order*2:order*3])
l4, = ax1.plot(xlab, df['VilarOscillator'].values[order*3:order*4])
ax2.set_title('Michaelis Menten')
ax2.plot(xlab, df['Michaelis_Menten'].values[0:order])
ax2.plot(xlab, df['Michaelis_Menten'].values[order:order*2])
ax2.plot(xlab, df['Michaelis_Menten'].values[order*2:order*3])
ax2.plot(xlab, df['Michaelis_Menten'].values[order*3:order*4])
ax3.set_title('Dimerization')
ax3.plot(xlab, df['Dimerization'].values[0:order])
ax3.plot(xlab, df['Dimerization'].values[order:order*2])
ax3.plot(xlab, df['Dimerization'].values[order*2:order*3])
ax3.plot(xlab, df['Dimerization'].values[order*3:order*4])
ax3.set_xlabel('System Size [Number Species, Number Parameters, Number Reactions]')
ax3.set_ylabel('Time')
plt.legend([l1, l2, l3, l4], ['GillesPy2', 'RoadRunner', 'BioSimulator.jl', 'StochKit'])
plt.show()
all_results.to_csv('./all_results.csv')
