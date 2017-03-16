from __future__ import division
from ctypes import *
import os
import array
from random import randint
import numpy as np

class baseplayer:

    def __init__(self, oppcards, foldratio = 0.75):
        self.foldratio = foldratio
        self.heads_up = oppcards
        self.suits = [0, 1, 2, 3]
        self.deck = [i for i in range(1, 53)]
        handsDB = open('HandRanks.dat', 'rb')
        self.ranks = array.array('i')
        self.ranks.fromfile(handsDB, 32487834)
        handsDB.close()
        
    def setpcards(self, cards):
        self.pcards = cards
        
    def figureHand(self, hand):
        p = 53
        for card in hand:
            p = self.ranks[p + card]
        return p
    
    def preflopchoice(self, pos, betsize, pot, big):
        playable = self.heads_up[:int(169*self.foldratio)]
        if self.pcards[0]%4 == self.pcards[1]%4:
            handrange = [(self.pcards[0]-1)//4*4+1, (self.pcards[1]-1)//4*4+1]
        else:
            handrange = [(self.pcards[0]-1)//4*4+2, (self.pcards[1]-1)//4*4+1 ]
        handrange.sort()

        if handrange in playable:
            if handrange in self.heads_up[:int(169*0.3)]:
                if pot <= big*5:
                    return "raise", (100-betsize)
                else:
                    return "call", betsize
            else:
                if pot == betsize+big*1.5 or betsize == 0:
                    return "raise", big*randint(1,2)
                elif betsize <= big*2:
                    return "call", betsize
                else:
                    return "fold", 0
        else:
            return "fold", 0

    def postflopchoice(self, bcards, pos, betsize, pot, big):
        if betsize == 0:
            card_odds = self.cardodds(bcards, self.pcards)      
            if card_odds > 0.66:    
                return "raise", max(big/2, (pot / (1-(1-card_odds)/card_odds-0.01)) - pot)
            else:
                return "call", betsize
        else:
            card_odds = self.cardodds(bcards, self.pcards)
            if betsize/(pot+betsize)+0.1 < card_odds:
                return "call", betsize
            elif len(bcards) != 5:
                if self.cardouts(bcards, self.pcards) > betsize/(pot+betsize)+0.1:
                    return "call", betsize
                else:
                    return "fold", 0
            else:
                return "fold", 0

    def decision(self, betsize, position, pot, bcards, big):
        #Preflop
        if len(bcards) == 0:
            choice = self.preflopchoice(position, betsize, pot, big)
            if betsize == 0 and choice[0] == 'fold':
                return "call", 0
            else:
                return choice
        else:
            return self.postflopchoice(bcards, position, betsize, pot, big)

    def cardouts(self, board, mycards):
        calcs = [0 for i in range(13)]
        specialsuits = [0 for i in range(4)]
        currentdeck = [i for i in self.deck if i not in board+mycards]

        for i in board:
            specialsuits[i%4] += 1
            
        outvalue = 0
        for kort in currentdeck:
            if specialsuits[kort%4] > 1:
                value = self.cardodds(list(board+[kort]), mycards)   
            elif calcs[(kort-1)//4] == 0:
                value = self.cardodds(list(board+[kort]), mycards)
                calcs[(kort-1)//4] = value
            else:
                value = calcs[(kort-1)//4]
            outvalue += value
        return outvalue/len(currentdeck)

    def cardodds(self, board, mycards):
        win = 0
        hands = 0
        if len(board) < 5:
            board + [0]
        myhand = self.figureHand(mycards + board)
        for i in self.heads_up:
            np.random.shuffle(self.suits)
            if i[0] % 4 == i[1] % 4:
                oppcard = [i[0]+self.suits[0], i[1]+self.suits[0]]
            else:
                oppcard = [i[0]//4*4+1+self.suits[0], i[1]//4*4+1+self.suits[1]]

            oppcard.sort()
            if oppcard[0] in mycards+board or oppcard[1] in mycards+board:
                continue
            elif self.figureHand(oppcard + board) <= myhand:
                win += 1
            hands += 1
        return win/hands
    
            
if __name__ == '__main__':
    heads_up = [[49, 50], [45, 46], [41, 42], [37, 38], [33, 34], [29, 30], [25, 26], [45, 49], [21, 22], [41, 49], [46, 49], [37, 49], [42, 49], [33, 49], [17, 18], [38, 49], [41, 45], [29, 49], [34, 49], [37, 45], [25, 49], [42, 45], [33, 45], [13, 14], [29, 50], [21, 49], [37, 46], [37, 41], [34, 45], [29, 45], [25, 50], [17, 49], [13, 49], [33, 41], [21, 50], [9, 49], [37, 42], [29, 46], [25, 45], [5, 49], [29, 41], [33, 37], [34, 41], [9, 10], [17, 50], [21, 45], [13, 50], [1, 49], [17, 45], [9, 50], [25, 41], [25, 46], [29, 37], [13, 45], [29, 42], [5, 50], [34, 37], [21, 46], [5, 6], [9, 45], [1, 50], [21, 41], [29, 33], [17, 46], [5, 45], [25, 37], [17, 41], [25, 42], [29, 38], [13, 46], [13, 41], [1, 45], [21, 37], [25, 33], [9, 46], [21, 42], [29, 34], [25, 38], [9, 41], [1, 2], [5, 46], [17, 42], [25, 29], [5, 41], [17, 37], [21, 33], [1, 46], [1, 41], [13, 42], [25, 34], [21, 38], [13, 37], [9, 42], [17, 33], [9, 37], [21, 29], [5, 42], [25, 30], [21, 34], [5, 37], [21, 25], [17, 38], [1, 42], [17, 29], [1, 37], [13, 33], [13, 38], [9, 33], [21, 30], [17, 25], [17, 34], [9, 38], [5, 33], [13, 29], [17, 21], [5, 38], [21, 26], [1, 33], [1, 38], [17, 30], [13, 25], [13, 34], [9, 29], [9, 34], [5, 29], [13, 21], [17, 26], [13, 17], [9, 25], [5, 34], [1, 29], [13, 30], [17, 22], [1, 34], [9, 21], [13, 26], [9, 13], [5, 25], [9, 17], [9, 30], [13, 22], [1, 25], [5, 30], [5, 21], [13, 18], [9, 26], [5, 13], [5, 17], [1, 30], [9, 22], [5, 9], [1, 21], [9, 14], [9, 18], [1, 13], [5, 26], [1, 17], [1, 26], [1, 9], [5, 14], [5, 22], [5, 18], [1, 5], [5, 10], [1, 22], [1, 14], [1, 18], [1, 10], [1, 6]]
    bp = baseplayer(heads_up)
    bp.setpcards( [49, 50] )
    bcards = [30, 5, 28]
    #print bp.decision(0, 0, 4, (), 1)
    print bp.decision(5, 1, 35, bcards, 5)





    
