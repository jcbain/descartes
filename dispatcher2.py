from __future__ import print_function
import subprocess
import argparse
import os
import re
import random

from itertools import product
from time import gmtime, strftime

def run_slim_process():
    command = "slim -d m=1e-6 -d mu=1e-6 -d sigsqr=2 -d N=1000 -d numpos=160 -d r=0.00625 -d outputEvery=1000 local_adaptation.slim"
    process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
    out, err = process.communicate()

    print(out)

if __name__ == "__main__":
    run_slim_process()