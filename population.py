import os

import random
import numpy as np
import matplotlib.pyplot as plt

from chromosome import Chromosome
from constants import N


class Population:
    def __init__(self, chromosomes: list[Chromosome], p_m, c_m):
        self.chromosomes = chromosomes
        self.phenotypes_list = np.fromiter(map(lambda chromosome: chromosome.fitness, self.chromosomes), dtype=np.float64)
        self.genotypes_list = list(map(lambda chromosome: list(chromosome.code), self.chromosomes))
        self.p_m = p_m
        self.c_m = c_m

    def print_phenotypes_distribution(
        self, folder_name, func_name, run, iteration, xAxisMax
    ):
        dir_path = f"Function/{N}/{func_name}/{folder_name}/{run}/phenotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        f = plt.figure()
        plt.ylim(0, len(self.chromosomes) * 1.1)
        plt.xlim(0, xAxisMax * 1.1)
        plt.hist(self.phenotypes_list, 20, width=xAxisMax / 30)
        plt.xlabel("Health")
        plt.ylabel("Num of individual")
        plt.title("Phenotypes (fitness)")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def print_genotypes_distribution(
        self, folder_name, func_name, run, iteration, fitness_func, xAxisMax
    ):
        dir_path = f"Function/{N}/{func_name}/{folder_name}/{run}/genotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        x_list = [fitness_func.get_genotype_value(code) for code in self.genotypes_list]

        if xAxisMax == 0:
            xAxisMax = len(self.genotypes_list[0])

        f = plt.figure()
        plt.ylim(0, len(x_list) * 1.1)
        plt.xlim(0, xAxisMax * 1.1)
        plt.hist(x_list, 15, width=xAxisMax / 20)
        plt.xlabel("X")
        plt.ylabel("Num of individual")
        plt.title("Genotype (x)")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def estimate_convergence(self):
        if self.p_m == 0:
            return self.is_identical
        else:
            return self.is_homogeneous(percentage=99)

    def is_homogeneous(self, percentage: int) -> bool:
        assert percentage < 100, (
            "According to formula: (unique / total) * 100 <= 100 - percentage, "
            "we can't have percentage >= 100!"
        )
        chromosomes = ["".join(map(str, genotype)) for genotype in self.genotypes_list]
        total = len(chromosomes)
        unique = len(set(chromosomes))
        return (unique / total) * 100 <= 100 - percentage

    @property
    def is_identical(self) -> bool:
        genotypes = {"".join(map(str, genotype)) for genotype in self.genotypes_list}
        return len(genotypes) == 1

    def crossover(self, fitness_function):
        if self.c_m == 0:
            return

        next_chromosomes = []

        chromosomes = self.chromosomes.copy()

        def pop_chromosome():
            index = random.randrange(0, len(chromosomes))
            return chromosomes.pop(index)

        next_key = 0

        while len(chromosomes) > 0:
            parent1 = pop_chromosome()
            parent2 = pop_chromosome()

            crossover_point = int(random.random() * len(parent1.code))

            child_code1 = [
                *parent1.code[:crossover_point],
                *parent2.code[crossover_point:],
            ]
            child_chromosome1 = Chromosome(
                child_code1, fitness_function.estimate(child_code1), next_key + 1
            )

            child_code2 = [
                *parent2.code[:crossover_point],
                *parent1.code[crossover_point:],
            ]
            child_chromosome2 = Chromosome(
                child_code2, fitness_function.estimate(child_code2), next_key + 2
            )

            next_chromosomes.append(child_chromosome1)
            next_chromosomes.append(child_chromosome2)

            next_key += 2

        self.update_chromosomes(next_chromosomes)

    def mutate(self, fitness_function):
        if self.p_m == 0:
            return
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < self.p_m:
                    chromosome.code[i] = int(not chromosome.code[i])
                    chromosome.fitness = fitness_function.estimate(chromosome.code)
        self.update()

    def get_mean_fitness(self):
        return self.phenotypes_list.mean()

    def get_max_fitness(self):
        return self.phenotypes_list.max()

    def get_fitness_std(self):
        return self.phenotypes_list.std()

    def get_best_genotype(self):
        max_index = self.phenotypes_list.argmax()
        return self.genotypes_list[max_index]

    def get_keys_list(self):
        return list(map(lambda chromosome: chromosome.key, self.chromosomes))

    def get_chromosomes_copies_count(self, genotype_copy):
        return self.genotypes_list.count(genotype_copy)

    def update(self):
        self.phenotypes_list = np.fromiter(map(lambda chromosome: chromosome.fitness, self.chromosomes), dtype=np.float64)
        self.genotypes_list = list(map(lambda chromosome: list(chromosome.code), self.chromosomes))

    def update_rws(self, probabilities):
        self.chromosomes = [
            np.random.choice(self.chromosomes, p=probabilities)
            for _ in range(0, len(self.chromosomes))
        ]
        self.update()

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()

    def __copy__(self):
        return Population(self.chromosomes.copy(), self.p_m.copy())
