env = "release"

# Config: amount of evolutionary algorithms / iterations to probe and report.
MAX_RUNS = 5 if env == "test" else 100
ITERATIONS_TO_REPORT = 1 if env == "test" else 5

# Genotype: amount of chromosomes in population / codec.
N = 100
ENCODING = "binary" # "binary" or "gray"

# Termination condition: maximum amount of iterations.
G = 100 if env == "test" else 10000000

# Selection: exponential parameter for Rank selection.
C = 0.9801

# Operators: rate for Dense mutation / rate for Single-point crossover.
P_M = 0.00001 if N == 100 else 0.0005  # depends on other criterias
P_C = 1  # 0 or 1

# Convergence condition:
SIGMA = DELTA = 0.01
