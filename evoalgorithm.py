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
        p_m: float | None,
        p_c: float | None,
    ):
        self.population: Population = initial_population
        self.selection_function = selection_function
        self.iteration = 0
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.best = self.population.get_best_genotype()
        self.pressure_stats.num_of_best.append(
            self.population.genotypes_list.count(self.best)
        )
        self.pressure_stats.f_best.append(self.population.get_max_fitness())
        self.fitness_function = fitness_function
        self.optimal = optimal
        self.p_m = p_m
        self.p_c = p_c

    def run(self, run, folder_name):
        self.iteration = 0
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        stop = G
        convergent = self.population.estimate_convergence(self.p_m)

        while not convergent and self.iteration < stop:
            if run < ITERATIONS_TO_REPORT and self.iteration < ITERATIONS_TO_REPORT:
                self.population.print_ones_distribution(
                    folder_name,
                    self.selection_function.__class__.__name__,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function
                )
                self.population.print_phenotypes_distribution(
                    folder_name,
                    self.selection_function.__class__.__name__,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function,
                )
                if self.fitness_function.__class__.__name__ != "FHD": 
                    self.population.print_genotypes_distribution(
                        folder_name,
                        self.selection_function.__class__.__name__,
                        run + 1,
                        self.iteration + 1,
                        self.fitness_function,
                    )
            keys_before_selection = self.population.get_keys_list()
            f = avg_fitness_list[self.iteration]

            self.population = self.selection_function.select(self.population)

            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(
                keys_after_selection
            )

            self.population.crossover(self.fitness_function, self.p_c)
            self.population.mutate(self.fitness_function, self.p_m)

            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            fs = self.population.get_mean_fitness()
            avg_fitness_list.append(fs)
            self.selection_diff_stats.s_list.append(fs - f)

            best_chromosome = self.population.get_best_chromosome()
            num_of_best = self.population.get_chromosomes_copies_count(best_chromosome)

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
            convergent = self.population.estimate_convergence(self.p_m)

        if convergent:
            self.pressure_stats.NI = self.iteration

        if run < ITERATIONS_TO_REPORT:
            self.population.print_ones_distribution(
                folder_name,
                self.selection_function.__class__.__name__,
                run + 1,
                self.iteration + 1,
                self.fitness_function
            )
            self.population.print_phenotypes_distribution(
                folder_name,
                self.selection_function.__class__.__name__,
                run + 1,
                self.iteration + 1,
                self.fitness_function,
            )
            if self.fitness_function.__class__.__name__ != "FHD": 
                self.population.print_genotypes_distribution(
                    folder_name,
                    self.selection_function.__class__.__name__,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function,
                )

        self.pressure_stats.takeover_time = self.iteration
        self.pressure_stats.f_found = self.population.get_max_fitness()
        self.pressure_stats.f_avg = self.population.get_mean_fitness()
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()
        is_successful = self.check_success() if convergent else False

        print("convergent", convergent)
        print("success", self.check_success())

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
        if ff_name == "FHD":
            optimal_chromosome = self.fitness_function.generate_optimal(len(self.population.genotypes_list[0]))
            optimal_chromosomes = self.population.get_chromosomes_copies_count(
                optimal_chromosome
            )
            return optimal_chromosomes == N
        else:
            success_chromosomes = [
                self.fitness_function.check_chromosome_success(p)
                for p in self.population.chromosomes
            ]
            print("any optimal", any(success_chromosomes))
            return any(success_chromosomes)

    @staticmethod
    def calculate_noise(p, sf): 
        iteration = 0
        stop = G

        while not p.estimate_convergence(0) and iteration < stop:
            p = sf.select(p)
            iteration += 1

        ns = NoiseStats()

        if p.estimate_convergence(0):
            ns.NI = iteration
            ns.conv_to = p.chromosomes[0].code[0]

        return ns
