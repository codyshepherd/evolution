#!/env/bin/python3
import datetime
import random
import time

from termcolor import cprint

import environment
import organism

MAX_POP = 130

random.seed(int(datetime.datetime.now().strftime('%Y%m%d%H%M%s')))
env = environment.Environment()
org1 = organism.Organism(env)
org2 = organism.Organism(env)
org3 = organism.Organism(env)

population = sorted([org1, org2, org3], key=lambda x: x.fitness, reverse=True)

generations = 1

print(organism.CHARS)
while True:

    if generations%500 == 0:
        env.adjust()
        print('environment adjustment')

    cprint(''.join([x.char for x in population]) + f' generations: {generations}' + f' best fitness: {population[0].fitness} worst fitness: {population[-1].fitness}')
    repr_var_fn = random.choice([lambda x,y: x+y, lambda x,y: x-y])
    repr_base = len(population) // 2
    repr_var = repr_base // 2
    repr_num = repr_var_fn(repr_base, repr_var)

    if repr_num < 2:
        repr_num = 2

    for n in range(repr_num):
        a = population[n]
        b = population[random.randint(0, repr_num)]
        population.append(a.reproduce(b))

    num_mutate = random.randint(0, len(population))
    mutate_pop = random.sample(population, num_mutate)
    for o in mutate_pop:
        o.mutate()
    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    if len(population) > MAX_POP:
        population = population[:MAX_POP]
    generations += 1
    time.sleep(1)
