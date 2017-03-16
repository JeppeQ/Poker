from __future__ import division
import eval7
from random import randint, shuffle
heads_up = [['Ao', 'Ao'], ['Ko', 'Ko'], ['Qo', 'Qo'], ['Jo', 'Jo'], ['To', 'To'], ['9o', '9o'], ['8o', '8o'], ['As', 'Ks'], ['7o', '7o'], ['As', 'Qs'], ['Ao', 'Ko'], ['As', 'Js'], ['Ao', 'Qo'], ['As', 'Ts'], ['6o', '6o'], ['Ao', 'Jo'], ['Ks', 'Qs'], ['9s', 'As'], ['Ao', 'To'], ['Js', 'Ks'], ['8s', 'As'], ['Ko', 'Qo'], ['Ks', 'Ts'], ['5o', '5o'], ['9o', 'Ao'], ['7s', 'As'], ['Jo', 'Ko'], ['Js', 'Qs'], ['Ko', 'To'], ['9s', 'Ks'], ['8o', 'Ao'], ['6s', 'As'], ['5s', 'As'], ['Qs', 'Ts'], ['7o', 'Ao'], ['4s', 'As'], ['Jo', 'Qo'], ['9o', 'Ko'], ['8s', 'Ks'], ['3s', 'As'], ['9s', 'Qs'], ['Js', 'Ts'], ['Qo', 'To'], ['4o', '4o'], ['6o', 'Ao'], ['7s', 'Ks'], ['5o', 'Ao'], ['2s', 'As'], ['6s', 'Ks'], ['4o', 'Ao'], ['8s', 'Qs'], ['8o', 'Ko'], ['9s', 'Js'], ['5s', 'Ks'], ['9o', 'Qo'], ['3o', 'Ao'], ['Jo', 'To'], ['7o', 'Ko'], ['3o', '3o'], ['4s', 'Ks'], ['2o', 'Ao'], ['7s', 'Qs'], ['9s', 'Ts'], ['6o', 'Ko'], ['3s', 'Ks'], ['8s', 'Js'], ['6s', 'Qs'], ['8o', 'Qo'], ['9o', 'Jo'], ['5o', 'Ko'], ['5s', 'Qs'], ['2s', 'Ks'], ['7s', 'Js'], ['8s', 'Ts'], ['4o', 'Ko'], ['7o', 'Qo'], ['9o', 'To'], ['8o', 'Jo'], ['4s', 'Qs'], ['2o', '2o'], ['3o', 'Ko'], ['6o', 'Qo'], ['8s', '9s'], ['3s', 'Qs'], ['6s', 'Js'], ['7s', 'Ts'], ['2o', 'Ko'], ['2s', 'Qs'], ['5o', 'Qo'], ['8o', 'To'], ['7o', 'Jo'], ['5s', 'Js'], ['4o', 'Qo'], ['6s', 'Ts'], ['4s', 'Js'], ['7s', '9s'], ['3o', 'Qo'], ['8o', '9o'], ['7o', 'To'], ['3s', 'Js'], ['7s', '8s'], ['6o', 'Jo'], ['2o', 'Qo'], ['6s', '9s'], ['2s', 'Js'], ['5s', 'Ts'], ['5o', 'Jo'], ['4s', 'Ts'], ['7o', '9o'], ['6s', '8s'], ['6o', 'To'], ['4o', 'Jo'], ['3s', 'Ts'], ['5s', '9s'], ['6s', '7s'], ['3o', 'Jo'], ['7o', '8o'], ['2s', 'Ts'], ['2o', 'Jo'], ['6o', '9o'], ['5s', '8s'], ['5o', 'To'], ['4s', '9s'], ['4o', 'To'], ['3s', '9s'], ['5s', '7s'], ['6o', '8o'], ['5s', '6s'], ['4s', '8s'], ['3o', 'To'], ['2s', '9s'], ['5o', '9o'], ['6o', '7o'], ['2o', 'To'], ['4s', '7s'], ['5o', '8o'], ['4s', '5s'], ['3s', '8s'], ['4s', '6s'], ['4o', '9o'], ['5o', '7o'], ['2s', '8s'], ['3o', '9o'], ['3s', '7s'], ['5o', '6o'], ['4o', '8o'], ['3s', '5s'], ['3s', '6s'], ['2o', '9o'], ['4o', '7o'], ['3s', '4s'], ['2s', '7s'], ['4o', '5o'], ['4o', '6o'], ['2s', '5s'], ['3o', '8o'], ['2s', '6s'], ['2o', '8o'], ['2s', '4s'], ['3o', '5o'], ['3o', '7o'], ['3o', '6o'], ['2s', '3s'], ['3o', '4o'], ['2o', '7o'], ['2o', '5o'], ['2o', '6o'], ['2o', '4o'], ['2o', '3o']]
deck = ['Ad', 'As', 'Ah', 'Ac', 'Kd', 'Ks', 'Kh', 'Kc', 'Qd', 'Qs', 'Qh', 'Qc', 'Jd', 'Js', 'Jh', 'Jc', 'Td', 'Ts', 'Th', 'Tc', '9d', '9s', '9h', '9c', '8d', '8s', '8h', '8c', '7d', '7s', '7h', '7c', '6d', '6s', '6h', '6c', '5d', '5s', '5h', '5c', '4d', '4s', '4h', '4c', '3d', '3s', '3h', '3c', '2d', '2s', '2h', '2c']
suits = ['d', 'c', 's', 'h']

