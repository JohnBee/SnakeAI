`# Uses Genetic Algorithms to adjust the weights of a NN to play Snake
# NN inputs:
# Clear Forward
# Clear Left
# Clear Right
# Food Left
# Food Right
# Food Forward

# NN outputs:
# Go forward
# Go Left
# Go Right

# Fitness of a NN is defined as:
# Moving 1 square = 1
# Picking up Food = 100 // The equivalent of transversing every square
from random import random
from SnakeAi.snake_engine.engine import Engine

class SimpleNN:
    def __init__(self, in_layers):
        '''

        :param in_layers: a list a values presenting the size of each layer, input to the output layer, final number
        should be size of the output layer
        '''
        # initialise random weights for input layers
        # +1 for the bias
        self.layers = []
        for i in range(1, len(in_layers)):
            # create a number of randomly weighted neurons with the number of weights equal to the number of neurons
            # in the previous layer. must have number of weights equal to the number of inputs in the layer before it.
            self.layers.append([[random() for n in range(in_layers[i-1]+1)] for x in range(in_layers[i])])


    @staticmethod
    def sigmoid_func(x):
        e = 2.7182818284590452353602874
        ex = e ** x
        out = ((ex) / (ex + 1)) - 0.5
        return out

    @staticmethod
    def activate_transfer(neuron_weights, input_layer):
        activ_out = neuron_weights[-1] # add the bias
        for i in range(len(neuron_weights) - 1): # all weights but the bias
            activ_out += neuron_weights[i] * input_layer[i]
        return SimpleNN.sigmoid_func(activ_out)

    def forward_propagate(self, input_l):
        inp = input_l
        for layer in self.layers:
            n_inps = []
            for neuron in layer:
                activ = self.activate_transfer(neuron, inp)
                n_inps.append(activ)
            inp = n_inps
        return inp

    @staticmethod
    def argmax(layer):
        max_val = max(layer)
        return [0 if x != max_val else 1 for x in layer]


def get_sensors(game):
    '''
    Supply a snake game and will return the result of the snake sensors
    :param game:
    :return: outputs a list of the snakes sensors Clear left, right, forward. Food left, right, forward
    '''
    direction = game.snake.direction
    head = game.snake.head
    body = game.snake.body
    food = game.food
    # 0 right (1, 0), 1 up (0, 1), 2 left (-1, 0), 3 down (0, -1)
    check_spaces = [(1,0), (0, 1), (-1, 0), (0, -1)]

    out = {"clear_left": True, "clear_right": True, "clear_forward": True, "food_left": False, "food_right": False, "food_forward": False}

    # clear in front of snake
    # check forward
    # clear check
    forward = (head[0] + check_spaces[direction][0], head[1] + check_spaces[direction][1])
    left = (head[0] + check_spaces[direction+1 % 4][0], head[1] + check_spaces[direction+1 % 4][1])
    right = (head[0] + check_spaces[direction-1 % 4][0], head[1] + check_spaces[direction-1 % 4][1])


    if forward in body or forward[0] < 0 or forward[0] > 9 or forward[1] < 0 or forward[1] > 9:
        out["clear_forward"] = False

    if left in body or left[0] < 0 or left[0] > 9 or left[1] < 0 or left[1] > 9:
        out["clear_left"] = False

    if right in body or right[0] < 0 or right[0] > 9 or right[1] < 0 or right[1] > 9:
        out["clear_right"] = False

    # food check
    if direction == 0: # going to the right
        out["food_forward"] = food[0] > head[0]
        out["food_left"] = food[1] < head[1]
        out["food_right"] = food[1] > head[1]

    if direction == 1: # going up
        out["food_forward"] = food[1] < head[1]
        out["food_left"] = food[0] < head[0]
        out["food_right"] = food[0] > head[0]

    if direction == 2: # going left
        out["food_forward"] = food[0] < head[0]
        out["food_left"] = food[1] > head[1]
        out["food_right"] = food[1] < head[1]

    if direction == 3: # going down
        out["food_forward"] = food[1] > head[1]
        out["food_left"] = food[0] > head[0]
        out["food_right"] = food[0] < head[0]


# genetic algorithm handler
class GeneticAlgorithm:
    def __init__(self, network_layers=None, population_size=100):
        if network_layers is None:
            network_layers = []
        self.population = self.initialise_population(network_layers, population_size)

    @staticmethod
    def initialise_population(self, network_layers, pop_size):
        return [SimpleNN(network_layers) for x in range(pop_size)]

    @staticmethod
    def fitness(agent):
        # initialise the game:
        e = Engine()






if __name__ == "__main__":
    n = SimpleNN([2, 1, 2, 2])
    out = n.forward_propagate([1, 0])
    a_max = SimpleNN.argmax(out)
    pass
`