import itertools
from gamesim import gamesim
from baseplayer import baseplayer
import numpy as np
import time

class oppsim:

    def __init__(self, pot, stacksize, betsize):
        self.heads_up = [[49, 50], [45, 46], [41, 42], [37, 38], [33, 34], [29, 30], [25, 26], [45, 49], [21, 22], [41, 49], [46, 49], [37, 49], [42, 49], [33, 49], [17, 18], [38, 49], [41, 45], [29, 49], [34, 49], [37, 45], [25, 49], [42, 45], [33, 45], [13, 14], [30, 49], [21, 49], [38, 45], [37, 41], [34, 45], [29, 45], [26, 49], [17, 49], [13, 49], [33, 41], [22, 49], [9, 49], [38, 41], [30, 45], [25, 45], [5, 49], [29, 41], [33, 37], [34, 41], [9, 10], [18, 49], [21, 45], [14, 49], [1, 49], [17, 45], [10, 49], [25, 41], [26, 45], [29, 37], [13, 45], [30, 41], [6, 49], [34, 37], [22, 45], [5, 6], [9, 45], [2, 49], [21, 41], [29, 33], [18, 45], [5, 45], [25, 37], [17, 41], [26, 41], [30, 37], [14, 45], [13, 41], [1, 45], [21, 37], [25, 33], [10, 45], [22, 41], [30, 33], [26, 37], [9, 41], [1, 2], [6, 45], [18, 41], [25, 29], [5, 41], [17, 37], [21, 33], [2, 45], [1, 41], [14, 41], [26, 33], [22, 37], [13, 37], [10, 41], [17, 33], [9, 37], [21, 29], [6, 41], [26, 29], [22, 33], [5, 37], [21, 25], [18, 37], [2, 41], [17, 29], [1, 37], [13, 33], [14, 37], [9, 33], [22, 29], [17, 25], [18, 33], [10, 37], [5, 33], [13, 29], [17, 21], [6, 37], [22, 25], [1, 33], [2, 37], [18, 29], [13, 25], [14, 33], [9, 29], [10, 33], [5, 29], [13, 21], [18, 25], [13, 17], [9, 25], [6, 33], [1, 29], [14, 29], [18, 21], [2, 33], [9, 21], [14, 25], [9, 13], [5, 25], [9, 17], [10, 29], [14, 21], [1, 25], [6, 29], [5, 21], [14, 17], [10, 25], [5, 13], [5, 17], [2, 29], [10, 21], [5, 9], [1, 21], [10, 13], [10, 17], [1, 13], [6, 25], [1, 17], [2, 25], [1, 9], [6, 13], [6, 21], [6, 17], [1, 5], [6, 9], [2, 21], [2, 13], [2, 17], [2, 9], [2, 5]]
        #smallblind = [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #C, S, H, D
        self.suits = [0, 1, 2, 3]
        self.deck = [i for i in range(1, 53)]
        self.stacksize = stacksize
        self.betsize = betsize
        self.pot = pot
        self.bets = [0, 2, 100]
        self.bp = baseplayer(self.heads_up)
        self.bp1 = baseplayer(self.heads_up)
        self.initialize()

    def initialize(self):
        cardgrps = list()
        values = list()
        finalgrps = [list() for i in range(len(self.bets))]
        starttime = int(round(time.time() * 1000))
        count = 0
        
        for i in self.heads_up:
            self.bp.setpcards(i)
            values.append( self.decision(i) )

        print values

        for i in range(len(cardgrps)):
            if max(values[i]) > 0:
                finalgrps[values[i].index(max(values[i]))].append( cardgrps[i] )

    def decision(self, pcards):
        self.deck = [i for i in self.deck if i not in pcards]   
        values = [0 for i in range(len(self.bets))]
        for i in range(5000):
            for bet in range(len(self.bets)):
                np.random.shuffle(self.deck)
                gsim = gamesim(self.bp, self.bp1, self.deck, self.stacksize, 500, self.pot, self.betsize, [], 0, self.bets[bet], 20)
                values[bet] += round(gsim.run(), 2)
        if max(values) < 0:
            return -1
        return values.index(max(values))

if __name__ == '__main__':
    opp = oppsim(30, 500, 10)
    