def preflopchoice(cards, pos, betsize, bet, ratio = 0.75):
    playable = heads_up[:int(169*ratio)]
    if cards[0][1] == cards[1][1]:
        cards = (cards[0][0]+'s', cards[1][0]+'s')
    else:
        cards = (cards[0][0]+'o', cards[1][0]+'o')

    cards = tuple(sorted(cards))
    
    if cards in playable:
        if pos == 0:
            if bet == 1:
                return "raise"
            elif bet == 2:
                if cards in playable[:int(len(playable)*(1-betsize/10))]:
                    return "call"
                else:
                    return "fold"
        elif pos == 1:
            if betsize < 4:
                if cards in heads_up[:int(169*0.3)]:
                    return "call"
                else:
                    return "fold"
            else:
                if cards in heads_up[:int(169*0.15)]:
                    return "call"
                else:
                    return "fold"
    else:
        return "fold"

def postflopchoice(mycards, bcards, pos, betsize, bet, preratio):
    if betsize == 0:
        card_odds = cardodds(heads_up[:preratio], bcards, mycards)
        if card_odds > 0.66:
            return "raise", (pot / (1-(1-card_odds)/card_odds-0.01)) - pot
        else:
            return "call"
    else:
        card_odds = cardodds(heads_up[:preratio], bcards, mycards)
        if betsize/pot < card_odds:
            return "call"
        elif len(bcards) == 5:
            if cardouts(heads_up[:preratio], bcards, mycards) > betsize/pot:
                return "call"
            else:
                return "fold"
        else:
            return "fold"

def cardouts(oppcards, board, mycards):
    currentdeck = [i for i in deck if i not in board+mycards]
    return sum([cardodds(oppcards, board+(kort,), mycards) for kort in currentdeck])/len(currentdeck)

def cardodds(cards, board, mycards):
    win = 0
    hands = 0
    myhand = eval7.evaluate([eval7.Card(s) for s in mycards + board])
    for i in cards:
        shuffle(suits)
        if i[0][1] == 's':
            oppcard = (i[0][0]+suits[0], i[1][0]+suits[0])
        else:
            oppcard = (i[0][0]+suits[0], i[1][0]+suits[1])

        if oppcard[0] in mycards+board or oppcard[1] in mycards+board:
            continue

        elif eval7.evaluate([eval7.Card(s) for s in oppcard + board]) <= myhand:
            win += 1
        hands += 1   
    return win/hands
    
    
if __name__ == '__main__':
    print cardodds(heads_up[:95], ('Ts', 'Kc', '5h'), ('Qh', 'Jd'))
    
