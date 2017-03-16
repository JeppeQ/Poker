from __future__ import division

import array
import heapq
import itertools as it
import random
import sqlite3
import time
from collections import deque

from scraper.screenshot import *

conn = sqlite3.connect('handranges.db')
starting_hands = [(49, 50), (45, 46), (41, 42), (37, 38), (33, 34), (29, 30), (25, 26), (45, 49), (41, 49), (21, 22),
                  (37, 49), (45, 50), (33, 49), (41, 50), (37, 50), (41, 45), (29, 49), (33, 50), (17, 18), (37, 45),
                  (25, 49), (33, 45), (21, 49), (41, 46), (29, 50), (13, 49), (37, 46), (17, 49), (37, 41), (29, 45),
                  (25, 50), (13, 14), (9, 49), (33, 46), (33, 41), (21, 50), (5, 49), (25, 45), (13, 50), (17, 50),
                  (37, 42), (29, 46), (21, 45), (1, 49), (29, 41), (33, 37), (9, 50), (33, 42), (17, 45), (5, 50),
                  (9, 10), (13, 45), (25, 41), (25, 46), (29, 37), (21, 46), (1, 50), (29, 42), (9, 45), (33, 38),
                  (17, 46), (5, 45), (21, 41), (25, 37), (29, 33), (17, 41), (13, 46), (1, 45), (25, 42), (29, 38),
                  (13, 41), (5, 6), (9, 46), (21, 37), (25, 33), (9, 41), (21, 42), (5, 46), (25, 38), (29, 34),
                  (5, 41), (17, 42), (25, 29), (21, 33), (17, 37), (1, 46), (13, 42), (13, 37), (1, 41), (21, 38),
                  (25, 34), (1, 2), (9, 37), (9, 42), (21, 29), (17, 33), (5, 37), (5, 42), (21, 25), (25, 30),
                  (17, 38), (21, 34), (17, 29), (1, 37), (1, 42), (13, 38), (13, 33), (9, 33), (17, 25), (9, 38),
                  (21, 30), (17, 34), (5, 33), (13, 29), (17, 21), (5, 38), (21, 26), (1, 33), (13, 25), (17, 30),
                  (1, 38), (13, 34), (13, 21), (9, 29), (9, 34), (13, 17), (17, 26), (5, 29), (9, 25), (13, 30),
                  (17, 22), (5, 34), (1, 29), (9, 21), (9, 13), (9, 17), (13, 26), (1, 34), (5, 25), (13, 22), (9, 30),
                  (1, 25), (13, 18), (5, 21), (5, 30), (5, 13), (5, 17), (9, 26), (1, 30), (5, 9), (9, 22), (9, 14),
                  (9, 18), (1, 21), (1, 13), (1, 17), (5, 26), (1, 9), (5, 22), (1, 26), (5, 14), (5, 18), (1, 5),
                  (5, 10), (1, 22), (1, 14), (1, 18), (1, 10), (1, 6)]
winrate = [0.854507, 0.826663, 0.802036, 0.777129, 0.754494, 0.724808, 0.695609, 0.678709, 0.670584, 0.668315, 0.663992,
           0.66166, 0.656615, 0.653471, 0.646847, 0.644195, 0.639872, 0.638683, 0.637855, 0.637003, 0.633704, 0.630142,
           0.626635, 0.62485, 0.620697, 0.617249, 0.61771, 0.616086, 0.614222, 0.613999, 0.613624, 0.609877, 0.608788,
           0.610059, 0.607069, 0.605516, 0.601535, 0.598578, 0.596096, 0.59571, 0.593655, 0.592861, 0.592665, 0.592392,
           0.591603, 0.589442, 0.588025, 0.586252, 0.585137, 0.578097, 0.578227, 0.577933, 0.576707, 0.575945, 0.572796,
           0.570564, 0.568852, 0.568304, 0.56881, 0.566909, 0.561715, 0.560755, 0.561292, 0.557828, 0.556999, 0.555945,
           0.553212, 0.551377, 0.551941, 0.548833, 0.548255, 0.546331, 0.543223, 0.542516, 0.541495, 0.53963, 0.536465,
           0.534926, 0.5315, 0.531626, 0.531729, 0.531491, 0.528175, 0.526108, 0.525773, 0.524993, 0.522903, 0.520615,
           0.52223, 0.516304, 0.515246, 0.512921, 0.51328, 0.511949, 0.513557, 0.510664, 0.504712, 0.503763, 0.500468,
           0.50147, 0.500296, 0.499627, 0.496383, 0.495803, 0.495145, 0.494364, 0.495038, 0.4891, 0.486606, 0.484814,
           0.485471, 0.483452, 0.479995, 0.481926, 0.47974, 0.475507, 0.474027, 0.471484, 0.471451, 0.468476, 0.46614,
           0.466801, 0.463831, 0.461742, 0.45858, 0.458993, 0.457878, 0.457665, 0.453253, 0.451411, 0.449147, 0.449715,
           0.448471, 0.445447, 0.444863, 0.442005, 0.440779, 0.441068, 0.434641, 0.433275, 0.432257, 0.427736, 0.428823,
           0.427485, 0.42661, 0.42662, 0.423701, 0.421639, 0.41783, 0.41572, 0.414028, 0.411585, 0.409046, 0.408883,
           0.40798, 0.404819, 0.402399, 0.39765, 0.394783, 0.395532, 0.394493, 0.390515, 0.388641, 0.381948, 0.374348,
           0.373972, 0.371218, 0.362741, 0.354495]
