from __future__ import print_function
import subprocess
import argparse
import os
import re
import random

from itertools import product
from time import gmtime, strftime
from helpers import output_manipulators

def create_params(param_str, *opts):
    """
    Creates a list of explicit simulation parameter options for a single parameter.

    Parameters
    ----------
    param_str: str
       A string parameter option to be modified which will generally take on the for of "<param>=". For example, to
       specify the rate of migration (m) you would input "m=".
    opts: str
       Any number of parameter values that you wish to run for any given parameter. For example, if you wanted to run a
       simulation with migrations rates of 1e-5 and 1e-3 then you would pass `"1e-5", "1e-3"` as arguments after the
       `param_str` option.

    Returns
    -------
    list
        A list of strings explicitly specifying the parameter to be run within the slim script.

    Examples
    --------
    To specify a simulation that runs migration rates (m) set to 1-e5 and 1-e4 you would:
    >>> create_params("m=", "1e-5", "1e-3")
    ["m=1e-5", "m=1e-6"]
    """
    return [param_str + "{}".format(opt) for opt in opts]

def create_file_name(x, dataset):
    """
    Creates a file name from the given parameter set.

    Parameters
    ----------
    x: list
        A set of parameter options.
    dataset: str
        A particular dataset parsed from the output of slim.

    Returns
    -------
    file_name: str
        A file name string.
    """
    cleaned_x = map(lambda y: re.sub("=", "", y), x)
    file_name = "_".join(list(cleaned_x)) + "_" + dataset + ".txt"
    return file_name


def run_slim_process():

    cwd = os.getcwd() + '/'
    output_dir = cwd + 'run' + strftime("%Y%m%d_%H%M%S", gmtime()) + '_' + str(random.randint(1, 1000)) + '/'
    os.mkdir(output_dir)

    parser = argparse.ArgumentParser()

    parser.add_argument('--rep', action='store', type=int, default=3)
    parser.add_argument('--m', action='store', type=str, default="1e-5")
    parser.add_argument('--mu', action='store', type=str, default="1e-6")
    parser.add_argument('--numpos', action='store', type=str, default="160")
    parser.add_argument('--r', action='store', type=str, default="1e-6")
    parser.add_argument('--sigsqr', action='store', type=str, default="5")
    parser.add_argument('--n', action='store', type=str, default="1000")
    parser.add_argument('--outputEvery', action='store', type=str, default="1000")

    results = parser.parse_args()

    m = create_params("m=", results.m)[0]
    mu = create_params("mu=", results.mu)[0]
    num_pos = create_params("numpos=", results.numpos)[0]
    r = create_params("r=", results.r)[0]
    sigsqr = create_params("sigsqr=", results.sigsqr)[0]
    n = create_params("N=", results.n)[0]
    output_every = create_params("outputEvery=", results.outputEvery)[0]
    reps = results.rep

    # params_list = [x for x in product(results.m, results.mu, results.numpos, results.r, results.sigsqr, results.n, results.outputEvery)]


    full = []

    for i in range(reps):
        command = "slim -d {} -d {} -d {} -d {} -d {} -d {} -d {} local_adaptation.slim".format(m, mu, num_pos, r, sigsqr, n, output_every)
        process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
        out, err = process.communicate()

        init_clause, body = output_manipulators.split_data_output(out)
        body = output_manipulators.clean_body(body)
        body = output_manipulators.append_replicate(body, i, 'rep')
        header = body[0]
        data = body[1:]
        
        if i == 0:
            full.append(header)
            full.extend(data)
        else:
            full.extend(data)

    print("\n".join(full))



if __name__ == "__main__":
    run_slim_process()