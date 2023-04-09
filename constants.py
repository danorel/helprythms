env = "test"

# Runs: amount of evolutionary algorithms to probe.
MAX_RUNS = 5 if env == "test" else 100

# Genotype: amount of genes.
N = 100

# Termination condition: maximum amount of iterations.
G = 10000000

# Selection: exponential parameter for Rank selection.
C = 0.9801

# Operators: rate for Dense mutation / rate for Single-point crossover.
P_M = 0
P_C = 0

fh_pm = 5.63605e-06 if N == 1000 else 5.81669e-05
fhd_pm = 5.08066e-06 if N == 1000 else 6.26079e-05
fx2_pm = 1.22e-04 if N == 1000 else 7.97e-04

# Convergence condition:
SIGMA = DELTA = 0.01
