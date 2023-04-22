import random

from constants import C
from population import Population


class RankExponentialRWS:
    def exponential_rws(self, population: Population):
        N = len(population.fitness_list)

        ranks = list(map(lambda index: N - index, range(0, N)))
        probabilities = list(map(lambda rank: self.scale(N, rank), ranks))

        if sum(probabilities) == 0:
            return population

        population.update_rws(probabilities)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        random.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.exponential_rws(population)

    def scale(self, size: int, rank: int):
        return ((C - 1) / (pow(C, size) - 1)) * pow(C, size - rank)

    def sort(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda chromosome: chromosome.fitness, reverse=True)
