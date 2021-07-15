#! /usr/bin/python3

import subprocess
import sys

try:
    order = sys.argv[1]
except:
    order = '1'
# realizations: number of samples at each order input
try:
    realizations = sys.argv[2]
except:
    realizations = '1'

subprocess.run(['python3', 'stochkit_tests.py', order, realizations])
subprocess.run(['julia', 'biosimulator-test.jl', order, realizations])
subprocess.run(['python3', 'roadrunner_tests.py', order, realizations])
subprocess.run(['python3', 'gillespy_tests.py', order, realizations])