occ = [0.0045525, 0.004547, 0.0045555, 0.004553, 0.0045052, 0.0045224, 0.0045451, 0.0030038, 0.00303, 0.0045148,
       0.0030203, 0.0090336, 0.0030281, 0.0090099, 0.009052, 0.0030156, 0.0030191, 0.0090485, 0.0044886, 0.0030621,
       0.0030319, 0.0029907, 0.0030235, 0.009041, 0.0090772, 0.002992, 0.009095, 0.0030073, 0.0030242, 0.0030118,
       0.0090552, 0.004516, 0.0030008, 0.0090543, 0.0030208, 0.0089864, 0.0030035, 0.0030211, 0.0090499, 0.0090778,
       0.0090484, 0.0090845, 0.0030206, 0.003034, 0.0030149, 0.0030568, 0.0090533, 0.0090287, 0.0030189, 0.0090156,
       0.0045261, 0.0030164, 0.0030295, 0.0090104, 0.0030152, 0.0089718, 0.0090304, 0.0090029, 0.0030245, 0.009076,
       0.0090732, 0.0030185, 0.0030221, 0.0030252, 0.0030036, 0.0029847, 0.0090292, 0.0030268, 0.009076, 0.0090768,
       0.0030075, 0.0045195, 0.0090166, 0.0029996, 0.0030272, 0.0030386, 0.0090719, 0.0090429, 0.0090138, 0.0090259,
       0.003054, 0.0090032, 0.0029965, 0.0030341, 0.0030101, 0.0090492, 0.0090405, 0.0030106, 0.0030077, 0.0090694,
       0.0090643, 0.0044739, 0.0029823, 0.0090371, 0.0030097, 0.0030121, 0.0030471, 0.0090586, 0.0030239, 0.009035,
       0.0090203, 0.0090231, 0.0030236, 0.0030328, 0.0090338, 0.0090303, 0.0030322, 0.0030621, 0.0030043, 0.0090662,
       0.0090507, 0.0090842, 0.0030187, 0.0029978, 0.0030018, 0.009035, 0.0090512, 0.00302, 0.00299, 0.0090378,
       0.0090783, 0.0090524, 0.0030294, 0.003038, 0.0090806, 0.0030185, 0.0090697, 0.0030223, 0.003044, 0.0090659,
       0.0090543, 0.0090446, 0.0030362, 0.0030091, 0.0030233, 0.0030088, 0.0090219, 0.0090524, 0.0029939, 0.0091156,
       0.0090936, 0.0029797, 0.0090293, 0.0030356, 0.0090184, 0.0030032, 0.0030149, 0.0090854, 0.0090845, 0.0029742,
       0.0090159, 0.0089954, 0.009076, 0.0030309, 0.0029933, 0.0030118, 0.0090388, 0.0030382, 0.0090137, 0.0090512,
       0.0090718, 0.0090504, 0.0030183, 0.0090112, 0.0091127, 0.009069, 0.0090509, 0.0090823, 0.009089]


def get_hand(x, y):
    suited = False
    if x % 4 == y % 4:
        suited = True
    x = (x - 1) // 4 * 4 + 1
    y = (y - 1) // 4 * 4 + 1
    if x == y:
        return x, y + 1
    elif suited:
        return x, y
    else:
        return x, y + 1


def calc_starting_hands():
    hands = list(it.permutations([i for i in range(1, 53)], 2))
    hands = list(set([tuple(sorted(i)) for i in hands]))
    res = list()
    for h in starting_hands:
        for x in hands:
            if get_hand(*x) == h:
                res.append(x)
    return res


