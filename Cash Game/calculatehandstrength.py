import eval7
from itertools import permutations
from random import shuffle
import array

#deck = ['Ad', 'As', 'Ah', 'Ac', 'Kd', 'Ks', 'Kh', 'Kc', 'Qd', 'Qs', 'Qh', 'Qc', 'Jd', 'Js', 'Jh', 'Jc', 'Td', 'Ts', 'Th', 'Tc', '9d', '9s', '9h', '9c', '8d', '8s', '8h', '8c', '7d', '7s', '7h', '7c', '6d', '6s', '6h', '6c', '5d', '5s', '5h', '5c', '4d', '4s', '4h', '4c', '3d', '3s', '3h', '3c', '2d', '2s', '2h', '2c']
#sh = [('Ac', 'Kc'), ('Ac', 'Qc'), ('Ac', 'Jc'), ('Ac', 'Tc'), ('Ac', '9c'), ('Ac', '8c'), ('Ac', '7c'), ('Ac', '6c'), ('Ac', '5c'), ('Ac', '4c'), ('Ac', '3c'), ('Ac', '2c'), ('Kc', 'Qc'), ('Kc', 'Jc'), ('Kc', 'Tc'), ('Kc', '9c'), ('Kc', '8c'), ('Kc', '7c'), ('Kc', '6c'), ('Kc', '5c'), ('Kc', '4c'), ('Kc', '3c'), ('Kc', '2c'), ('Qc', 'Jc'), ('Qc', 'Tc'), ('Qc', '9c'), ('Qc', '8c'), ('Qc', '7c'), ('Qc', '6c'), ('Qc', '5c'), ('Qc', '4c'), ('Qc', '3c'), ('Qc', '2c'), ('Jc', 'Tc'), ('Jc', '9c'), ('Jc', '8c'), ('Jc', '7c'), ('Jc', '6c'), ('Jc', '5c'), ('Jc', '4c'), ('Jc', '3c'), ('Jc', '2c'), ('Tc', '9c'), ('Tc', '8c'), ('Tc', '7c'), ('Tc', '6c'), ('Tc', '5c'), ('Tc', '4c'), ('Tc', '3c'), ('Tc', '2c'), ('9c', '8c'), ('9c', '7c'), ('9c', '6c'), ('9c', '5c'), ('9c', '4c'), ('9c', '3c'), ('9c', '2c'), ('8c', '7c'), ('8c', '6c'), ('8c', '5c'), ('8c', '4c'), ('8c', '3c'), ('8c', '2c'), ('7c', '6c'), ('7c', '5c'), ('7c', '4c'), ('7c', '3c'), ('7c', '2c'), ('6c', '5c'), ('6c', '4c'), ('6c', '3c'), ('6c', '2c'), ('5c', '4c'), ('5c', '3c'), ('5c', '2c'), ('4c', '3c'), ('4c', '2c'), ('3c', '2c'), ('Ac', 'Kd'), ('Ac', 'Qd'), ('Ac', 'Jd'), ('Ac', 'Td'), ('Ac', '9d'), ('Ac', '8d'), ('Ac', '7d'), ('Ac', '6d'), ('Ac', '5d'), ('Ac', '4d'), ('Ac', '3d'), ('Ac', '2d'), ('Kc', 'Qd'), ('Kc', 'Jd'), ('Kc', 'Td'), ('Kc', '9d'), ('Kc', '8d'), ('Kc', '7d'), ('Kc', '6d'), ('Kc', '5d'), ('Kc', '4d'), ('Kc', '3d'), ('Kc', '2d'), ('Qc', 'Jd'), ('Qc', 'Td'), ('Qc', '9d'), ('Qc', '8d'), ('Qc', '7d'), ('Qc', '6d'), ('Qc', '5d'), ('Qc', '4d'), ('Qc', '3d'), ('Qc', '2d'), ('Jc', 'Td'), ('Jc', '9d'), ('Jc', '8d'), ('Jc', '7d'), ('Jc', '6d'), ('Jc', '5d'), ('Jc', '4d'), ('Jc', '3d'), ('Jc', '2d'), ('Tc', '9d'), ('Tc', '8d'), ('Tc', '7d'), ('Tc', '6d'), ('Tc', '5d'), ('Tc', '4d'), ('Tc', '3d'), ('Tc', '2d'), ('9c', '8d'), ('9c', '7d'), ('9c', '6d'), ('9c', '5d'), ('9c', '4d'), ('9c', '3d'), ('9c', '2d'), ('8c', '7d'), ('8c', '6d'), ('8c', '5d'), ('8c', '4d'), ('8c', '3d'), ('8c', '2d'), ('7c', '6d'), ('7c', '5d'), ('7c', '4d'), ('7c', '3d'), ('7c', '2d'), ('6c', '5d'), ('6c', '4d'), ('6c', '3d'), ('6c', '2d'), ('5c', '4d'), ('5c', '3d'), ('5c', '2d'), ('4c', '3d'), ('4c', '2d'), ('3c', '2d'), ('Ac', 'Ad'), ('Kc', 'Kd'), ('Qc', 'Qd'), ('Jc', 'Jd'), ('Tc', 'Td'), ('9c', '9d'), ('8c', '8d'), ('7c', '7d'), ('6c', '6d'), ('5c', '5d'), ('4c', '4d'), ('3c', '3d'), ('2c', '2d')]
deck = [i for i in range(1, 53)]
starting_hands =  [(49, 50), (45, 46), (41, 42), (37, 38), (33, 34), (29, 30), (25, 26), (45, 49), (41, 49), (21, 22), (37, 49), (45, 50), (33, 49), (41, 50), (37, 50), (41, 45), (29, 49), (33, 50), (17, 18), (37, 45), (25, 49), (33, 45), (21, 49), (41, 46), (29, 50), (13, 49), (37, 46), (17, 49), (37, 41), (29, 45), (25, 50), (13, 14), (9, 49), (33, 46), (33, 41), (21, 50), (5, 49), (25, 45), (13, 50), (17, 50), (37, 42), (29, 46), (21, 45), (1, 49), (29, 41), (33, 37), (9, 50), (33, 42), (17, 45), (5, 50), (9, 10), (13, 45), (25, 41), (25, 46), (29, 37), (21, 46), (1, 50), (29, 42), (9, 45), (33, 38), (17, 46), (5, 45), (21, 41), (25, 37), (29, 33), (17, 41), (13, 46), (1, 45), (25, 42), (29, 38), (13, 41), (5, 6), (9, 46), (21, 37), (25, 33), (9, 41), (21, 42), (5, 46), (25, 38), (29, 34), (5, 41), (17, 42), (25, 29), (21, 33), (17, 37), (1, 46), (13, 42), (13, 37), (1, 41), (21, 38), (25, 34), (1, 2), (9, 37), (9, 42), (21, 29), (17, 33), (5, 37), (5, 42), (21, 25), (25, 30), (17, 38), (21, 34), (17, 29), (1, 37), (1, 42), (13, 38), (13, 33), (9, 33), (17, 25), (9, 38), (21, 30), (17, 34), (5, 33), (13, 29), (17, 21), (5, 38), (21, 26), (1, 33), (13, 25), (17, 30), (1, 38), (13, 34), (13, 21), (9, 29), (9, 34), (13, 17), (17, 26), (5, 29), (9, 25), (13, 30), (17, 22), (5, 34), (1, 29), (9, 21), (9, 13), (9, 17), (13, 26), (1, 34), (5, 25), (13, 22), (9, 30), (1, 25), (13, 18), (5, 21), (5, 30), (5, 13), (5, 17), (9, 26), (1, 30), (5, 9), (9, 22), (9, 14), (9, 18), (1, 21), (1, 13), (1, 17), (5, 26), (1, 9), (5, 22), (1, 26), (5, 14), (5, 18), (1, 5), (5, 10), (1, 22), (1, 14), (1, 18), (1, 10), (1, 6)]

