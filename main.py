from phrase_dna import *
import time

import matplotlib.pyplot as plt

def main():
    population_size = 2000 # Per generation
    mutation_rate   = 0.01 
    target_phrase = "Hello world"
    phraser = Phrase(target_phrase=target_phrase, population=population_size, mutation_rate=mutation_rate)

    # For graph visualization
    generations_list = []
    fitness_list = []
    plt.title("Fitness Score over Time - \nTarget Phrase: \"{TARGET_PHRASE}\" - \nPopulation: {POP_SIZE} at Mutation Rate: {MUTATION_RATE}".format(POP_SIZE=population_size, TARGET_PHRASE=target_phrase, MUTATION_RATE=mutation_rate))
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.ylim(0, len(target_phrase))

    for i in range(0,9999999):
        cur_fitness = phraser.generate_population()

        # Graph to plot
        generations_list.append(i)
        fitness_list.append(cur_fitness)
        plt.plot(generations_list, fitness_list)
        plt.draw()

        if i % 1 == 0 and i != 0:
            plt.pause(0.001)

    plt.show()

if __name__ == "__main__":
    main()