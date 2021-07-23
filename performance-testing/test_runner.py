#! /usr/bin/python3

import subprocess
import sys

order = sys.argv[1]

subprocess.run(['python3', 'stochkit_tests.py', order])
subprocess.run(['julia', 'biosimulator-test.jl', order])
subprocess.run(['python3', 'roadrunner_tests.py', order])
subprocess.run(['python3', 'gillespy_tests.py', order])
