import functools
import random

from numpy import random

from constants import C
from population import Population


def basic_sus(population: Population, total_fitness, fitness_scale: []):
    mating_pool = []
    number_of_parents = len(population.chromosomes)
    fitness_step = total_fitness / number_of_parents
    random_offset = random.uniform(0, fitness_step)
    current_fitness_pointer = random_offset
    last_fitness_scale_position = 0

    for _ in range(len(population.chromosomes)):
        for fitness_scale_position in range(
            last_fitness_scale_position, len(fitness_scale)
        ):
            if fitness_scale[fitness_scale_position] >= current_fitness_pointer:
                mating_pool.append(population.chromosomes[fitness_scale_position])
                last_fitness_scale_position = fitness_scale_position
                break
        current_fitness_pointer += fitness_step

    return mating_pool


class RankExponentialSUS:
    def __init__(self):
        self.c = 0.95

    def exponential_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        size = len(population.chromosomes)

        for index in range(size):
            individual_scaled_fitness = self.scale(size, index)
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                fitness_scale.append(
                    individual_scaled_fitness + fitness_scale[index - 1]
                )

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.exponential_sus(population)

    def scale(self, size: int, rank: int):
        return ((C - 1) / (pow(C, size) - 1)) * pow(C, size - rank)

    def shuffle(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda _: random.random())

    def sort(self, chromosomes):
        return sorted(chromosomes.copy(), key=functools.cmp_to_key(self.compare))

    def compare(self, chromosome1, chromosome2):
        if chromosome1.fitness < chromosome2.fitness:
            return -1
        elif chromosome1.fitness > chromosome2.fitness:
            return 1
        else:
            return 0
