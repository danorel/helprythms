import time

from tqdm import tqdm

from multiprocessing import Pool
from constants import ITERATIONS_TO_REPORT, MAX_RUNS, env
from functions import *
from rws import RankExponentialRWS
from sus import RankExponentialSUS
from plots import *
from program import main
from excel import save_avg_to_excel
from runs_stats import RunsStats
from excel import save_to_excel


selection_methods = [
    RankExponentialSUS(c=0.9801),
    RankExponentialSUS(c=0.95099005),
    RankExponentialSUS(c=0.941480149),
    RankExponentialSUS(c=0.904382075),

    RankExponentialRWS(c=0.9801),
    RankExponentialRWS(c=0.95099005),
    RankExponentialRWS(c=0.941480149),
    RankExponentialRWS(c=0.904382075),
]

pm_b = 0.00001
pm_x = 0.0001
pc = 1

fconst_arguments = [
    ("FConst", 0, 0),
    ("FConst_pc", 0, pc),
    ("FConst_pm", pm_b, 0),
    ("FConst_pmpc", pm_b, pc),
]
fconst_fitness_config = (FConst(), N, 100)

fhd_arguments = [
    ("FHD", 0, 0),
    ("FHD_pc", 0, pc),
    ("FHD_pm", pm_b, 0),
    ("FHD_pmpc", pm_b, pc),
]
fhd_fitness_config = (FHD(100), N, 100)

fx2_arguments = [
    ("Fx2", 0, 0),
    ("Fx2_pm", pm_x, 0),
    ("Fx2_pc", 0, pc),
    ("Fx2_pmpc", pm_x, pc),
]
fx2_fitness_config = (Fx2(0, 10.23), N, 10)

f5122subx2_arguments = [
    ("512subx2", 0, 0),
    ("512subx2_pm", pm_x, 0),
    ("512subx2_pc", 0, pc),
    ("512subx2_pmpc", pm_x, pc),
]
f5122subx2_fitness_config = (F5122subx2(-5.11, 5.12), N, 10)

test_arguments = [
    [("FConst", 0, 0)],
    [("Fx2_pmpc", pm_x, pc)],
    [("512subx2_pmpc", pm_x, pc)],
    [("FHD_pmpc", pm_b, pc)],
]
test_fitness_configs = [
    (FConst(), N, 100),
    (Fx2(0, 10.23), N, 10),
    (F5122subx2(-5.11, 5.12), N, 10),
    (FHD(100), N, 100)
]

release_arguments = [
    fhd_arguments,
    fx2_arguments,
    f5122subx2_arguments,
    fconst_arguments
]
relase_fitness_configs = [
    fhd_fitness_config,
    fx2_fitness_config,
    f5122subx2_fitness_config,
    fconst_arguments
]

def run_functions(fitness_config, arguments):
    runs_stats = {}

    fitness_function, *population_arguments = fitness_config

    for argument in arguments:
        file_name, *_ = argument
        runs_stats[file_name] = {}
        for selection_method in selection_methods:
            sf_name = repr(selection_method)
            runs_stats[file_name][sf_name] = RunsStats()

    for run in tqdm(range(MAX_RUNS)):
        initial_population = fitness_function.generate_population(*population_arguments)
        for argument in arguments:
            file_name, *rest_argument = argument

            for selection_method in selection_methods:
                sf_name = repr(selection_method)

                run_stats = main(run, fitness_function, initial_population, selection_method, file_name, *rest_argument)
                runs_stats[file_name][sf_name].runs.append(run_stats)

                if run <= ITERATIONS_TO_REPORT:
                    print(f"{file_name} for {sf_name} per {run} run: saving plots...")
                    save_run_plots(file_name, sf_name, run_stats, run)

            if run == ITERATIONS_TO_REPORT - 1:
                print(f"{file_name}, {run} run: saving reports...")
                sf_run_dictionary = runs_stats[file_name]
                for selection_method in selection_methods:
                    sf_name = repr(selection_method)
                    sf_run_stats = runs_stats[file_name][sf_name]
                    sf_run_stats.calculate()
                save_to_excel(sf_run_dictionary, file_name, file_name.startswith("FConst"))
    
    for argument in arguments:
        file_name, *_ = argument
        for selection_method in selection_methods:
            sf_name = repr(selection_method)
            runs_stats[file_name][sf_name].calculate()

    return runs_stats


if __name__ == "__main__":
    p_start = time.time()

    fitness_configs = test_fitness_configs if env == "test" else relase_fitness_configs 
    arguments = test_arguments if env == "test" else release_arguments
    properties = [(fitness_config, argument) for fitness_config, argument in zip(fitness_configs, arguments)]

    with Pool(6) as pool:
        runs_list = pool.starmap(run_functions, properties)
        save_avg_to_excel(runs_list)

    p_end = time.time()
    print("Program calculation (in sec.): " + str((p_end - p_start)))
