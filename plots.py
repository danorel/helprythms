import os

import matplotlib.pyplot as plt

from constants import N


def save_line_plot(fitness_func_name, func_name, data, file_name, y_label, iteration):
    dir_path = f"Function/{N}/{func_name}/{fitness_func_name}/{str(iteration)}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    x = list(range(1, len(data) + 1))

    plt.bar(x, 100, width=1, data=data, label=func_name)
    plt.ylabel(y_label)
    plt.xlabel("generation")
    plt.legend()
    plt.savefig(f"{dir_path}/{file_name}.png")
    plt.close()


def save_lines_plot(
    fitness_func_name, func_name, data_arr, label_arr, file_name, y_label, iteration
):
    dir_path = f"Function/{N}/{func_name}/{fitness_func_name}/{str(iteration)}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for i in range(0, len(data_arr)):
        data = data_arr[i]
        label = label_arr[i]
        x = list(range(1, len(data) + 1))
        plt.bar(x, 100, width=1, data=data, label=label)

    plt.ylabel(y_label)
    plt.xlabel("generation")
    plt.legend()
    plt.savefig(f"{dir_path}/{file_name}.png")
    plt.close()
