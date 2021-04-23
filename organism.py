import itertools
import random
import string

from termcolor import colored, cprint

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


def hash_to_number(string, mod):
    total = 0
    for l in string:
        total += ord(l)
    return total % mod


class Organism(object):

    gene = ''

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
            gstring = ''.join([self.int_to_str[random.randint(0, 3)] for i in range(g_length)])
            self.genome = gstring
        else:
            self.genome = genome
            g_length = len(genome)

        self.letter = self.compute_letter()
        self.color = random.choice(COLORS) if color is None else color
        self.bg = random.choice(COLORS) if bg is None else bg
        self.prop = PROPERTIES[hash_to_number(self.genome, len(PROPERTIES))]

        self.char = colored(self.letter, self.color, 'on_'+self.bg, attrs=[self.prop])

    def compute_letter(self):
        g_length = len(self.genome)
        old_pct = (g_length - GENE_MIN) / (GENE_MAX - GENE_MIN)
        index = int((len(CHARS)-1) * old_pct)
        if index >= len(CHARS):
            index = len(CHARS)-1
        if index < 0:
            index = 0
        return CHARS[index]

    def copy(self):
        return Organism(self.env, genome=self.genome, char=self.char, color=self.color, bg=self.bg, prop=self.prop)

    @property
    def fitness(self):
        total = 0
        num = 1
        for selector in self.env.selectors:
            total += self.window_search(selector)
            num += 1
        return total

    @staticmethod
    def hamming_dist(str1, str2):
        pos_exp = 0
        sum_score = 0
        for ch1, ch2 in itertools.zip_longest(str1, str2, fillvalue='-'):
            if ch1 == ch2:
                sum_score += 2**pos_exp
                pos_exp += 1
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
        opt = random.choice(['color', 'bg'])
        if opt == 'color':
            self.color = random.choice(COLORS)
        else:
            self.bg = random.choice(COLORS)

        self.letter = self.compute_letter()
        self.prop = PROPERTIES[hash_to_number(self.genome, len(PROPERTIES))]

    def window_search(self, selector):
        size = len(selector)
        low = 0
        high = size
        score = 0
        while high < len(self.genome):
            score += self.hamming_dist(self.genome[low:high], selector)
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
