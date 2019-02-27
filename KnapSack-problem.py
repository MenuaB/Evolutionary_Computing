import random
import copy

capacity = 15
profit = (10, 9, 5, 8, 3, 12, 9, 15)
weight = (3, 5, 1, 2, 1, 9, 6, 4)
population_size = 40
tournament_parameter = 5
item_size = len(profit)
max_cost = 1000
cross_over_rate = .8
mutation_rate = .6
iteration_no = 200


def generate_population(population_size, item_size):
    population = []
    for i in range(population_size):
        temp_chromosome = []
        for j in range(item_size):
            temp_chromosome.append(random.randint(0, 1))
        if len(temp_chromosome) == item_size:
            temp_chromosome.append(
                fitness_function(temp_chromosome, capacity, profit, weight,
                                 max_cost))
        population.append(temp_chromosome)
    return population


def fitness_function(chromosome, capacity, profit, weight, max_cost):
    chromosome_worth = 0
    chromosome_weight = 0
    for i in range(len(chromosome)):
        chromosome_worth += chromosome[i] * profit[i]
        chromosome_weight += chromosome[i] * weight[i]
    if chromosome_weight > capacity:
        chromosome_worth -= max_cost
    return chromosome_worth


def choosing_parent(population_size, population, tournament_parameter):
    chosen_population = []
    while len(chosen_population) < population_size:
        chosen_population.append(
            max(random.sample(population, k=tournament_parameter),
                key=lambda l: l[-1]))
    return chosen_population


def recombination(chrome1, chrome2):
    child1, child2 = [], []
    gene_size = random.randint(0, len(chrome1) - 1)
    for i in range(len(chrome1)):
        if i <= gene_size:
            child1.append(chrome1[i])
            child2.append(chrome2[i])
        else:
            child2.append(chrome1[i])
            child1.append(chrome2[i])
    return [child1, child2]


def cross_over(cross_over_rate, chosen_population):
    generated_cross_population = []
    for i in range(0, len(chosen_population), 2):
        if random.uniform(0, 1) < cross_over_rate:
            generated_cross_population.extend(recombination(
                chosen_population[i][:-1], chosen_population[i + 1][:-1]))
        else:
            generated_cross_population.append(chosen_population[i][:-1])
            generated_cross_population.append(chosen_population[i + 1][:-1])
    return generated_cross_population


def mutation(mutation_rate, generated_cross_population):
    for i in generated_cross_population:
        if random.uniform(0, 1) < mutation_rate:
            chosen_gene = random.randint(0, len(i) - 2)
            i[chosen_gene] = (i[chosen_gene] + 1) % 2
    return generated_cross_population


def fit_join(new_generation, population):
    for i in new_generation:
        i.append(fitness_function(i, capacity, profit, weight, max_cost))
        population.append(i)
    return population


def next_generation(population):
    best_chromes = sorted(population, key=lambda x: x[-1], reverse=True)
    return best_chromes[: population_size]


def knapsack(pop):
    copy_pop = copy.deepcopy(pop)
    chosen_population = choosing_parent(population_size, copy_pop,
                                        tournament_parameter)
    generated_cross_population = cross_over(cross_over_rate, chosen_population)
    generated_mutation_population = mutation(mutation_rate,
                                             generated_cross_population)
    population = fit_join(generated_mutation_population, chosen_population)
    next_generation_population = next_generation(population)
    return next_generation_population


if __name__ == '__main__':
    counter = 0
    population = generate_population(population_size, item_size)
    while counter < iteration_no:
        next_gen = knapsack(population)
        population = copy.deepcopy(next_gen)
        print(population[0])
        counter += 1
#sdfaas
