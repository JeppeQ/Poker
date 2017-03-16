import random
import numpy as np
import array
import cPickle as pickle

handsDB = open('HandRanks.dat', 'rb')
ranks = array.array('i')
ranks.fromfile(handsDB, 32487834)
handsDB.close()

def sigmoid(x):
  return 1.0 / (1.0 + np.exp(-x)) # sigmoid "squashing" function to interval [0,1]

def figureHand(hand):
    hand = list(hand)
    # A,2,3,4,5 NOT STRAIGHT!
    if max(hand) > 48:
        cr = [(i-1)/4+2 for i in hand]
        if len(set(cr)) > 4 and max(cr) == 5:
            hand[hand.index(max(hand))] = max(hand)-4

    if len(hand) < 7 and hand[-1] != 0:
        hand.append(0)

    p = 53
    for card in hand:
        p = ranks[p + card]
    return p

def rotate(l, n):
    return l[-n:] + l[:-n]

def qinput(data):
    bina = list()
    for i in data:
        r = (i-1)/4
        s = i%4
        bina.append(norm(r, 0, 12))
        bina.append(norm(s, 0, 3))
    return bina

def norm(x, min, max):
	return (x-float(min))/(max-float(min))

def marco(x):
    arr = np.array(x)
    cumsum = np.cumsum(arr)
    chain = np.array([i/cumsum[-1] for i in cumsum])
    return np.where(chain > np.random.random())[0][0]

class Player:
    def __init__(self):
        self.bet = 0
        self.handrank = 0
        self.chips = 2000
        self.folded = False
        self.redraws = [[[1], [2], [3], [4], [5]],
                   [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 5]],
                   [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5],
                    [3, 4, 5]],
                   [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]]

    def give_chips(self, chips):
        self.chips -= chips
        self.bet += chips

    def get_chips(self, chips):
        self.chips += chips

    def set_handrank(self):
        self.handrank = figureHand(self.cards)

    def start_cards(self, cards):
        self.cards = list(cards)
        self.set_handrank()

    def draw_cards(self, cards):
        self.cards += cards
        self.set_handrank()

    def bet_decision(self, betsize, cap):
        """Returns: Raise, Fold/Check"""
        desc = np.random.randint(0, 11)
        if desc < 2:
            if betsize > 0:
                self.folded = True
                return "Fold"
            else:
                return "Check"
        if desc < 6:
            if betsize > 0:
                self.give_chips(betsize)
                return "Call"
            else:
                return "Check"
        elif self.bet+20+betsize <= cap:
            self.give_chips(20+betsize)
            return "Raise"
        else:
            self.give_chips(betsize)
            return "Call"

    def draw_decision(self, _round):
        "Returns Number of Draws"
        draw = np.random.randint(0,4)
        self.cards = self.cards[:5-draw]
        return draw

    def set_position(self, pos):
        self.position = pos

    def new_round(self):
        self.bet = 0
        self.handrank = 0
        self.folded = False
        self.chips = 2000
        self.round_draws = [-1, -1, -1]
        self.discards = list()
        self.betstates = list()
        self.drawstates = list()

    def me(self):
        return False

class Heuristic(Player):
    def __init__(self):
        Player.__init__(self)

    def bet_decision(self, betsize, cap):
        if cap > 160:
            min_bet = 40
        else:
            min_bet = 20

        hr = figureHand(self.cards)
        if hr <= 4115:
            fr = 0.0
        else:
            fr = 0.1 + norm(hr, 4115, 72000)

        actions = [fr, (1-fr)/2, (1-fr)/2]
        desc = marco(actions)
        if desc == 0:
            if betsize > 0:
                self.folded = True
                return 1 #FOLD
            else:
                return 1 #CHECK
        elif desc == 1:
            if betsize > 0:
                self.give_chips(betsize)
                return 2 #CALL
            else:
                return 1 #CHECK
        elif self.bet + min_bet + betsize <= cap:
            self.give_chips(min_bet + betsize)
            return 3 #RAISE
        else:
            self.give_chips(betsize)
            return 2 #CALL

    def draw_decision(self, _round):
        goodcards = [2, 3, 4, 5, 7]
        hand = [(i-1)/4+2 for i in self.cards]
        draw = np.random.randint(0, 6-len(set(hand) & set(goodcards)))
        self.choose_draws(draw)
        self.round_draws[_round] = norm(draw, 0, 5)
        return draw

    def choose_draws(self, n_draws):
        if not n_draws:
            return
        elif n_draws == 5:
            self.cards = list()
        else:
            deck = [i for i in range(1, 53) if i not in self.cards]
            winner = [0 for i in range(len(self.redraws[n_draws-1]))]
            for run in range(1000):
                rankings = list()
                np.random.shuffle(deck)
                for exc in self.redraws[n_draws - 1]:
                    nhand = list(self.cards)
                    for i in range(len(exc)):
                        nhand[exc[i] - 1] = deck[i]
                    rankings.append(figureHand(nhand))
                winner[rankings.index(min(rankings))] += 1

            alt_draws = self.redraws[n_draws-1][ winner.index(max(winner)) ]
            discards = [i for i in self.cards if self.cards.index(i)+1 in alt_draws]
            self.cards = [i for i in self.cards if i not in discards]

