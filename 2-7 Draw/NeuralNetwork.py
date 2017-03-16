import numpy as np

alphas = [0.001,0.01,0.1,1,10,100,1000]

# compute sigmoid nonlinearity
def sigmoid(x):
    return 1/(1+np.exp(-x))

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)

def norm(x):
    return (x-1.0)/(51.0)

def train(data, s0, s1, neurons=70, alpha=0.003):

    X = np.array([i[:-1] for i in data])
    y = np.array([[i[-1] for i in data]]).T
    # seed random numbers to make calculation
    # deterministic (just a good practice)
    np.random.seed(1)

  #  randomly initialize our weights with mean 0
  #  synapse_0 = 2 * np.random.random((85, neurons)) - 1
   # synapse_1 = 2 * np.random.random((neurons, 1)) - 1
    synapse_0 = s0
    synapse_1 = s1

    for j in xrange(60000):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = layer_2 - y

        if (j % 1000) == 0:
            print "Error after " + str(j) + " iterations:" + str(np.mean(np.abs(layer_2_error)))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1 -= alpha * (layer_1.T.dot(layer_2_delta))
        synapse_0 -= alpha * (layer_0.T.dot(layer_1_delta))
    np.save("synaps1", synapse_1)
    np.save("synaps0", synapse_0)

if __name__ == '__main__':
    testdata = np.load("draw1.npy").tolist()
    s0 = np.load("synaps0.npy")
    s1 = np.load("synaps1.npy")
    print train(testdata, s0, s1)

