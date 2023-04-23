import time

from tqdm import tqdm

from multiprocessing import Pool
from constants import P_M, P_C, MAX_RUNS, env
from functions import *
from rws import RankExponentialRWS
from sus import RankExponentialSUS
from plots import *
from program import main, main_noise
from excel import save_avg_to_excel
from runs_stats import RunsStats


selection_methods = [RankExponentialSUS(), RankExponentialRWS()]

fhd_arguments = [
    ("FHD", 0, 0),
    ("FHD_pc", 0, P_C),
    ("FHD_pm", 0.00001, 0),
    ("FHD_pmpc", 0.00001, P_C),
]
fhd_fitness_config = (FHD(100), N, 100)

fx2_arguments = [
    ("Fx2", 0, 0),
    ("Fx2_pm", 0.0001, 0),
    ("Fx2_pc", 0, P_C),
    ("Fx2_pmpc", 0.0001, P_C),
]
fx2_fitness_config = (Fx2(0, 10.23), N, 10)

f5122subx2_arguments = [
    ("512subx2", 0, 0),
    ("512subx2_pm", 0.0001, 0),
    ("512subx2_pc", 0, P_C),
    ("512subx2_pmpc", 0.0001, P_C),
]
f5122subx2_fitness_config = (F5122subx2(-5.11, 5.12), N, 10)

test_arguments = [
    [("Fx2_pmpc", P_M, P_C)],
    [("512subx2_pmpc", P_M, P_C)],
    [("FHD_pmpc", P_M, P_C)]
]
test_fitness_configs = [
    (Fx2(0, 10.23), N, 10),
    (F5122subx2(-5.11, 5.12), N, 10),
    (FHD(100), N, 100)
]

release_arguments = [
    fhd_arguments,
    fx2_arguments,
    f5122subx2_arguments
]
relase_fitness_configs = [
    fhd_fitness_config,
    fx2_fitness_config,
    f5122subx2_fitness_config
]

def run_functions(fitness_config, arguments):
    runs_stats = {}

    fitness_function, *population_arguments = fitness_config

    for argument in arguments:
        file_name, *_ = argument
        runs_stats[file_name] = {}
        for selection_method in selection_methods:
            runs_stats[file_name][selection_method.__class__.__name__] = RunsStats()

    for run in tqdm(range(MAX_RUNS)):
        initial_population = fitness_function.generate_population(*population_arguments)
        for argument in arguments:
            file_name, *rest_argument = argument
            for selection_method in selection_methods:
                run_stats = main(run, fitness_function, initial_population, selection_method, file_name, *rest_argument)
                runs_stats[file_name][selection_method.__class__.__name__].runs.append(run_stats)

    for argument in arguments:
        file_name, *_ = argument
        for selection_method in selection_methods:
            runs_stats[file_name][selection_method.__class__.__name__].calculate()

    return runs_stats


if __name__ == "__main__":
    p_start = time.time()

    fitness_configs = test_fitness_configs if env == "test" else relase_fitness_configs 
    arguments = test_arguments if env == "test" else release_arguments

    properties = [(fitness_config, argument) for fitness_config, argument in zip(fitness_configs, arguments)]

    with Pool(6) as p:
        func_stats = p.starmap(run_functions, properties)
        noise_stats = {}
        noise_stats["FConst"] = main_noise(selection_methods)
        save_avg_to_excel(func_stats, noise_stats)

    p_end = time.time()
    print("Program calculation (in sec.): " + str((p_end - p_start)))
