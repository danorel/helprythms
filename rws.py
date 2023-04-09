import functools
import random

from constants import C
from population import Population


class RankExponentialRWS:
    def exponential_rws(self, population: Population):
        size = len(population.fitness_list)

        probabilities = list(
            map(lambda index: self.scale(size, index), range(1, size + 1))
        )

        if sum(probabilities) == 0:
            return population

        population.update_rws(probabilities)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.exponential_rws(population)

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
