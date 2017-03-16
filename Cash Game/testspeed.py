from random import shuffle
import time
import eval7
import numpy as np

def testEvaluation(num):
    start_time = time.time()
    oppcard = ['As', 'Ks']
    deck = ['Ad', 'As', 'Ah', 'Ac', 'Kd', 'Ks', 'Kh', 'Kc', 'Qd', 'Qs', 'Qh', 'Qc', 'Jd', 'Js', 'Jh', 'Jc', 'Td', 'Ts', 'Th', 'Tc', '9d', '9s', '9h', '9c', '8d', '8s', '8h', '8c', '7d', '7s', '7h', '7c', '6d', '6s', '6h', '6c', '5d', '5s', '5h', '5c', '4d', '4s', '4h', '4c', '3d', '3s', '3h', '3c', '2d', '2s', '2h', '2c']
    for i in range(num):
        np.random.shuffle(deck)
        eval7.evaluate([eval7.Card(s) for s in oppcard + deck[:5]])
    print("--- %s seconds ---" % (time.time() - start_time))

def testList(num):
    start_time = time.time()
    for i in range(num):
        a = [2, 2, 2, 2, 2]
        b = [3, 3, 3, 3, 3]
        c = [x+y for x,y in zip(a, b)]
    print("--- %s seconds ---" % (time.time() - start_time))
    

if __name__ == '__main__':
    testEvaluation(10000)
