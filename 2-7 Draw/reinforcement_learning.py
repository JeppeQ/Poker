""" Trains an agent with SPG on 2-7 triple draw. """
import numpy as np
import random
import cPickle as pickle
from gamesim import Gamesim

# Hyperparameters
H = 30 # Number of hidden neurons
batch_size = 100 # How many games do we play before updating weights?
learning_rate = 1e-4
gamma = 0.99 # Discount factor for reward
epsilon = 0.01 # learning rate for gradient descent
reg_lambda = 0.01 # regularization strength
version1 = 1
version2 = 1
resume = True

# Model initialization
# draw model
draw_input = 54
draw_output = 6
# bet model
bet_input = 55
bet_output = 3

if resume:
    draw_model = pickle.load(open('poker_draw_nn_%s.p' % str(version1), 'rb'))
    bet_model = pickle.load(open('poker_bet_nn_%s.p' % str(version1), 'rb'))
else:
    np.random.seed(0)
    draw_model = dict()
    draw_model['W1'] = np.random.randn(draw_input, H) / np.sqrt(draw_input) # "Xavier" init
    draw_model['b1'] = np.zeros((1, H))
    draw_model['W2'] = np.random.randn(H, draw_output) / np.sqrt(H)
    draw_model['b2'] = np.zeros((1, draw_output))

    bet_model = dict()
    bet_model['W1'] = np.random.randn(bet_input, H) / np.sqrt(bet_input)
    bet_model['b1'] = np.zeros((1, H))
    bet_model['W2'] = np.random.randn(H, bet_output) / np.sqrt(H)
    bet_model['b2'] = np.zeros((1, bet_output))

    pickle.dump(draw_model, open('poker_draw_nn.p', 'wb'))
    pickle.dump(bet_model, open('poker_bet_nn.p', 'wb'))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

def sigmoid(x):
  return 1.0 / (1.0 + np.exp(-x)) # sigmoid "squashing" function to interval [0,1]

def discount_rewards(r):
    """ Compute discounted rewards, Early actions count the most """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in xrange(0, r.size):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r

def policy_forward(x, y, reward, model):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']

    x = np.array(x)
    y = np.array(y)
    reward = np.array(reward)

    #Forward propagation
    z1 = x.dot(W1) + b1
    a1 = sigmoid(z1)
    z2 = a1.dot(W2) + b2
    probs = softmax(z2)

    delta3 = probs
    # Add reward

    for q in range(len(x)):
        if model == bet_model:
            if reward[q] < 0:
                delta3[q, 0] -= 1
            else:
                delta3[q, y[q]] -= 1
                delta3[q, y[q]] *= reward[q]
        else:
            delta3[q, y[q]] -= 1
            delta3[q, y[q]] *= reward[q]

        delta3[q] -= np.mean(delta3[q])

    # Backpropagate
    dW2 = (a1.T).dot(delta3)
    db2 = np.sum(delta3, axis=0, keepdims=True)
    delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
    dW1 = np.dot(x.T, delta2)
    db1 = np.sum(delta2, axis=0)

    # Add regularization terms (b1 and b2 don't have regularization terms)
    dW2 += reg_lambda * W2
    dW1 += reg_lambda * W1

    # Gradient descent parameter update
    W1 += -epsilon * dW1
    b1 += -epsilon * db1
    W2 += -epsilon * dW2
    b2 += -epsilon * db2

    # Assign new parameters to the model
    model = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    return model

def policy_backward(eph, epdlogp):
  """ backward pass. (eph is array of intermediate hidden states) """
  dW2 = np.dot(eph.T, epdlogp).ravel()
  dh = np.outer(epdlogp, model['W2'])
  dh[eph <= 0] = 0 # backpro prelu
  dW1 = np.dot(dh.T, epx)
  return {'W1':dW1, 'W2':dW2}

env = Gamesim(2, bet_model, draw_model)
running_reward = None
reward_sum = 0
episode_number = 0
bet_states, draw_states = list(), list()
bet_rewards, draw_rewards = list(), list()
bet_y, draw_y = list(), list()
# Here we go
for i in range(10000):
    episode_number += 1
    #Play hand
    bets, draws, reward = env.main()
    bet_states += [i[:-1] for i in bets]
    draw_states += [i[:-1] for i in draws]
    bet_y += [i[-1] for i in bets]
    draw_y += [i[-1] for i in draws]

    bet_rewards += [reward/500.0+1 if reward > 0 else reward/500.0-1 for i in range(len(bets))]
    draw_rewards += [reward/500.0+1 if reward > 0 else reward/500.0-1 for i in range(len(draws))]

    if episode_number % 1000 == 0:
        print episode_number

    if episode_number % batch_size == 0:
        #bet_rewards /= np.std(bet_rewards)
        #draw_rewards /= np.std(draw_rewards)

        # Forward propagation
        bet_model = policy_forward(bet_states, bet_y, bet_rewards, bet_model)

        if len(draw_states) > 0:
            draw_model = policy_forward(draw_states, draw_y, draw_rewards, draw_model)

        pickle.dump(draw_model, open('poker_draw_nn_%s.p' % str(version2), 'wb'))
        pickle.dump(bet_model, open('poker_bet_nn_%s.p' % str(version2), 'wb'))

        env.update_models()

        bet_states, draw_states = list(), list()
        bet_rewards, draw_rewards = list(), list()
        bet_y, draw_y = list(), list()