import time

from copy import copy

from evoalgorithm import EvoAlgorithm

def main(
    run: int,
    fitness_function,
    initial_population,
    selection_method,
    file_name,
    *args,
):
    print(f"{file_name}, {run} run: is starting...")
    p_start = time.time()
    p = copy(initial_population)
    ff_name = fitness_function.__class__.__name__
    optimal = fitness_function.get_optimal(*args)
    folder_name = file_name if file_name is not None else ff_name
    current_run = EvoAlgorithm(p, selection_method, fitness_function, optimal, *args).run(
        run, folder_name
    )
    p_end = time.time()
    print(f"{file_name}, {run} run: finished in {str(p_end - p_start)} seconds...")
    return current_run
