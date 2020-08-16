import random
import sys
import math

# Space + Uppercases + Lowercases
CHARACTER_SET = list([32]) + list(range(65,91)) + list(range(97,123))

class Phrase:
    def __init__(self, target_phrase="Hello world", population=2000, mutation_rate=0.01):
        self.target_phrase = target_phrase
        self.phrase_length = len(target_phrase)
        self.population = population
        self.mutation_rate = mutation_rate

        self.generation = 0 #starts with 0
        self.prev_phrases_scores_list = None

    def generate_population(self):
        # Generation 1 are random phrases
        if self.generation == 0:
            phrases_list = self.generate_random_population(self.population)
            # Entire Population Fitness calculation
            phrases_scores_list = self.assign_score_to_phrases_list(phrases_list)

            # Summary of fitness
            best_score = self.display_summary_of_fitness(phrases_scores_list)

            self.prev_phrases_scores_list = phrases_scores_list
            self.generation += 1
            return 
        else:
            #* Genetic Algo Processes
            # Selection
            parents_pool = self.selection(self.prev_phrases_scores_list)
            
            # Crossover with mutation
            new_phrases_list = self.crossover(parents_pool, self.population)

            # Entire Population Fitness calculation
            phrases_scores_list = self.assign_score_to_phrases_list(new_phrases_list)

            # Check if found ideal phrase
            for phrase_score in phrases_scores_list:
                if phrase_score[1] == self.phrase_length:
                    print("[~!~!~!~!~ EUREKA! Population contains a phrase that is exactly the same as target phrase \'{TARGET_PHRASE}\'".format(TARGET_PHRASE=phrase_score[0]))
                    print("[+] Found target phrase at generation: {GEN}".format(GEN=self.generation))
                    sys.exit(1)
            
            # Summary of fitness
            best_score = self.display_summary_of_fitness(phrases_scores_list)

            self.prev_phrases_scores_list = phrases_scores_list
            self.generation += 1

            return best_score

    def generate_random_population(self, population_size):
        phrases_list = []

        for _ in range(0,population_size):
            cur_phrase = ""
            for _ in range(0, self.phrase_length):
                cur_char = chr(CHARACTER_SET[random.randint(0, len(CHARACTER_SET)-1)])
                cur_phrase += cur_char

            # Add to list when finish generating a random phrase
            phrases_list.append(cur_phrase)

        return phrases_list

    def assign_score_to_phrases_list(self,phrases_list):
        phrases_scores_list = [] # list of list e.g. [['phrase', 3], ['phrack',5], ...]

        for i in phrases_list:
            cur_fitness = self.calc_fitness(i)
            phrases_scores_list.append([i, cur_fitness])

        return phrases_scores_list

    def calc_fitness(self, phrase):
        # Simple fitness scoring - if character in correct position as target phrase, 1 point
        score = 0
        for i in range(0, self.phrase_length):
            if ord(phrase[i]) == ord(self.target_phrase[i]):
                score += 1

        return score

    def display_summary_of_fitness(self, phrases_scores_list):
        # Header
        print("[*] ---------------------------------")

        # Generation info
        print("[*] Current generation: {GEN}".format(GEN=self.generation))

        # Best fitness
        best_score = 0
        best_phrase_index = None
        for index, phrase_score in enumerate(phrases_scores_list):
            if phrase_score[1] > best_score:
                best_score = phrase_score[1]
                best_phrase_index = index

        print("[+] Best fitness phrase: \'{PHRASE}\' with score: {SCORE}".format(PHRASE=phrases_scores_list[best_phrase_index][0], SCORE=best_score))
    
        print("") # new empty line

        return best_score #? Also returns best_score

    def selection(self, phrases_scores_list):
        parents_pool = []

        for phrase_score in phrases_scores_list:
            for _ in range(0, phrase_score[1]):
                parents_pool.append(phrase_score[0])

        #debug
        #print("phrases_scores_list[:1]:",phrases_scores_list[:1])
        #print("parents_pool[:10]:",parents_pool[:10])

        return parents_pool

    def crossover(self, parents_pool, population):
        new_phrases_list = []

        for i in range(0, population):
            # Randomly select parents from pool
            parent_1 = parents_pool[random.randint(0, len(parents_pool)-1)]
            parent_2 = parents_pool[random.randint(0, len(parents_pool)-1)]

            child = ""
            mid_point = math.ceil(self.phrase_length/2) # Round up (roughly mid point)

            # Select half for each parents to combine
            for j in range(0,self.phrase_length):
                # Mutate - based on mutation rate
                if random.random() < self.mutation_rate:
                    child += chr(CHARACTER_SET[random.randint(0, len(CHARACTER_SET)-1)]) # Generate a random character as mutation
                    continue
                # Crossover
                else:
                    if j < mid_point:
                        child += parent_1[j]
                    else:
                        child += parent_2[j]

            new_phrases_list.append(child)

        return new_phrases_list