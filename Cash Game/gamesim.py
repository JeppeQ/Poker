import eval7
from baseplayer import baseplayer
import numpy as np

class gamesim:
    
    def __init__(self, bp, bp1, deck, pstack, ostack, pot, betsize, board, pos, decision, big):
        self.deck = deck
        self.oppcard = deck[:2]
        self.pstack = pstack
        self.ostack = ostack
        self.pot = pot
        self.betsize = betsize
        self.board = board
        self.pos = pos
        self.decision = decision
        self.bettype = ['call', 'call']
        self.big = big
        self.late = False
        self.newround = False

        #Create Baseplayer objects
        self.bp = bp
        self.bp1 = bp1
        self.oppcard.sort()
        self.bp1.setpcards(self.oppcard)

    def initialize(self):
        if self.pos == 0:
            if len(self.board) == 0:
                self.bets = [0, self.betsize]
                self.turns = [self.bp, self.bp1]
                self.posi = [self.pos, 1-self.pos]
            else:
                self.bets = [self.betsize, 0]
                self.turns = [self.bp1, self.bp]
                self.posi = [1-self.pos, self.pos]
        else:
            if len(self.board) == 0:
                self.bets = [self.betsize, 0]
                self.turns = [self.bp1, self.bp]
                self.posi = [1-self.pos, self.pos]
            else:
                self.bets = [0, self.betsize]
                self.turns = [self.bp, self.bp1]
                self.posi = [self.pos, 1-self.pos]
            
        if self.pos == 0 and self.decision == 0 and len(self.board) == 0:
            self.late = True

        if self.decision == 100:
            self.bets[self.turns.index(self.bp)] = self.pstack
        else:
            self.bets[self.turns.index(self.bp)] = self.decision*self.big + self.betsize
    
    def bcards(self):
        self.newround = True
        if len(self.board) == 0:
            self.turns[0], self.turns[1] = self.turns[1], self.turns[0]
            self.board = self.deck[2:5]
        elif len(self.board) == 3:
            self.board = self.deck[2:6]
        elif len(self.board) == 4:
            self.board = self.deck[2:7]

    def betround(self):
        #preflop, bigblind needs to check
        if self.late:
            desc = self.bp1.decision( 0, 1-self.pos, self.pot+sum(self.bets), self.board, self.big )
            self.bettype[self.turns.index(self.bp1)] = desc[0]
            self.bets[self.turns.index(self.bp1)] += desc[1]
            self.late = False
            
        while self.newround or (self.bets.count(max(self.bets)) < len(self.bets) and 'fold' not in self.bettype):
            for i in range(len(self.turns)):
                if self.bets[i] == max(self.bets) and not self.newround:
                    continue
                else:
                    desc = self.turns[i].decision( max(self.bets)-self.bets[i], self.posi[i], self.pot+sum(self.bets), self.board, self.big )
                    self.bettype[i] = desc[0]
                    self.bets[i] += desc[1]
            self.newround = False
            

    def run(self):
        self.initialize()
        while True:
            self.betround()
            #Someone is All-In
            if (self.bets[self.turns.index(self.bp)] >= self.pstack or self.bets[self.turns.index(self.bp)] >= self.ostack) and 'fold' not in self.bettype:
                self.bets = [min(self.pstack, self.ostack) for i in self.bets]
                self.board = self.deck[2:7]
                break
            
            if 'fold' not in self.bettype and len(self.board) < 5:
                self.bcards()
            else:
                break

        #print self.board
        #Return EV
        if 'fold' in self.bettype:
            if self.turns[self.bettype.index('fold')] == self.bp:
                return self.bets[self.turns.index(self.bp)]*-1
            else:
                return self.bets[self.turns.index(self.bp1)]+self.pot
        elif self.bp.figureHand(self.bp.pcards + self.board) >= \
             self.bp.figureHand(self.bp1.pcards + self.board):
            return self.bets[self.turns.index(self.bp1)]+self.pot
        else:
            return self.bets[self.turns.index(self.bp)]*-1
            
if __name__ == '__main__':
    for i in range(1):
        pcard = ['Ah', 'Kh']
        oppcard = ['Tc', 'Td']
        pstack = 350
        ostack = 400
        pot = 15
        betsize = 5
        board = []
        pos = 0
        decision = 1
        big = 10
        gsim = gamesim(pstack, ostack, pot, betsize, board, pos, decision, big)
        print gsim.run()

        