class hyper_turbo:
    def __init__(self, first, second, total=3001):
        handsDB = open('HandRanks.dat', 'rb')
        self.ranks = array.array('i')
        self.ranks.fromfile(handsDB, 32487834)
        handsDB.close()
        self.total_chips = total
        self.fi = first
        self.se = second
        self.starthands = calc_starting_hands()
        self.diffpos = ['lojack', 'hijack', 'cutoff', 'button', 'sb', 'bb']

    def state(self, big, ante, players, cards, button, chips, bets):
        self.used = list()
        self.bb = big
        self.antepot = players * ante
        self.ante = min([0, 10, 13, 17, 25], key=lambda x: abs(x - ante / big * 100))
        self.players = players
        self.button = button
        self.cards = cards
        self.deck = [i for i in range(1, 53) if i not in self.cards]

        self.chips = chips
        self.bets = bets
        self.hands = [self.cards, 0, 0, 0, 0, 0]
        self.cards_used(*self.cards)
        self.folded_players = list()
        self.set_og(chips, bets, self.deck)

    def set_og(self, chips, bets, deck):
        self.og_chips = list(chips)
        self.og_bets = list(bets)
        self.og_deck = list(deck)
        self.og_folds = list()

    def reset_state(self):
        self.used = list()
        self.folded_players = list(self.og_folds)
        self.deck = list(self.og_deck)
        self.bets = list(self.og_bets)
        self.chips = list(self.og_chips)
        self.hands = [self.cards, 0, 0, 0, 0, 0]
        self.cards_used(*self.cards)
        self.ebig = self.og_ebig
        self.epos = self.og_epos

    def runner_up(self, players):
        total = [0 for i in range(6)]
        for p in players:
            try:
                total[p] = self.bets[p] + self.chips[p]
            except:
                total[p] = self.bets[p]
        return total.index(heapq.nlargest(2, total)[1])

    def sort_opponents(self):
        self.first = self.fi
        self.second = self.se
        if self.players == 3:
            self.second = 0

        _all = [i for i in range(6) if self.chips[i] != 0]
        pos = ['lojack', 'hijack', 'cutoff', 'button', 'sb', 'bb'][-self.players:]
        self.runnerup = self.runner_up(_all)

        if self.bets[0] > self.bb:
            self._all = _all
            self.preplayers = list(_all[1:])
            self.postplayers = []
            d = deque(pos)
            d.rotate(1)
            self.positions = list(d)
            return

        if self.players == 2:
            self._all = _all
            if self.button == 0:
                self.positions = list(pos)
                self.preplayers = []
                self.postplayers = [_all[1]]
            else:
                self.positions = ['bb', 'sb']
                self.preplayers = [_all[1]]
                self.postplayers = []
            return

        d = deque(pos)
        d.rotate(_all.index(self.button) - pos.index('button'))
        self.positions = list(d)
        prep = pos.index(self.positions[0])
        self._all = _all

        if prep == 0:
            self.preplayers = []
        else:
            self.preplayers = _all[-prep:]
        self.postplayers = _all[1:len(_all) - len(self.preplayers)]

    def cards_used(self, x, y):
        self.used += [x, y]

    def open_range(self, pos, blinds):
        return conn.execute("SELECT range FROM hyper WHERE players=%s AND blinds=%s AND pos='%s' AND ante=%s" %
                            (str(self.players), str(min(25, max(1, blinds))), pos, str(self.ante))).fetchone()[0]

    def call_range(self, openpos, pos, blinds):
        if self.diffpos.index(openpos) > self.diffpos.index(pos):
            openpos, pos = pos, openpos
        return conn.execute(
            "SELECT range FROM hypercall WHERE openpos='%s' AND players=%s AND blinds=%s AND pos='%s' AND ante=%s" %
            (openpos, str(self.players), str(min(25, max(1, blinds))), pos, str(self.ante))).fetchone()[0]

    def pre_ranges(self):
        ranges = list()
        self.ebig = 0
        self.epos = ""
        for p in self.preplayers:
            # Get Maximum blind - if chip leader goes all in
            max_blind = list()
            for c in [i for i in self._all if i != p and i not in self.folded_players]:
                if self.chips[c] == 'all':
                    max_blind.append(self.bets[c] // self.bb)
                else:
                    max_blind.append((self.chips[c] + self.bets[c]) // self.bb)
            max_blinds = max(max_blind)

            # Fold
            if self.bets[p] < self.bb and self.chips[p] != 'all':
                self.folded_players.append(p)
                if self.ebig == 0:  # Open fold
                    ranges.append((self.open_range(self.positions[self._all.index(p)], self.chips[p] // self.bb), 0, p))
                else:  # Call fold
                    ranges.append((self.call_range(self.epos, self.positions[self._all.index(p)], self.ebig), 0, p))
            elif self.bets[p] >= self.bb:
                if not self.ebig:
                    if self.chips[p] == 'all':
                        shoveb = min(max_blinds, self.bets[p] // self.bb)
                    else:
                        shoveb = min(max_blinds, max(self.bets[p], self.chips[p]) // self.bb)
                    ranges.append((self.open_range(self.positions[self._all.index(p)], shoveb), 1, p))

                else:
                    if self.chips[p] == 'all':
                        shoveb = min(max_blinds, self.bets[p] // self.bb)
                    else:
                        shoveb = min(max_blinds, max(self.bets[p], self.chips[p]) // self.bb)
                    ranges.append((self.call_range(self.epos, self.positions[self._all.index(p)], self.ebig), 1, p))

                if shoveb > self.ebig:
                    self.ebig = shoveb
                    self.epos = self.positions[self._all.index(p)]
                if self.bets[p] == max(self.bets):
                    self.epos = self.positions[self._all.index(p)]

            elif self.bets[p] < self.bb and self.chips[p] == 'all':
                ranges.append((100, 1, p))
        self.og_folds = list(self.folded_players)
        self.og_ebig = self.ebig
        self.og_epos = self.epos
        return ranges

    def set_ebig(self):
        max_blind = list()
        for c in [i for i in self._all if i != 0 and i not in self.folded_players]:
            if self.chips[c] == 'all':
                max_blind.append(self.bets[c] // self.bb)
            else:
                max_blind.append((self.chips[c] + self.bets[c]) // self.bb)
        max_blinds = max(max_blind)

        if self.chips[0] == 'all':
            if min(self.bets[0] // self.bb, max_blinds) > self.ebig:
                self.ebig = min(self.bets[0] // self.bb, max_blinds)
        else:
            if min(max(self.bets[0], self.chips[0]) // self.bb, max_blinds) > self.ebig:
                self.ebig = min(max(self.bets[0], self.chips[0]) // self.bb, max_blinds)
        if self.bets[0] == max(self.bets):
            self.epos = self.positions[0]

    def post_desc(self, p, pcards):
        self.hands[p] = pcards
        if self.chips[p] == 'all' or (
                    self.positions[self._all.index(p)] == 'bb' and self.bets[p] == max(self.bets) and self.bets.count(
                max(self.bets)) == 1):
            return

        _range = starting_hands.index(get_hand(*sorted(pcards)))

        if len(self.folded_players) == self.players - 1:
            return

        # Get Maximum blind - if chip leader goes all in
        max_blind = [0]
        for c in [i for i in self._all if i != p and i not in self.folded_players]:
            if self.chips[c] == 'all':
                max_blind.append(self.bets[c] // self.bb)
            else:
                max_blind.append((self.chips[c] + self.bets[c]) // self.bb)
        max_blinds = max(max_blind)

        if self.ebig == 0:
            if 169 * self.open_range(self.positions[self._all.index(p)], self.chips[p] // self.bb) / 100 > _range:
                self.bets[p] += self.chips[p]
                self.chips[p] = 'all'
            else:
                self.folded_players.append(p)
        else:
            if 169 * self.call_range(self.epos, self.positions[self._all.index(p)], self.ebig) / 100 > _range:
                self.bets[p] += self.chips[p]
                self.chips[p] = 'all'
            else:
                self.folded_players.append(p)
        shoveb = min(self.bets[p] // self.bb, max_blinds)

        if shoveb > self.ebig:
            self.ebig = shoveb
            self.epos = self.positions[self._all.index(p)]
        if self.bets[p] == max(self.bets):
            self.epos = self.positions[self._all.index(p)]

    def after_desc(self):
        for p in [x for x in self.preplayers if
                  x not in self.folded_players and self.bets[x] < max(self.bets) and self.chips[x] != 'all']:
            _range = starting_hands.index(get_hand(*sorted(self.hands[p])))
            if 169 * self.call_range(self.positions[self._all.index(p)], self.epos,
                                     self.ebig - self.bets[p] // self.bb) / 100 > _range:
                trump = min(max(self.bets) - self.bets[p], self.chips[p])
                self.bets[p] += trump
                self.chips[p] -= trump
                if self.chips[p] == 0:
                    self.chips[p] = 'all'
            else:
                self.folded_players.append(p)

    def random_hand(self, r, x):
        def availeble(c, y):
            return c in self.used or y in self.used

        if x:
            _range = self.starthands[:int(1326 * r / 100)]
        else:
            r = min(95, r)
            _range = self.starthands[int(1326 * r / 100):]

        hand = _range[random.randint(0, len(_range) - 1)]
        while availeble(*hand):
            hand = _range[random.randint(0, len(_range) - 1)]
        return hand

    def equity(self):
        if self.chips.count(0) == 5:
            self.chips[self.runnerup] += 1

        second_equity = list()
        win_chance = [i / self.total_chips for i in self.chips]
        first_equity = [self.first * i for i in win_chance]

        for c in range(len(self.chips)):
            second_equity.append(
                sum([win_chance[i] * self.second * (self.chips[c] / (self.total_chips - self.chips[i]))
                     for i in range(len(self.chips)) if i != c])
            )
        return [round(x + y, 2) for x, y in zip(first_equity, second_equity)]

    def showdown(self):
        players = [p for p in self._all if p not in self.folded_players]
        self.chips = [0 if i == 'all' else i for i in self.chips]

        if self.raiseeq and len(players) == 1:
            self.foldequity += 1
            return

        if len(players) == 1:
            self.chips[players[0]] += sum(self.bets) + self.antepot
            self.foldequity += 1
            return

        handranks = list(range(6))
        for player in players:
            handranks[player] = self.figureHand(list(self.hands[player]) + self.deck[-5:])

        if max(handranks) == handranks[0]:
            self.winchance += 1

        # Remove Excessive chips
        ls = heapq.nlargest(2, self.bets)
        if ls[0] > ls[1]:
            self.chips[self.bets.index(max(self.bets))] += ls[0] - ls[1]
            self.bets[self.bets.index(max(self.bets))] = ls[1]

        chips = [self.bets[p] for p in players]
        # side pots
        pots = list()
        for i in range(len(set(chips))):
            low = min(chips)
            if i == 0:
                pot = sum([min(i, low) for i in self.bets]) + self.antepot
            else:
                pot = sum([min(i, low) for i in chips])
            pots.append((list(players), pot))
            chips = [i - low for i in chips]
            del players[chips.index(min(chips))]
            chips.remove(0)

        # distribute
        for pot in pots:
            hrs = [handranks[p] for p in pot[0]]
            count = hrs.count(max(hrs))
            for p in pot[0]:
                if handranks[p] == max(hrs):
                    self.chips[p] += pot[1] // count

    def figureHand(self, hand):
        p = 53
        for card in hand:
            p = self.ranks[p + card]
        return p

    def decision(self, pre, mydesc):
        self.raiseeq = 0
        # pre: range, x, p
        for p in pre:
            hand = self.random_hand(*p[:2])
            self.hands[p[2]] = hand
            self.cards_used(*hand)

        if mydesc == 1:
            self.bets[0] += self.chips[0]
            self.chips[0] = 'all'
            self.set_ebig()
        elif mydesc == 2:
            self.folded_players.append(0)
        elif mydesc == 0 and self.chips[0] > self.bb * 2:
            self.raiseeq = 1
            self.bets[0] += self.bb * 2
            self.chips[0] -= self.bb * 2
            self.set_ebig()
        else:
            return 0

        self.deck = [i for i in range(1, 53) if i not in self.used]
        np.random.shuffle(self.deck)
        for p in self.postplayers:
            index = self.postplayers.index(p)
            self.post_desc(p, self.deck[index * 2:index * 2 + 2])
        self.after_desc()

    def main(self):
        self.sort_opponents()
        pre_range = self.pre_ranges()
        choice = list()

        for desc in [(1, 2500), (2, 1000)]:
            start = int(round(time.time() * 1000))
            self.gold = 0
            equity = 0
            count = 0
            self.foldequity = 0
            self.winchance = 0
            while int(round(time.time() * 1000)) - start < desc[1]:
                self.reset_state()
                count += 1
                self.decision(pre_range, desc[0])
                self.showdown()
                equity += self.equity()[0]
            choice.append((equity / count, self.foldequity / count))

        if choice[0][0] > choice[1][0]:
            print "ALL-IN"
        else:
            print "FOLD"
        print "all-in:", choice[0][0]
        print "fold:", choice[1][0]
        print "----------------"


if __name__ == '__main__':
    state = [False]
    hp = hyper_turbo(1295, 697)
    # hp.state(100, 10, 3, [35, 50], 0, [595, 0, 850, 0, 1375, 0], [0, 0, 50, 0, 100, 0])
    # hp.main()
    while True:
        ss = scraper()
        state = ss.get_screen()
        if not state[0]:
            sleep(1.0)
        else:
            print state
            try:
                hp.state(*state)
                hp.main()
            except:
                print state
                break
            while state[0]:
                sleep(1.5)
                ss = scraper()
                state = ss.get_screen()
