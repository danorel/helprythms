import os
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from statistics import mean

from constants import N
from chromosome import Chromosome


class Population:
    def __init__(self, chromosomes: list[Chromosome], p_m, c_m):
        self.chromosomes = chromosomes
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]
        self.p_m = p_m
        self.c_m = c_m

    def print_phenotypes_distribution(self, folder_name, func_name, run, iteration):
        path = (
            "Histogram"
            + "/"
            + str(N)
            + "/"
            + func_name
            + "/"
            + folder_name
            + "/"
            + str(run)
            + "/"
            + "phenotypes"
        )

        if not os.path.exists(path):
            os.makedirs(path)

        sns.displot(self.fitness_list)
        plt.savefig(path + "/" + str(iteration) + ".png")
        plt.close()

    def print_genotypes_distribution(
        self, folder_name, func_name, run, iteration, fitness_func
    ):
        path = (
            "Histogram"
            + "/"
            + str(N)
            + "/"
            + func_name
            + "/"
            + folder_name
            + "/"
            + str(run)
            + "/"
            + "genotypes"
        )

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.get_genotype_value(code) for code in self.genotypes_list]
        sns.displot(x_list)
        plt.savefig(path + "/" + str(iteration) + ".png")
        plt.close()

    def estimate_convergence(self):
        if self.p_m == 0:
            return self.is_homogeneous(percentage=100)
        else:
            return self.is_homogeneous(percentage=99)

    def is_homogeneous(self, percentage: float):
        chromosomes = ["".join(map(str, genotype)) for genotype in self.genotypes_list]
        total = len(chromosomes)
        unique = len(set(chromosomes))
        return (unique / total) * 100 <= 100 - percentage 

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

            child_code1 = parent1.code[:crossover_point] + parent2.code[crossover_point:]
            child_chromosome1 = Chromosome(
                child_code1,
                fitness_function.estimate(child_code1),
                next_key + 1
            )
            
            child_code2 = parent2.code[:crossover_point] + parent1.code[crossover_point:]
            child_chromosome2 = Chromosome(
                child_code2,
                fitness_function.estimate(child_code2),
                next_key + 2
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
        return mean(self.fitness_list)

    def get_max_fitness(self):
        return max(self.fitness_list)

    def get_best_genotype(self):
        max_value = self.get_max_fitness()
        best_list = list(
            filter(
                lambda x: self.fitness_list[x] == max_value,
                range(len(self.fitness_list)),
            )
        )
        return self.genotypes_list[best_list[0]]

    def get_fitness_std(self):
        return np.std(self.fitness_list)

    def get_keys_list(self):
        return list([chromosome.key for chromosome in self.chromosomes])

    def get_chromosomes_copies_count(self, genotype_copy):
        genotype_copy = ''.join(map(str, genotype_copy))
        genotypes = [''.join(map(str, genotype)) for genotype in self.genotypes_list]
        return genotypes.count(genotype_copy)

    def update(self):
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]

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
