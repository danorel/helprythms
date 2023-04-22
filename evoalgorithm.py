from pressure_stats import PressureStats
from noise_stats import NoiseStats
from selection_diff_stats import SelectionDiffStats
from reproduction_stats import ReproductionStats
from run import Run
from functions import *
from constants import *


class EvoAlgorithm:
    def __init__(
        self,
        initial_population: Population,
        selection_function,
        fitness_function,
        optimal,
    ):
        self.population: Population = initial_population
        self.selection_function = selection_function
        self.iteration = 0
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.best = self.population.genotypes_list[0]
        self.pressure_stats.num_of_best.append(
            self.population.genotypes_list.count(self.best)
        )
        self.pressure_stats.f_best.append(self.population.get_max_fitness())
        self.fitness_function = fitness_function
        self.optimal = optimal

    def run(self, run, folder_name, iterations_to_plot):
        self.iteration = 0
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        stop = G
        convergent = self.population.estimate_convergence()

        while not convergent and self.iteration < stop:
            if run < iterations_to_plot and self.iteration < iterations_to_plot:
                self.population.print_phenotypes_distribution(folder_name, self.selection_function.__class__.__name__, run + 1, self.iteration + 1, self.optimal.fitness)
                self.population.print_genotypes_distribution(folder_name, self.selection_function.__class__.__name__, run + 1, self.iteration + 1, self.fitness_function, self.fitness_function.get_genotype_value(self.optimal.code))
            keys_before_selection = self.population.get_keys_list()
            best_genotype = (
                self.population.genotypes_list[0]
                if run < 5 or self.population.p_m == 0
                else self.population.get_best_genotype()
            )
            f = avg_fitness_list[self.iteration]

            self.population = self.selection_function.select(self.population)

            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(
                keys_after_selection
            )

            self.population.crossover(self.fitness_function)
            self.population.mutate(self.fitness_function)

            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            fs = self.population.get_mean_fitness()
            avg_fitness_list.append(fs)
            self.selection_diff_stats.s_list.append(fs - f)
            num_of_best = self.population.get_chromosomes_copies_count(best_genotype)
            self.reproduction_stats.rr_list.append(
                1 - (len(not_selected_chromosomes) / N)
            )
            self.reproduction_stats.best_rr_list.append(
                num_of_best / len(self.population.chromosomes)
            )
            self.pressure_stats.intensities.append(
                PressureStats.calculate_intensity(
                    self.population.get_mean_fitness(), f, f_std
                )
            )
            self.pressure_stats.f_best.append(self.population.get_max_fitness())
            self.pressure_stats.num_of_best.append(num_of_best)
            self.iteration += 1
            self.pressure_stats.grs.append(
                PressureStats.calculate_growth_rate(
                    self.pressure_stats.num_of_best[self.iteration],
                    self.pressure_stats.num_of_best[self.iteration - 1],
                    self.pressure_stats.f_best[self.iteration],
                    self.pressure_stats.f_best[self.iteration - 1],
                )
            )
            if num_of_best >= N / 2 and self.pressure_stats.grl is None:
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]
            convergent = self.population.estimate_convergence()

        if convergent:
            self.pressure_stats.NI = self.iteration

        if run < iterations_to_plot:
            self.population.print_phenotypes_distribution(folder_name, self.selection_function.__class__.__name__, run + 1, self.iteration, self.optimal.fitness)
            self.population.print_genotypes_distribution(folder_name, self.selection_function.__class__.__name__, run + 1, self.iteration + 1, self.fitness_function, self.fitness_function.get_genotype_value(self.optimal.code))

        self.pressure_stats.takeover_time = self.iteration
        self.pressure_stats.f_found = self.population.get_max_fitness()
        self.pressure_stats.f_avg = self.population.get_mean_fitness()
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()
        is_successful = self.check_success() if convergent else False
        return Run(
            avg_fitness_list,
            std_fitness_list,
            self.pressure_stats,
            self.reproduction_stats,
            self.selection_diff_stats,
            None,
            is_successful,
        )

    def check_success(self):
        ff_name = self.fitness_function.__class__.__name__
        if ff_name == "FH" or ff_name == "FHD":
            optimal_chromosome = list(self.optimal.code)
            optimal_chromosomes = self.population.get_chromosomes_copies_count(
                optimal_chromosome
            )
            return optimal_chromosomes == N
        else:
            success_chromosomes = [
                self.fitness_function.check_chromosome_success(p)
                for p in self.population.chromosomes
            ]
            return any(success_chromosomes)

    @staticmethod
    def calculate_noise(sf):
        pop = Fconst().generate_population(N, 100, 0, 0)
        population = Population(pop.chromosomes.copy(), pop.p_m, pop.c_m)
        iteration = 0
        stop = 1000 if "Disruptive" in sf.__class__.__name__ else G

        while not population.estimate_convergence() and iteration < stop:
            population = sf.select(population)
            iteration += 1

        ns = NoiseStats()

        if population.estimate_convergence():
            ns.NI = iteration
            ns.conv_to = population.chromosomes[0].code[0]

        return ns
