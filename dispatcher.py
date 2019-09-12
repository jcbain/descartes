from __future__ import print_function
import subprocess
import argparse
import os

from itertools import product


def remove_all(x, *items):
    """
    Removes all occurrences of specified items from a list.

    Parameters
    ----------
    x : list
        List from which items must be removed.
    items
        Specified items from the list to remove.
    Returns
    -------
    list
        The original list <x> without the specified <items>.
    """
    for item in items:
        i_count = x.count(item)
        for i in range(i_count):
            x.remove(item)
    return x


def parse_output(output, rep):
    """
    Parses the data of the stdout from the slim script.

    Parameters
    ----------
    output: str
        The stdout from the slim script.
    rep: int
        The replicate number.

    Returns
    -------
    tuple
        Returns a tuple where the first item is the data and the second item is the header and the third item is some
        other metadata.
    """
    split_output = output.split("// Starting run at generation <start>:\n1")
    meta, body = split_output[0], split_output[1]
    body = body.split("\n")
    header = body[2]
    body = remove_all(body, header, '', ' ', '"')
    header = header.replace('"', '')
    body = [i + " {}".format(rep) for i in body]
    return body, header, meta


def create_params(param_str, *opts):
    """

    Parameters
    ----------
    param_str
    opts

    Returns
    -------

    """
    return [param_str + "{}".format(opt) for opt in opts]


def main():
    """
    Provides a wrapper around the slim command and runs a file for simulating local adaptation called
        `local_adaptation.slim`. This file can be run from the command line with the falling named arguments:
        --rep : The number of replicates you want to run.

    Returns:
        A call to the slim command running the script `local_adaptation.slim`
    """
    cwd = os.getcwd() + '/'

    parser = argparse.ArgumentParser()

    parser.add_argument('--rep', action='store', type=int)
    parser.add_argument('--m', action='store', type=bool, default=False)
    parser.add_argument('--mu', action='store', type=bool, default=False)
    results = parser.parse_args()

    m_string = "m="
    if not(results.m):
        m = create_params(m_string, "1e-5")  # migration rate = "m=1e-5"
    else:
        m = create_params(m_string, "1e-5", "1e-4", "1e-3")
    mu = ["mu=1e-5"]  # mutation rate
    r = ["r=1e-5"]  # recombination rate
    phi = ["phi=5"]  # fitness

    params_list = [x for x in product(m, mu, r, phi)]
    popen_unformatted = 'slim -d "{}" -d "{}" -d "{}" -d "{}" -d "{}" -d "{}" practice/local_adaptation.slim'

    output_every = "outputEvery=750"
    outfile_path = "stdout='/Users/jamesbain/Documents/research/simulations/practice/output/{}'"

   output_list = []
    for params in params_list:
        popen_string = popen_unformatted.format(params[0], params[1], params[2], params[3], output_every,
                                                outfile_path)
        rep_list = []
        for rep in range(results.rep):
            process = subprocess.Popen([popen_string], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            out, err = process.communicate()
            rep_list.append(parse_output(out, rep)[0])
    #
    #         if rep == 0:
    #             header = parse_output(out, rep)[1] + "rep"
    #
    #         if len(err) > 0:
    #             print(err)
    #
        flat_reps = '\n'.join([i for sublist in rep_list for i in sublist])
        output_list.append(flat_reps)
    # print(output_list)
    # print(header)
    print('\n'.join(output_list))


if __name__ == "__main__":
    main()
