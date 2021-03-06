import random

import organism

MIN_NUM_SELECTORS = 5
MAX_NUM_SELECTORS = 10
MAX_TOTAL_SELECTORS = 20

MIN_SELECTOR_SIZE = 5
MAX_SELECTOR_SIZE = 50


class Environment(object):

    def __init__(self):
        self.selectors = []
        num_selectors = random.randint(MIN_NUM_SELECTORS, MAX_NUM_SELECTORS)
        for i in range(num_selectors):
            selector = ''.join([organism.Organism.int_to_str[random.randint(0, 3)] for i in range(random.randint(MIN_SELECTOR_SIZE, MAX_SELECTOR_SIZE))])
            self.selectors.append(selector)
        self.fitness_db = {}    # (env.signature, org.gene): fitness

    def adjust(self):
        sel_index = random.randint(0, len(self.selectors)-1)
        genome_index = random.randint(0, len(self.selectors[sel_index])-1)
        selector = self.selectors[sel_index]
        self.selectors[sel_index] = selector[:genome_index] + organism.Organism.int_to_str[random.randint(0, 3)] + selector[genome_index+1:]
        adj_sels = random.choice(['add', 'drop', 'none'])
        print(f"adjustment type: {adj_sels}")
        if adj_sels == 'add':
            new_selector = ''.join([organism.Organism.int_to_str[random.randint(0, 3)] for i in range(random.randint(MIN_SELECTOR_SIZE, MAX_SELECTOR_SIZE))])
            if len(self.selectors) < MAX_TOTAL_SELECTORS:
                self.selectors.append(new_selector)
            else:
                to_replace = random.randint(0, len(self.selectors)-1)
                self.selectors[to_replace] = new_selector
        elif adj_sels == 'drop' and len(self.selectors) > MIN_NUM_SELECTORS:
            del self.selectors[random.randint(0, len(self.selectors)-1)]

    @property
    def signature(self):
        return ''.join(self.selectors)

    def store_fitness(self, gene, fitness):
        if len(self.fitness_db.keys()) == 0:
            self.lowest_fitness = fitness
            self.highest_fitness = fitness
        self.fitness_db[(self.signature, gene)] = fitness
        if fitness < self.lowest_fitness:
            self.lowest_fitness = fitness
        if fitness > self.highest_fitness:
            self.highest_fitness = fitness

    def get_fitness(self, gene):
        return self.fitness_db.get((self.signature, gene), None)

    @staticmethod
    def env_distance(sig1, sig2):
        score = abs(len(sig1) - len(sig2))
        for a, b in zip(sig1, sig2):
            if a != b:
                score += 1

        return score
