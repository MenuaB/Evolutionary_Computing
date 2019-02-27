import random
import copy

queen_no = 64
chromosome_size = queen_no
population_size = 1000
tournament_parameter = 4
cross_over_rate = .8
mutation_rate = 1
iteration_no = 200


def generate_population(chromosome_size, population_size, queen_no):
    population = []
    choice_list = [i for i in range(queen_no)]
    for i in range(population_size):
        random.shuffle(choice_list)
        temp_chromosome = choice_list.copy()
        temp_chromosome = fitness_function(temp_chromosome)
        population.append(temp_chromosome)
    return population


def fitness_function(chromosome):
    fitness = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if abs(i - j) == abs(chromosome[i] - chromosome[j]):
                fitness -= 1
    chromosome.append(fitness)
    return chromosome


def select_parent(population, population_size, tournament_parameter):
    selected_population = []
    while len(selected_population) < population_size:
        selected_population.append(
            max(random.sample(population, k=tournament_parameter),
                key=lambda l: l[-1]))
    return selected_population


def recombination(parent1, parent2):
    child1, child2 = [], []
    gene_size = random.randint(0, len(parent1) - 1)
    for i in range(len(parent1)):
        if i < gene_size:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            for j in range(gene_size - len(parent1) + 1, gene_size + 1):
                if parent1[j] not in child2:
                    child2.append(parent1[j])
                if parent2[j] not in child1:
                    child1.append(parent2[j])
    return [child1, child2]


def cross_over(population, cross_over_rate):
    cross_overed_population = []
    for i in range(0, len(population), 2):
        if random.uniform(0, 1) < cross_over_rate:
            cross_overed_population.extend(
                recombination(population[i][:-1], population[i + 1][:-1]))
        else:
            cross_overed_population.extend(
                [population[i][:-1], population[i + 1][:-1]])
    return cross_overed_population


def mutation(population, mutation_rate):
    for chromosome in population:
        if random.uniform(0, 1) < mutation_rate:
            random_genes = random.sample(
                [i for i in range(len(population[0]))], 2)
            chromosome[random_genes[0]], chromosome[random_genes[1]] = \
                chromosome[random_genes[1]], chromosome[random_genes[0]]
    return population


def fit_join(new_generation, population):
    for chromosome in new_generation:
        chromosome = fitness_function(chromosome)
        population.append(chromosome)
    return population


def next_generation(population):
    best_chromes = sorted(population, key=lambda x: x[-1], reverse=True)
    return best_chromes[: population_size]


def evolution(pop):
    population = select_parent(pop, population_size, tournament_parameter)
    cross_overed_population = cross_over(population, cross_over_rate)
    mutated_population = mutation(cross_overed_population, mutation_rate)
    new_generation = fit_join(mutated_population, population)
    new_population = next_generation(new_generation)
    return new_population


if __name__ == '__main__':
    counter = 0
    population = generate_population(chromosome_size, population_size,
                                     queen_no)
    while counter < iteration_no:
        next_gen = evolution(population)
        population = copy.deepcopy(next_gen)
        print(population[0])
        counter += 1