class NN(Player):
    def __init__(self, m1, m2):
        Player.__init__(self)
        self.betmodel = m1
        self.drawmodel = m2

    def update_model(self):
        self.drawmodel = pickle.load(open('poker_draw_nn.p', 'rb'))
        self.betmodel = pickle.load(open('poker_bet_nn.p', 'rb'))

    def bet_decision(self, input, cap, betsize):
        if cap > 160:
            min_bet = 40
        else:
            min_bet = 20

        probs = self.policy_forward(self.betmodel, input)
        desc = marco(probs)
        if desc == 1:
            self.give_chips(betsize)
        elif desc == 2:
            if self.bet + betsize + min_bet <= cap:
                self.give_chips(betsize + min_bet)
            else:
                self.give_chips(betsize)
        elif desc == 0:
            if betsize > 0:
                self.folded = True

        self.add_state(list(input + [desc]), True)

    def policy_forward(self, model, x):
        W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
        # Forward propagation
        x = np.array(x)
        z1 = x.dot(W1) + b1
        a1 = sigmoid(z1)
        z2 = a1.dot(W2) + b2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return probs

    def draw_decision(self, input):
        goodcards = [2, 3, 4, 5, 7]
        hand = [(i - 1) / 4 + 2 for i in self.cards]
        all_ = 6-len(set(hand) & set(goodcards))
        probs = self.policy_forward(self.drawmodel, input)
        if all_ == 0:
            draw = 0
        else:
            draw = marco(probs[:all_])
        self.add_state(list(input + [draw]), False)
        self.choose_draws(draw)
        return draw

    def choose_draws(self, n_draws):
        if not n_draws:
            return
        elif n_draws == 5:
            self.cards = list()
        else:
            deck = [i for i in range(1, 53) if i not in self.cards]
            winner = [0 for i in range(len(self.redraws[n_draws-1]))]
            for run in range(1000):
                rankings = list()
                np.random.shuffle(deck)
                for exc in self.redraws[n_draws - 1]:
                    nhand = list(self.cards)
                    for i in range(len(exc)):
                        nhand[exc[i] - 1] = deck[i]
                    rankings.append(figureHand(nhand))
                winner[rankings.index(min(rankings))] += 1

            alt_draws = self.redraws[n_draws-1][ winner.index(max(winner)) ]
            discards = [i for i in self.cards if self.cards.index(i)+1 in alt_draws]
            self.cards = [i for i in self.cards if i not in discards]
            self.discards += discards

    def add_state(self, state, bet):
        if bet:
            self.betstates.append(state)
        else:
            self.drawstates.append(state)

    def reward(self):
        return self.chips - 2000

    def me(self):
        return True

