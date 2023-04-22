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


selection_methods = [RankExponentialSUS, RankExponentialRWS]

fhd_arguments = [
    (selection_methods, "FHD", 0, 0),
    (selection_methods, "FHD_pc", 0, P_C),
    (selection_methods, "FHD_pm", 0.00001, 0),
    (selection_methods, "FHD_pmpc", 0.00001, P_C),
]
fhd_fitness_config = (FHD(100), N, 100)

fx2_arguments = [
    (selection_methods, "Fx2", 0, 0),
    (selection_methods, "Fx2_pm", 0.0001, 0),
    (selection_methods, "Fx2_pc", 0, P_C),
    (selection_methods, "Fx2_pmpc", 0.0001, P_C),
]
fx2_fitness_config = (Fx2(0, 10.23), N, 10)

f5122subx2_arguments = [
    (selection_methods, "512subx2", 0, 0),
    (selection_methods, "512subx2_pm", 0.0001, 0),
    (selection_methods, "512subx2_pc", 0, P_C),
    (selection_methods, "512subx2_pmpc", 0.0001, P_C),
]
f5122subx2_fitness_config = (F5122subx2(-5.11, 5.12), N, 10)

test_arguments = [
    [(selection_methods, "Fx2_pm", P_M, P_C)]
]
test_fitness_configs = [
    (Fx2(0, 10.23), N, 10)
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
    file_names = []
    runs_dicts = []

    fitness_function, *population_arguments = fitness_config

    for run in tqdm(range(MAX_RUNS)):
        initial_population = fitness_function.generate_population(*population_arguments)
        for argument in arguments:
            file_name, run_dict = main(run, fitness_function, initial_population, *argument)
            file_names.append(file_name)
            runs_dicts.append(run_dict)

    return file_names, runs_dicts


if __name__ == "__main__":
    p_start = time.time()

    func_runs = {}
    noise_runs = {}

    fitness_configs = test_fitness_configs if env == "test" else relase_fitness_configs 
    arguments = test_arguments if env == "test" else release_arguments

    properties = [(fitness_config, argument) for fitness_config, argument in zip(fitness_configs, arguments)]

    with Pool(6) as p:
        for file_names, runs in p.starmap(run_functions, properties):
            for file_name, run in zip(file_names, runs):
                func_runs[file_name] = run

        noise_runs["FConst"] = main_noise(selection_methods, 0, 0)

        save_avg_to_excel(func_runs, noise_runs)

    p_end = time.time()
    print("Program calculation (in sec.): " + str((p_end - p_start)))