handsDB = open('HandRanks.dat', 'rb')
ranks = array.array('i')
ranks.fromfile(handsDB, 32487834)
handsDB.close()

def a(x,y):
    suited = False
    if x%4 == y%4:
        suited = True
    x = (x-1)/4*4+1
    y = (y-1)/4*4+1
    if x == y:
        return (x,y+1)
    elif suited:
        return(x,y)
    else:
        return(x,y+1)
	    
def figureHand(hand):
    p = 53
    for card in hand:
        p = ranks[p + card]
    return p

def occurence():
    deck = [i for i in range(1, 53)]
    occ = [0 for i in range(169)]
    for i in range(1000000000):
        shuffle(deck)
        cards = a(*sorted(deck[:2]))
        occ[ starting_hands.index(cards) ] += 1
    return [(float(x)/1000000000) for x in occ]
        
def handstrengths(nopp):
    stre = list()
    hand = 0
    for i in starting_hands:
        hand += 1
        print hand
        cdeck = list(deck)
        cdeck.remove(i[0])
        cdeck.remove(i[1])
        count = 0

        for sim in range(1000000):
            win = True
            simdeck = list(cdeck)
            shuffle(simdeck)
            board = simdeck[-5:]
            for opp in range(nopp):
                oppcard = (simdeck[opp*2], simdeck[opp*2+1])
                if figureHand(list(oppcard)+board) > figureHand(list(i)+board):
                    win = False
            if win:
                count += 1
        stre.append(count/1000000.0)
    return stre

print handstrengths(1)



