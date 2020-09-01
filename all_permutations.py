from itertools import product
from dispatcher import create_params

m = create_params("m=", "0.1" ,"5e-2", "1e-2", "5e-3", "1e-3", "5e-4", "1e-4", "1e-5")
mu = create_params("mu=", "1e-6")
r = create_params("r=", "1e-6")
sigsqr = create_params("sigsqr=", "2", "25")
n = create_params("n=", "5000", "1000", "500")

params_list = [x for x in product(m, mu, r, sigsqr, n)]

for perm in params_list:
    print(' '.join([f'--{opt}' for opt in perm]))
