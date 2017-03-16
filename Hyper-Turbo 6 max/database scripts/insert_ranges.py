import sqlite3

conn = sqlite3.connect('handranges.db')

def insert(ope, players, blinds, ante, pos, rang):
    conn.execute("INSERT OR IGNORE INTO hyper VALUES(%s, %s, %s, %s, '%s', %s)" % (ope, blinds, ante, players, pos, rang))
    conn.commit()

def check(ante, pos):
    four = conn.execute("SELECT range FROM Hypercall WHERE openpos='button' AND pos='%s' AND ante = %s AND players = 4" % (pos, ante)).fetchall()
    six = conn.execute("SELECT range FROM Hypercall WHERE openpos='button' AND pos='%s' AND ante = %s AND players = 6" % (pos, ante)).fetchall()
    return [round(four[i][0]+abs((six[i][0]-four[i][0])/2),2) for i in range(len(four))]

def update(ranges, ante, pos):
    print ranges
    for i in range(1, 26):
        conn.execute("UPDATE Hypercall set range=%s WHERE blinds = %s AND openpos='button' AND pos='%s' AND ante = %s AND players = 5"
                     % (str(ranges[i-1]), str(i), pos, str(ante) ))
        conn.commit()

##antes = ['0', '10', '13', '17', '25']
##pos = ['sb', 'bb']
##for p in pos:
##    for a in antes:
##        r = check(a, p)
##        update(r, a, p)
##        

#print check('10', 'bb')

print conn.execute("SELECT range FROM hyper WHERE players=6 AND blinds=5 AND pos='sb' AND ante=17").fetchone()[0]


##conn.execute("UPDATE Hypercall SET range=35.2 WHERE players = 6 and blinds = 5 and range = 100.0")
##conn.commit()
def call_range(openpos, pos, blinds, ante, players):
        return conn.execute("SELECT range FROM hypercall WHERE openpos='%s' AND players=%s AND blinds=%s AND pos='%s' AND ante=%s" %
                     (openpos, str(players), min(25, str(blinds)), pos, str(ante))).fetchone()

#print call_range('lojack', 'hijack', 5, 17, 6)