class Gamesim:

    def __init__(self, n_players, betmodel, drawmodel):
        #draw_model = pickle.load(open('poker_draw_nn_1.p', 'rb'))
        #bet_model = pickle.load(open('poker_bet_nn_1.p', 'rb'))

        self.deck = range(1, 53)
        self.players = list()
        #0 BB, 1 SB
        self.positions = range(n_players)
        self.BB_pos = min(2, self.positions[-1])
        self.button_pos = 0
        self.BB = 20
        self.SB = 10
        self.betcaps = [80, 160, 320, 480]
        self.cards_drawn = 0
        self._nn = NN(betmodel, drawmodel)
        #self.players.append(NN(bet_model, draw_model))
        self.players.append(Heuristic())
        self.players.append(self._nn)

    def deal_cards(self):
        for p in range(len(self.players)):
            self.players[p].start_cards(self.deck[p*5:p*5+5])
            self.cards_drawn += 5

    def draw_cards(self, player, _round):
        if player.me():
            new_cards = player.draw_decision(self.get_draw_input(player, _round))
        else:
            new_cards = player.draw_decision(_round)
        player.draw_cards(self.deck[self.cards_drawn:self.cards_drawn + new_cards])
        self.cards_drawn += new_cards

    def betting_round(self, n_round, players):
        while True:
            for player in [p for p in players if not p.folded]:
                self.bets = [i.bet for i in self.players]
                betsize = max(self.bets)-player.bet
                if player.me():
                    input = self.get_bet_input(player, n_round, betsize)
                    player.bet_decision( input, self.betcaps[n_round], betsize )
                else:
                    player.bet_decision( betsize, self.betcaps[n_round] )
            if len(set([i.bet for i in [p for p in self.players if not p.folded]])) == 1:
                self.round_bets[n_round] = (sum([i.bet for i in self.players]) - self.round_bets[n_round-1])/1000.0
                return

    def rotate_button(self):
        #Positions
        self.positions = rotate(self.positions, 1)
        for i in range(len(self.players)):
            self.players[i].set_position(self.positions[i])
        #Bet orders
        self.R1_order = rotate( self.players, len(self.players)-(self.positions.index(self.BB_pos)+1) )
        self.R2_order = rotate( self.players, len(self.players)-(self.positions.index(self.button_pos)+1) )
        #Blinds
        self.players[self.positions.index(self.BB_pos)].give_chips(self.BB)
        self.players[self.positions.index(self.BB_pos-1)].give_chips(self.SB)

    def showdown(self, players):
        hands = [p.handrank for p in players]
        winner = min(hands)
        for player in players:
            if player.handrank == winner:
                player.get_chips( sum([i.bet for i in self.players])/hands.count(winner) )

    def new_hand(self):
        np.random.shuffle(self.deck)
        #Reset
        #Training Data (list of input, shared reward)
        self.bet_examples = list()
        self.draw_examples = list()
        self.round_bets = [-1, -1, -1, -1]
        self.cards_drawn = 0
        for p in self.players:
            p.new_round()
        #Rotate and Get Le Blinds
        self.rotate_button()
        #Deal Cards
        self.deal_cards()
        #First Betting Round - BB+1 First
        self.betting_round(0, self.R1_order)
        #Next three rounds - Button+1 First
        for round in range(3):
            # Only one player left
            active_players = [p for p in self.players if not p.folded]
            if len(active_players) == 1:
                active_players[0].get_chips(sum([i.bet for i in self.players]))
                return

            #Draw Round
            for i in range(len(self.players)):
                self.draw_cards(self.players[self.positions.index(i)], round)

            #Betting Round
            self.betting_round(round+1, self.R2_order)

        #Showdown
        self.showdown(active_players)

    def get_bet_input(self, player, round, betsize):
        cards = qinput(player.cards)
        pos = player.position
        _round = norm(round, 0, 3)
        pot = sum([i.bet for i in self.players]) / 1000.0
        hr = figureHand(player.cards)
        opp = self.players[0] if self.players[0] != player else self.players[1]
        discards = qinput(player.discards) + [-1 for i in range(30 - len(player.discards)*2)]
        return cards + [norm(hr, 4097, 36874), pos, _round, betsize/max(betsize,1), pot] + \
               self.round_bets + player.round_draws + opp.round_draws + discards

    def get_draw_input(self, player, round):
        hr = figureHand(player.cards)
        cards = qinput(player.cards)
        pos = player.position
        _round = norm(round, 0, 2)
        pot = sum([i.bet for i in self.players]) / 1000.0
        opp = self.players[0] if self.players[0] != player else self.players[1]
        discards = qinput(player.discards) + [-1 for i in range(30 - len(player.discards)*2)]
        return cards + [norm(hr, 4097, 36874), pos, _round, pot] + self.round_bets + player.round_draws + opp.round_draws + discards

    def main(self):
        self.new_hand()
        return self._nn.betstates, self._nn.drawstates, self._nn.reward()

    def update_models(self):
        self._nn.update_model()

    def test(self, samples = 1000):
        total_reward = 0
        for i in range(samples):
            np.random.seed(i)
            self.new_hand()
            total_reward += self._nn.reward()
        return total_reward

if __name__ == "__main__":
    draw_model = pickle.load(open('poker_draw_nn_1.p', 'rb'))
    bet_model = pickle.load(open('poker_bet_nn_1.p', 'rb'))
    game = Gamesim(2, bet_model, draw_model)
    print game.test()
