import os

import random
import numpy as np
import matplotlib.pyplot as plt

from chromosome import Chromosome
from constants import N, ENCODING


class Population:
    def __init__(self, chromosomes: list[Chromosome]):
        self.chromosomes = chromosomes
        self.phenotypes_list = np.fromiter(
            map(lambda chromosome: chromosome.fitness, self.chromosomes),
            dtype=np.float64,
        )
        self.genotypes_list = list(
            map(lambda chromosome: list(chromosome.code), self.chromosomes)
        )

    def print_ones_distribution(
        self, fitness_function_name, selection_name, run, iteration, fitness_function
    ):
        dir_path = f"Function/{N}/{fitness_function_name}/{selection_name}/{ENCODING}/{run}/ones"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
 
        counts, bins = np.histogram([genotype_list.count(1) for genotype_list in self.genotypes_list])
        width = 1

        f = plt.figure()
        plt.hist(bins[:-1], 10, weights=counts, width=width)
        plt.xlabel("Number of ones")
        plt.ylabel("Number of individual")
        plt.title("Counts (ones)")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)


    def print_phenotypes_distribution(
        self, fitness_function_name, selection_name, run, iteration, fitness_function
    ):
        dir_path = f"Function/{N}/{fitness_function_name}/{selection_name}/{ENCODING}/{run}/phenotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        counts, bins = np.histogram(self.phenotypes_list)
        width = fitness_function.extremum_y / 10

        f = plt.figure()
        plt.hist(bins[:-1], 10, weights=counts, width=width)
        plt.xlim(0, fitness_function.extremum_y * 1.1)
        plt.xlabel("Health")
        plt.ylabel("Number of individuals")
        plt.title("Phenotypes (fitness)")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def print_genotypes_distribution(
        self, fitness_function_name, selection_name, run, iteration, fitness_function
    ):
        dir_path = f"Function/{N}/{fitness_function_name}/{selection_name}/{ENCODING}/{run}/genotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        counts, bins = np.histogram([fitness_function.get_genotype_value(code) for code in self.genotypes_list])
        width = (fitness_function.b - fitness_function.a) / 10 

        f = plt.figure()
        plt.hist(bins[:-1], 10, weights=counts, width=width)
        plt.xlabel("X")
        plt.ylabel("Number of individuals")
        plt.title("Genotype (x)")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def estimate_convergence(self, p_m):
        if p_m == 0:
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

    def crossover(self, fitness_function, p_c):
        if p_c == 0:
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

    def mutate(self, fitness_function, p_m):
        if p_m == 0:
            return
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < p_m:
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
        best_index = self.phenotypes_list.argmax()
        best_genotype = self.genotypes_list[best_index]
        return best_genotype

    def get_keys_list(self):
        return list(map(lambda chromosome: chromosome.key, self.chromosomes))

    def get_chromosomes_copies_count(self, genotype_copy):
        return self.genotypes_list.count(genotype_copy)

    def update(self):
        self.phenotypes_list = np.fromiter(
            map(lambda chromosome: chromosome.fitness, self.chromosomes),
            dtype=np.float64,
        )
        self.genotypes_list = list(
            map(lambda chromosome: list(chromosome.code), self.chromosomes)
        )

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
        return Population(self.chromosomes.copy())
