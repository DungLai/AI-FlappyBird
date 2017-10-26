import numpy as np
import Bird as Bird_Class
from settings import *
import sys
import random

class ANN:
    def __init__(self, genome = None):
        self.fitness = 0
        self.weight1 = np.random.uniform(-1,1,(HIDDEN_LAYER, INPUT_LAYER + 1))#add bias node by adding 1 to input layer
        self.weight2 = np.random.uniform(-1,1,(OUTPUT_LAYER, HIDDEN_LAYER + 1))

        if genome is not None: #if constructor have genome then use that genome for weight
            self.decode(genome)

    def __sigmoid(self,np_array): #private method in ANN class, apply sigmoid function to numpy array
        return 1.0 / (1.0 + np.exp(-1.0 * np_array))

    def __regularize_input(self, list_input): #regularize input, make it between 0 and 1
        if np.shape(list_input) != (INPUT_LAYER,1): #check dimension of input
            sys.exit('INPUT to Neural Nets doesnt match')

        sum = np.sum(abs(list_input))

        for array in list_input:
            if sum == 0:
                array[0] = 0
            else:
                array[0] = array[0]/sum

    #This function return a number x, if x > threshold then bird.flap()
    def feed_forward(self, list_input): #list_input muse be numpy array dim(2,1)
        if np.shape(list_input) != (INPUT_LAYER,1): #check dimension of input
            sys.exit('INPUT to Neural Nets doesnt match')

        self.__regularize_input(list_input)#regularize input, make it between 0 and 1

        nodes_hidden_layer = np.dot(self.weight1, np.concatenate((np.array([[1]]), list_input),axis = 0)) #concatenate vertically, using matrix multiplication on weight and nodes

        activation_hidden_layer = self.__sigmoid(nodes_hidden_layer) #apply sigmoid activation on hidden layer

        node_output_layer = np.dot(self.weight2, np.concatenate((np.array([[1]]), activation_hidden_layer),axis = 0)) #matrix multiplication of weight and activation to create final output

        return self.__sigmoid(node_output_layer) #apply sigmoid function on final output

    def encode(self): #put all weight into a list double

        genome = [] #write each row from left to right

        for row in range(self.weight1.shape[0]): #read each row first
            for row_element in range(self.weight1.shape[1]): #read element of row from left to right
                genome.append(self.weight1[row][row_element])

        for row in range(self.weight2.shape[0]):
            for row_element in range(self.weight2.shape[1]):
                genome.append(self.weight2[row][row_element])

        return genome

    def decode(self, genome): #read weight from genome
        for i in range(HIDDEN_LAYER): #read genome from left to right
            for j in range(INPUT_LAYER+1):
                self.weight1[i][j] = genome[i*(INPUT_LAYER+1)+j]

        for i in range(OUTPUT_LAYER):
            for j in range(HIDDEN_LAYER+1):
                self.weight2[i][j] = genome[(i*(OUTPUT_LAYER)) + j + HIDDEN_LAYER*(INPUT_LAYER+1)]

    @classmethod #class method is some method that must be call with class, like ANN.selection but the only thing they care about is the parameter
    def selection(cls, bird_list):
        elite_birds_copy = [] #create a copy of list to put all elite bird in to avoid inconsistency problem
        elite_birds =  bird_list[0:round(SELECTION_PERCENTAGE*POPULATION)]

        for bird in elite_birds:
            gen = bird.ANN.encode() #encode to gen
            elite_birds_copy.append(Bird_Class.Bird(gen)) #decode gen to read weight

        return elite_birds_copy

    @classmethod
    def mutation(cls, bird): #change some weights randomly
        gen = bird.ANN.encode()

        for i in range(TOTAL_WEIGHT):
            if (np.random.rand(0,100) < MUTATION_RATE*100):
                gen[i] = np.random.uniform(-1,1) #random float from -1 to 1

        new_bird = Bird_Class.Bird(gen)

        return new_bird

    @classmethod #swap weight with certain chance (MUTATION RATE)
    def crossover(cls, bird1, bird2): #swap weight
        gen_bird1 = bird1.ANN.encode() #mutation on a gene so that the actual bird.ANN will not be change
        gen_bird2 = bird2.ANN.encode()

        for i in gen_bird1:
            if (np.random.rand(0,100) < CROSSOVER_RATE*100): #Create a random number from 0 and 100 and check with possibility of CROSSOVER_RATE
                gen_bird1[i], gen_bird2[i] = gen_bird2[i], gen_bird1[1]

        return [Bird_Class.Bird(gen_bird1), Bird_Class.Bird(gen_bird2)]

    @classmethod
    def save_weight(cls):
        pass

    @classmethod
    def create_new_generation(cls, bird_list):
        new_generation = []

        #selection
        elite_birds = ANN.selection(bird_list)
        new_generation.extend(elite_birds)

        #mutation
        for i in range(0, round(MUTATION_PERCENTAGE*100/POPULATION)):
           new_generation.append(ANN.mutation(bird_list[i]))

        # crossover with the elite birds
        for i in range(round((MUTATION_PERCENTAGE*100/POPULATION)), round(((MUTATION_PERCENTAGE*100/POPULATION) + (CROSSOVER_PERCENTAGE*100/POPULATION)))):
            new_generation.append(ANN.crossover(bird_list[i], elite_birds[random.randint(0,len(elite_birds)-1)])[0])

        #random bird to increase diversity
        for i in range(POPULATION-len(new_generation)):
            new_generation.append(Bird_Class.Bird())

        return new_generation
