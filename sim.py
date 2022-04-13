#!/env/bin/python3
import datetime
import random
import time

from termcolor import cprint

import environment
import organism

MAX_POP = 1300
MAX_POP_SHOWN = 130

random.seed(int(datetime.datetime.now().strftime('%Y%m%d%H%M%s')))
env = environment.Environment()
old_sig = env.signature
org1 = organism.Organism(env)
org2 = organism.Organism(env)
org3 = organism.Organism(env)

population = sorted([org1, org2, org3], key=lambda x: x.fitness, reverse=True)

MAX_SUCCESS_LIST_LEN = 10
successful_list = []

MIN_FITNESS = population[0].fitness
OLD_MIN_FITNESS = MIN_FITNESS

generations = 1

print(organism.CHARS)
while True:

    if generations % 100 == 0:
        env.adjust()
        print('environment adjustment')
        env_dist = environment.Environment.env_distance(old_sig, env.signature)
        print(f'adjustment dist: {env_dist}')
        old_sig = env.signature

    # Show only a uniform sample of the population
    if len(population) > MAX_POP_SHOWN:
        show_interval = len(population) // MAX_POP_SHOWN if len(population) > MAX_POP_SHOWN*2 else 2
        show_pop = []
        for i in range(len(population)):
            if i % show_interval == 0:
                show_pop.append(population[i])
    else:
        show_pop = population

    # attempt to regenerate a decimated population
    if len(population) < 2:
        print("population decimated. the world is quiet...")
        for i in range(3 - len(population)):
            org = organism.Organism(env)
            if org.fitness >= MIN_FITNESS:
                population.append(org)
            else:
                MIN_FITNESS += 10000

        if len(population) < 2:
            print("life struggles to find a foothold...")
            continue
        else:
            print("life finds a way...")

    cprint(''.join([x.char for x in show_pop]) + f' gens: {generations} pop: {len(population)} best f: {population[0].fitness} worst f: {population[-1].fitness} min f: {MIN_FITNESS}')

    last_gen = [x for x in population]

    # the N fittest reproduce with the M fittest
    repr_var_fn = random.choice([lambda x, y: x+y, lambda x, y: x-y])
    repr_base = len(population) // 2
    repr_var = repr_base // 2
    repr_num = repr_var_fn(repr_base, repr_var)

    if repr_num < 2:
        repr_num = 2

    for n in range(repr_num):
        a = population[n]
        b = population[random.randint(0, repr_num-1)]
        population.append(a.reproduce(b))

    # approx 10% of the population undergoes mutation
    num_mutate = round(abs(random.gauss(mu=.1, sigma=.05))*len(population))
    mutate_pop = random.sample(population, num_mutate)
    for o in mutate_pop:
        o.mutate()
    population = sorted(population, key=lambda x: x.fitness, reverse=True)

    new_pop = []
    for o in population:
        if o.fitness >= MIN_FITNESS:
            new_pop.append(o)

    population = new_pop

    # Some max number of the population survives under any circumstances
    if len(population) > MAX_POP:
        population = population[:MAX_POP]
    generations += 1

    time.sleep(1)
