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

    def adjust(self):
        sel_index = random.randint(0, len(self.selectors)-1)
        genome_index = random.randint(0, len(self.selectors[sel_index]))
        selector = self.selectors[sel_index]
        self.selectors[sel_index] = selector[:genome_index] + organism.Organism.int_to_str[random.randint(0,3)] + selector[genome_index+1:]
        adj_sels = random.choice(['add', 'drop', 'none'])
        if adj_sels == 'add' and len(self.selectors) < MAX_TOTAL_SELECTORS:
            selector = ''.join([organism.Organism.int_to_str[random.randint(0, 3)] for i in range(random.randint(MIN_SELECTOR_SIZE, MAX_SELECTOR_SIZE))])
            self.selectors.append(selector)
        elif adj_sels == 'drop' and len(self.selectors) > MIN_NUM_SELECTORS:
            del self.selectors[random.randint(0, len(self.selectors)-1)]
