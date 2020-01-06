from itertools import product
from dispatcher import create_params

m = create_params("m=", "1e-5", "1e-4", "1e-3", "1e-2")
mu = create_params("mu=", "1e-6", "1e-5", "1e-4")
r = create_params("r=", "1e-6", "1e-7", "1e-8")
sigsqr = create_params("sigsqr=", "5", "2", "25")

params_list = [x for x in product(m, mu, r, sigsqr)]

for perm in params_list:
    print(perm)
