from __future__ import print_function
import subprocess
import argparse
import os
import re
import random

from itertools import product
from time import gmtime, strftime


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


def find_dataset(output_list, identifier):
    """
    Finds specified data set with the search of beginning strings used to delimit specific types of output.

    Parameters
    ----------
    output_list: list
        A list of strings containing the body of data where each relevant string begins with a keyword to denote that it
        belongs to a certain data set.
    identifier: str
        The identifying string for the specific data set. Each line in the data set should begin with this string.

    Returns
    -------
    found_output: list
        A list of the relevant data set rows with the `identifier` string removed from the beginning.

    """
    alt_identifier = '"' + identifier
    found_output = [re.sub('"?{} '.format(identifier), '', i) for i in output_list if i.startswith(identifier) or
                    i.startswith(alt_identifier)]
    return found_output


def parse_output(output, identifier, rep):
    """
    Parses the data of the stdout from the slim script.

    Parameters
    ----------
    output: str
        The stdout from the slim script.
    identifier: str
        Identifying string of the given data set. See documentation for `find_dataset`.
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
    body = find_dataset(body, identifier)
    header = body[0]
    body = remove_all(body, header)
    body = [i + " {}".format(rep) for i in body]
    return body, header, meta


def parse_fullgenome(meta):
    """
    Parses the meta data to collect the full genome.

    Parameters
    ----------
    meta: str
        The meta data output from `parse_output` or the third item of tuple of the `parse_output` function.

    Returns
    -------
    out_list: list
        Returns a list where each base position is contained within its own list. The corresponding items within the
        list of lists are the genome, base and gene.
    """
    meta_list = meta.split('\n')
    search_list = [re.search('initializeGenomicElement\((g\d+, \d*, \d*)\);', i) for i in meta_list]
    matches = [i.group(1) for i in search_list if i is not None]
    matches_labels = ["{}, {}".format(i, matches.index(i)) for i in matches]
    split_list = [i.split(', ') for i in matches_labels]

    gene_bases = []
    for i in split_list:
        gene_bases.append(list(range(int(i[1]), int(i[2]) + 1)))

    out_list = []
    for i, bases in enumerate(gene_bases):
        for b in bases:
            out_list.append([split_list[i][0], b, split_list[i][3]])

    return out_list


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


def trigger_options(opt_on, param_str, *opts):
    """
    This is wrapper function around `create_params()` that triggers whether or not one or more options will
    be specified per parameter.

    Parameters
    ----------
    opt_on: bool
        An option that specifies whether or not the parameter should be a single call or multiple calls.
    param_str: str
        The parameter options string that takes on the form "<opt>=".
    opts: str
        The parameter option values. If `opton` is `False` then only the first option specified will be considered.

    Returns
    -------
    list
        A list of strings explicitly specifying the parameter to be run within the slim script.
    """
    if not opt_on:
        call = create_params(param_str, opts[0])
    else:
        call = create_params(param_str, *opts)
    return call


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


def convert_popen_to_data(params_list, popen_scaffold, output_every, output_dir, datasets, num_reps):
    """
    Turns popen output into workable data.

    Parameters
    ----------
    params_list: list
        A list of parameters to have set for the simulation.
    popen_scaffold: str
        A string of the scaffolding provided to run the slim command with the given parameters of the params_list.
    output_every: str
        A parameter setting specifying when output is written.
    output_dir
        The directory to save the output to.
    datasets
        The name of the dataset that is being written. This corresponds to different levels of aggregation of output.
    num_reps
        The number of replicates to run per simulation.
    """
    # dictionary to map code to dataset name
    datasets_dict = {
        # 'phenotypes': 'p33',
        'mutations': 'm39',
        # 'genome1': 'g36',
        # 'genome2': 'g30'
    }

    for ind, params in enumerate(params_list):

        # create the string command to be run
        popen_string = popen_scaffold.format(params[0], params[1], params[2], params[3], params[4], params[5], output_every)

        # file and dataset rep dictionary calls
        file_name_dict = dict()
        rep_list_dict = dict()
        for d in datasets:
            file_name_dict[d] = create_file_name(params, d)
            rep_list_dict[d] = []

        # run the command for n replicates
        meta_dict = dict()
        for rep in range(num_reps):
            process = subprocess.Popen([popen_string], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            out, err = process.communicate()

            header_dict = dict()

            for d in datasets:
                body, header, meta = parse_output(out, datasets_dict[d], rep)
                rep_list_dict[d].append(body)

                header_dict[d] = header + "rep"

                if not bool(meta_dict):
                    meta_dict['meta'] = parse_fullgenome(meta)
                    meta_file = create_file_name(params, "fullgenome")
                    with open(output_dir + meta_file, "w") as f:
                        f.write("genome position gene\n")
                        f.write('\n'.join([' '.join(list(map(lambda x: str(x), i))) for i in meta_dict['meta']]))

            flat_reps_dict = {}
            for d in datasets:
                flat_reps_dict[d] = '\n'.join([i for sublist in rep_list_dict[d] for i in sublist])
                with open(output_dir + file_name_dict[d], "w") as f:
                    f.write(header_dict[d] + "\n")
                    f.write(flat_reps_dict[d])

            if len(err) > 0:
                print(err)


def main():
    """
    Provides a wrapper around the slim command and runs a file for simulating local adaptation called
    `local_adaptation.slim`. This file can be run from the command line with the falling named arguments:
    --rep : The number of replicates you want to run.
    --m : An option to run a series of migration rates.
    --mu : An option to run a series of mutation rates.
    --r : An option to run a series of recombination rates.
    --sigsqr: An option to run a series of fitness widths.
    --concat: An option to concatenate all the results into one print statement.

    Returns
    -------
        A call to the slim command running the script `local_adaptation.slim`
    """
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
    parser.add_argument('--n', action='store', type=int, default=1000)
    parser.add_argument('--datasets', nargs='+', default=['mutations'])
    results = parser.parse_args()

    m = create_params("m=", results.m)
    mu = create_params("mu=", results.mu)
    numpos = create_params("numpos=", results.numpos)
    r = create_params("r=", results.r)
    sigsqr = create_params("sigsqr=", results.sigsqr)
    n = create_params("N=", results.n)
    

    params_list = [x for x in product(m, mu, r, sigsqr, n, numpos)]
    popen_scaffold = 'slim -d "{}" -d "{}" -d "{}" -d "{}" -d "{}" -d "{}" -d "{}" local_adaptation.slim'

    output_every = "outputEvery=2500"

    convert_popen_to_data(params_list, popen_scaffold, output_every, output_dir, results.datasets, results.rep)


if __name__ == "__main__":
    main()
