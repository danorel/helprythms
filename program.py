import time

from copy import copy
from tqdm import tqdm

from constants import MAX_RUNS, ITERATIONS_TO_REPORT
from run import Run
from runs_stats import RunsStats
from functions import Fconst 
from evoalgorithm import EvoAlgorithm
from excel import save_to_excel, save_noise_to_excel
from plots import *


def save_run_plots(ff_name, sf_name, run, iteration):
    save_line_plot(
        ff_name,
        sf_name,
        run.avg_fitness_list,
        "f_avg" + str(iteration + 1),
        "f avg",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.std_fitness_list,
        "f_std" + str(iteration + 1),
        "f std",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.pressure_stats.intensities,
        "intensity" + str(iteration + 1),
        "intensity",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.selection_diff_stats.s_list,
        "selection_diff" + str(iteration + 1),
        "selection difference",
        iteration + 1,
    )
    save_lines_plot(
        ff_name,
        sf_name,
        [run.pressure_stats.intensities, run.selection_diff_stats.s_list],
        ["Intensity", "EvoAlgorithm diff"],
        "intensity_and_sel_diff" + str(iteration + 1),
        "Intensity + EvoAlgorithm diff",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.pressure_stats.grs,
        "gr" + str(iteration + 1),
        "growth rate",
        iteration + 1,
    )
    save_lines_plot(
        ff_name,
        sf_name,
        [
            run.reproduction_stats.rr_list,
            [1 - rr for rr in run.reproduction_stats.rr_list],
        ],
        ["Reproduction rate", "Loss of diversity"],
        "repro_rate_and_loss_of_diversity" + str(iteration + 1),
        "Reproduction rate + Loss of diversity",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.reproduction_stats.best_rr_list,
        "best_rr" + str(iteration + 1),
        "best chromosome rate",
        iteration + 1,
    )


def main(
    run: int,
    fitness_function,
    initial_population,
    selection_functions: list,
    file_name,
    *args,
):
    p_start = time.time()
    runs_dict = {}
    ff_name = fitness_function.__class__.__name__

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__] = RunsStats()

    print(f"{file_name}, {run} run: is starting...")

    for selection_function in selection_functions:
        p = copy(initial_population)
        sf_name = selection_function.__name__
        sf = selection_function()
        optimal = fitness_function.get_optimal(*args)
        folder_name = file_name if file_name is not None else ff_name
        current_run = EvoAlgorithm(p, sf, fitness_function, optimal, *args).run(
            run, folder_name
        )
        runs_dict[sf_name].runs.append(current_run)
        if run < ITERATIONS_TO_REPORT:
            save_run_plots(folder_name, sf_name, current_run, run)

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__].calculate()

    if run < ITERATIONS_TO_REPORT:
        print(f"{file_name}, {run} run: saving reports...")
        save_to_excel(runs_dict, file_name if file_name is not None else ff_name)

    p_end = time.time()
    print(f"{file_name}, {run} run: finished in {str(p_end - p_start)} seconds...")

    return file_name, runs_dict


def main_noise(selection_functions: list, *args):
    p_start = time.time()
    runs_dict = {}

    fitness_function = Fconst()
    file_name = fitness_function.__class__.__name__

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__] = RunsStats()

    print(f"{file_name}: is starting...")
    for _ in tqdm(range(MAX_RUNS)):
        initial_population = fitness_function.generate_population(N, 100)
        for selection_function in selection_functions:
            p = copy(initial_population) 
            sf_name = selection_function.__name__
            sf = selection_function()
            ns = EvoAlgorithm.calculate_noise(p, fitness_function, sf, *args)
            runs_dict[sf_name].runs.append(Run(noise_stats=ns))

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__].calculate_noise_stats()

    print(f"{file_name}: saving reports...")
    save_noise_to_excel(runs_dict, file_name)

    p_end = time.time()
    print(f"{file_name}: finished in {str(p_end - p_start)} seconds...")

    return runs_dict
