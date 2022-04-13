import itertools
import petname
import random
import string

from termcolor import colored

GENE_MIN_GRAN = 25
GENE_MAX_GRAN = 250

GENE_MIN = 4*GENE_MIN_GRAN
GENE_MAX = 4*GENE_MAX_GRAN

COLORS = [
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
]

PROPERTIES = [
    'bold',
    'dark',
    'underline',
    'blink',
    'reverse',
]

CHARS = string.ascii_letters + string.digits + string.punctuation


def hash_to_number(_string, mod):
    total = 0
    for letter in _string:
        total += ord(letter)
    return total % mod


class Organism(object):

    int_to_str = {
            0: 'G',
            1: 'A',
            2: 'T',
            3: 'C'
    }

    def __init__(self, env, genome=None, color=None, bg=None):
        self.env = env
        if genome is None:
            g_length = random.randint(GENE_MIN, GENE_MAX)
            gstring = ''.join([self.int_to_str[random.randint(0, 3)] for _ in range(g_length)])
            self.genome = gstring
        else:
            self.genome = genome

        self.update(color=color, bg=bg)
        self.name = petname.generate()

    @staticmethod
    def compute_letter(genome, _min=GENE_MIN, _max=GENE_MAX):
        g_length = len(genome)
        old_pct = (g_length - _min) / (_max - _min)
        index = int((len(CHARS)-1) * old_pct)
        if index >= len(CHARS):
            index = len(CHARS)-1
        if index < 0:
            index = 0
        return CHARS[index]

    def copy(self):
        return Organism(self.env, genome=self.genome, color=self.color, bg=self.bg)

    @property
    def fitness(self):
        if len(self.genome) < GENE_MIN:
            return self.env.lowest_fitness-1
        total = self.env.get_fitness(self.genome)
        if total is None:
            total = 0
            for selector in self.env.selectors:
                total += Organism.window_search(self.genome, selector.selector_string)
            self.env.store_fitness(self.genome, total)
        return total

    @staticmethod
    def hamming_dist(str1, str2):
        # not truly hamming distance
        pos_exp = 0
        sum_score = 0
        for ch1, ch2 in itertools.zip_longest(str1, str2, fillvalue='-'):
            if ch1 == ch2:
                pos_exp += 1
                sum_score += 2**pos_exp
            else:
                sum_score -= 10
                pos_exp = 0

        return sum_score

    def mutate(self):
        if random.randint(0, 100) > 1:
            return
        mutation = random.choice(['change', 'drop', 'add'])
        high = len(self.genome)//10
        if high < 2:
            high = 2
        num_to_change = random.randint(1, high)
        if num_to_change < 1:
            num_to_change = 1
        if mutation == 'change':
            for n in range(num_to_change):
                index = random.randint(0, len(self.genome)-1)
                self.genome = self.genome[:index] + self.int_to_str[random.randint(0, 3)] + self.genome[index+1:]
        elif mutation == 'drop':
            for n in range(num_to_change):
                index = random.randint(0, len(self.genome)-1)
                self.genome = self.genome[:index] + self.genome[index+1:]
        else:
            for n in range(num_to_change):
                index = random.randint(0, len(self.genome)-1)
                self.genome = self.genome[:index] + self.int_to_str[random.randint(0, 3)] + self.genome[index:]

        self.update()

    @staticmethod
    def window_search(genome, selector):
        size = len(selector)
        low = 0
        high = size
        score = 0
        while high < len(genome):
            score += Organism.hamming_dist(genome[low:high], selector)
            low += 1
            high += 1
        return score

    def reproduce(self, mate):
        genome = []
        l_length = min(len(self.genome), len(mate.genome))
        take_remaining_genome = random.choice([True, False])
        org_with_longer_genome = self if len(self.genome) >= len(mate.genome) else mate
        for i in range(l_length):
            donor = random.choice([self, mate])
            genome.append(donor.genome[i])
        if take_remaining_genome and len(org_with_longer_genome.genome) > l_length:
            genome.append(org_with_longer_genome.genome[l_length:])
        color = self.color
        bg = mate.bg
        return Organism(self.env, genome=''.join(genome), color=color, bg=bg)

    def update(self, color=None, bg=None):
        self.letter = Organism.compute_letter(self.genome)

        self.index = hash(self.genome)
        self.color = COLORS[self.index % len(COLORS)] if color is None else color
        self.bg = COLORS[self.index % (len(COLORS)-1)] if bg is None else bg
        self.prop = PROPERTIES[hash_to_number(self.genome, len(PROPERTIES))]

        self.char = colored(self.letter, self.color, 'on_'+self.bg, attrs=[self.prop])
