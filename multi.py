import time
from multiprocessing import Pool
from constants import fh_pm, fhd_pm, fx2_pm, env
from functions import *
from rws import RankExponentialRWS
from sus import RankExponentialSUS
from plots import *
from program import main, main_noise
from excel import save_avg_to_excel


release_sm = [RankExponentialSUS, RankExponentialRWS]
testing_sm = [RankExponentialSUS, RankExponentialRWS]
selection_methods = testing_sm if env == "test" else release_sm
release_functions = [
    (FH(), selection_methods, "FH", N, 100, 0),
    (FH(), selection_methods, "FH_pm", N, 100, fh_pm),
    (FHD(100), selection_methods, "FHD_100", N, 100, 0),
    (FHD(100), selection_methods, "FHD_100_pm", N, 100, fhd_pm),
    (Fx2(0, 10.23), selection_methods, "Fx2", N, 10, 0),
    (Fx2(0, 10.23), selection_methods, "Fx2_pm", N, 10, fx2_pm),
    (F5122subx2(-5.11, 5.12), selection_methods, "5_12_sub_X2", N, 10, 0),
    (F5122subx2(-5.11, 5.12), selection_methods, "5_12_sub_X2_pm", N, 10, fx2_pm),
    (Fecx(0, 10.23, 0.25), selection_methods, "Fx", N, 10, 0),
    (Fecx(0, 10.23, 1), selection_methods, "Fx", N, 10, 0),
    (Fecx(0, 10.23, 2), selection_methods, "Fx", N, 10, 0),
]
test_functions = [
    (FH(), selection_methods, "FH_pm", N, 100, fh_pm),
    (Fecx(0, 10.23, 1), selection_methods, "Fecx_pm", N, 10, fx2_pm),
    (Fx2(0, 10.23), selection_methods, "Fx2_pm", N, 10, fx2_pm),
]
functions = test_functions if env == "test" else release_functions


if __name__ == "__main__":
    p_start = time.time()

    func_runs = {}
    noise_runs = {}

    with Pool(12) as p:
        for file_name, run in p.starmap(main, functions):
            func_runs[file_name] = run

        noise_runs["FConst"] = main_noise(selection_methods)

        save_avg_to_excel(func_runs, noise_runs)

    p_end = time.time()
    print("Program calculation (in sec.): " + str((p_end - p_start)))
