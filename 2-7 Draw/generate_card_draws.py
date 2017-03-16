import random
import numpy as np
import array

handsDB = open('HandRanks.dat', 'rb')
ranks = array.array('i')
ranks.fromfile(handsDB, 32487834)
handsDB.close()

def norm(x, min, max):
	return (x-min)/(max-min)

def figureHand(hand):
    # A,2,3,4,5 NOT STRAIGHT!
    if max(hand) > 48:
        cr = [(i-1)/4+2 for i in hand]
        if len(set(cr)) > 4 and max(cr) == 5:
            hand[hand.index(max(hand))] = max(hand)-4

    p = 53
    for card in hand:
        p = ranks[p + card]
    return p

def qinput(data):
    bina = list()
    for i in data:
        #num = [0 for i in range(13)]
        #suit = [0,0,0,0]
        r = (i-1)/4
        s = i%4
        bina.append(norm(r, 0.0, 12.0))
        bina.append(norm(s, 0.0, 3.0))
        #num[r] += 1
        #suit[s] += 1
        #bina += num+suit
    return bina

def generate_draw_samples(n_draws, test = False):
    redraws = [[[1], [2], [3], [4], [5]],
               [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 5]],
               [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5],
                [3, 4, 5]],
               [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]]

    if n_draws == 2 or n_draws == 3:
        output = [0.0, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88, 1.0]
    else:
        output = [0.0, 0.25, 0.5, 0.75, 1.0]

    deck = range(1, 53)
    data = list()
    for n in range(10000):
        if n % 1000 == 0:
            print n
        np.random.shuffle(deck)
        handdata = deck[:5]
        handdata.sort()
        draws = n_draws
        winner = [0 for i in range(len(redraws[draws - 1]))]
        for run in range(1000):
            rankings = list()
            random_draw = list(deck[5:])
            np.random.shuffle(deck)
            for exc in redraws[draws - 1]:
                nhand = list(handdata)
                for i in range(len(exc)):
                    nhand[exc[i] - 1] = random_draw[i]
                rankings.append(figureHand(nhand + [0]))
            winner[rankings.index(min(rankings))] += 1
        y = output[winner.index(max(winner))]
        data.append(qinput(handdata) + [y])
        #print winner
        #print [(i-1)/4+2 for i in handdata], redraws[1][output.index(y)]
        #print qinput(handdata)
    if test:
        np.save("test_draws%s" % (str(draws)), data)
    else:
        np.save("draw%s" % (str(draws)), data)
        #print data[100:110]

if __name__ == "__main__":
    generate_draw_samples(2, True)
