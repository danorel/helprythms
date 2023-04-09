import time
from multiprocessing import Pool
from constants import P_M, P_C, env
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
    (FH(), selection_methods, "FH", N, 100, 0, 0),
    (FH(), selection_methods, "FH_pm", N, 100, P_M, 0),
    (FH(), selection_methods, "FH_pc", N, 100, 0, P_C),
    (FH(), selection_methods, "FH_pmpc", N, 100, P_M, P_C),
    (FHD(100), selection_methods, "FHD", N, 100, 0, 0),
    (FHD(100), selection_methods, "FHD_pm", N, 100, P_M, 0),
    (FHD(100), selection_methods, "FHD_pc", N, 100, 0, P_C),
    (FHD(100), selection_methods, "FHD_pmpc", N, 100, P_M, P_C),
    (Fx2(0, 10.23), selection_methods, "Fx2", N, 10, 0, 0),
    (Fx2(0, 10.23), selection_methods, "Fx2_pm", N, 10, P_M, 0),
    (Fx2(0, 10.23), selection_methods, "Fx2_pc", N, 10, 0, P_C),
    (Fx2(0, 10.23), selection_methods, "Fx2_pmpc", N, 10, P_M, P_C),
    (F5122subx2(-5.11, 5.12), selection_methods, "512subx2", N, 10, 0, 0),
    (F5122subx2(-5.11, 5.12), selection_methods, "512subx2_pm", N, 10, P_M, 0),
    (F5122subx2(-5.11, 5.12), selection_methods, "512subx2_pc", N, 10, 0, P_C),
    (F5122subx2(-5.11, 5.12), selection_methods, "512subx2_pmpc", N, 10, P_M, P_C),
    (Fecx(0, 10.23, 0.25), selection_methods, "Fec025x", N, 10, 0, 0),
    (Fecx(0, 10.23, 0.25), selection_methods, "Fec025x_pm", N, 10, P_M, 0),
    (Fecx(0, 10.23, 0.25), selection_methods, "Fec025x_pc", N, 10, 0, P_C),
    (Fecx(0, 10.23, 0.25), selection_methods, "Fec025x_pmpc", N, 10, P_M, P_C),
    (Fecx(0, 10.23, 1), selection_methods, "Fec1x", N, 10, 0, 0),
    (Fecx(0, 10.23, 1), selection_methods, "Fec1x_pm", N, 10, P_M, 0),
    (Fecx(0, 10.23, 1), selection_methods, "Fec1x_pc", N, 10, 0, P_C),
    (Fecx(0, 10.23, 1), selection_methods, "Fec1x_pmpc", N, 10, P_M, P_C),
    (Fecx(0, 10.23, 2), selection_methods, "Fec2x", N, 10, 0, 0),
    (Fecx(0, 10.23, 2), selection_methods, "Fec2x_pm", N, 10, P_M, 0),
    (Fecx(0, 10.23, 2), selection_methods, "Fec2x_pc", N, 10, 0, P_C),
    (Fecx(0, 10.23, 2), selection_methods, "Fec2x_pmpc", N, 10, P_M, P_C),
]
test_functions = [
    (FH(), selection_methods, "FH_pm", N, 100, P_M, P_C),
    (Fecx(0, 10.23, 1), selection_methods, "Fecx_pm", N, 10, P_M, P_C),
    (Fx2(0, 10.23), selection_methods, "Fx2_pm", N, 10, P_M, P_C),
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
