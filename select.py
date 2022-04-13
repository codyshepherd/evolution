#!/usr/bin/env python
import string

import click
import datetime
import random

from typing import List

import environment
import organism

OPTIONS = {

}
QUIT = False


@click.option('-s', '--starting-pop', type=int, default=10,
              help="The number of organisms to start with")
@click.command()
def main(starting_pop):

    random.seed(int(datetime.datetime.now().strftime('%Y%m%d%H%M%s')))
    starting_env = environment.Environment()

    organisms: List[organism.Organism] = []
    for i in range(starting_pop):
        organisms.append(organism.Organism(starting_env))

    turn = -1
    while not QUIT:
        turn += 1
        if turn % 100 == 0:
            letter_options = []
            print("Selectors:")
            for letter, selector in zip(string.ascii_lowercase, starting_env.selectors):
                letter_options.append(letter)
                print(f"{letter}: {selector.name} - {selector.char}")

            killer_selector = random.choice(starting_env.selectors)

        print(f"Killer selector: {killer_selector.char}")

        numeric_options = []
        print("Organisms and fitness")
        for i, org in enumerate(organisms):
            numeric_options.append(i)
            fitness_list = [(selector, organism.Organism.window_search(org.genome, selector.selector)) for selector in
                            starting_env.selectors]
            sorted_flist = [f"{tup[0].char}: {tup[1]}" for tup in
                            sorted(fitness_list, key=lambda x: x[1], reverse=True)]
            print(f"{i}: {org.char} {org.name} - {' '.join(sorted_flist)}")

        ans = ''
        '''
        print("Pick a selector to breed for: ")
        while ans not in letter_options:
            ans = input("Choose selector: ")
        chosen_selector = ord(ans.upper()) - 64
        ans = ''
        '''

        print("Pick two organisms to breed: ")
        while ans not in numeric_options:
            ans = int(input("Choose first organism: "))
        first_org = ans

        ans = ''
        while ans not in numeric_options or ans == first_org:
            ans = int(input("Choose second organism: "))
        second_org = ans

        '''
        print("How many generations to breed?")
        while not is_int(ans):
            ans = input("Number of generations: ")
        num_generations = int(ans)
        ans = ''
        '''

        # for i in range(num_generations):
        org_1 = organisms[first_org]
        org_2 = organisms[second_org]
        # selector = starting_env.selectors[chosen_selector]

        child = org_1.reproduce(org_2)
        print(f"{child.name} was born.")
        organisms.append(child)

        organisms = sorted(
            organisms,
            key=lambda x: organism.Organism.window_search(
                x.genome,
                killer_selector.selector),
            reverse=True
        )
        print(f"{organisms[-1].name} died.")
        organisms = organisms[:-1]


def is_int(candidate):
    try:
        int(candidate)
        return True
    except TypeError:
        return False


if __name__ == '__main__':
    main()
