# Uses Genetic Algorithms to adjust the weights of a NN to play Snake
# NN inputs:
# Clear Forward
# Clear Left
# Clear Right
# Food Left
# Food Right
# Food Ahead

# NN outputs:
# Go forward
# Go Left
# Go Right

# Fitness of a NN is defined as:
# Moving 1 square = 1
# Picking up Food = 100 // The equivalent of transversing every square
from random import random


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

if __name__ == "__main__":
    n = SimpleNN([2, 1, 2, 2])
    out = n.forward_propagate([1, 0])
    a_max = SimpleNN.argmax(out)
    pass
