env = "test"

# Config: amount of evolutionary algorithms / iterations to probe and report.
MAX_RUNS = 2 if env == "test" else 100
ITERATIONS_TO_REPORT = 3 if env == "test" else 5

# Genotype: amount of chromosomes in population / codec.
N = 100
ENCODING = "binary" # "binary" or "gray"

# Termination condition: maximum amount of iterations.
G = 100 if env == "test" else 10000000

# Convergence condition:
SIGMA = DELTA = 0.01
