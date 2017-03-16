import win32api, win32con, win32clipboard
from time import sleep
import sqlite3

conn = sqlite3.connect('handranges.db')

def insert(ope, players, blinds, ante, pos, rang):
    conn.execute("INSERT OR IGNORE INTO hypercall VALUES('%s', %s, %s, %s, '%s', %s)" % (ope, blinds, ante, players, pos, rang))
    conn.commit()

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def drag(x, y, x1, y2):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.SetCursorPos((x1,y2))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x1,y2,0,0)
    
def get_range():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()[:50]
    win32clipboard.CloseClipboard()
    click(810, 1050)
    sleep(1)
    return data.split("%")[0].split(" ")[-1]

def calculate():
    click(900, 1010)
    sleep(2)
    
def blinds(b):
    if b == 1:
        click(650, 355)
    else:
        drag(632+25*(b-1), 360, 632+25*b, 360)
    sleep(0.5)

def pos(p, y, l):
    if p == 0:
        click(730, y)
    elif p == 1:
        if l == 4:
            click(1200, y)
        else:
            click(965, y)
    elif p == 2:
        click(1200, y)
    elif p == 3:
        click(730, y+50)
    elif p == 4:
        click(1200, y+50)
    sleep(0.5)

def ante(a):
    click(730+110*a, 250)
    sleep(0.5)

def pp(p):
    click(1200, 150)
    sleep(1)
    click(730+110*(5-p), 210)
    sleep(1)

def getcp(p, n):
    if p > 4:
        if n == 5:
            return [(730, 630), (965, 630), (1200, 630), (730, 680), (1200, 680)]
        elif n == 4:
            return [(730, 630), (1200, 630), (730, 680), (1200, 680)]
        elif n == 3:
            return [(730, 630), (965, 630), (1200, 630)]
        elif n == 2:
            return [(730, 630), (1200, 630)]
        elif n == 1:
            return [(730, 630)]
    else:
        if n == 3:
            return [(730, 580), (965, 580), (1200, 580)]
        elif n == 2:
            return [(730, 580), (1200, 580)]
        elif n == 1:
            return [(730, 580)] 

def getpositions(n):
    if n == 6:
        return [(730, 480), (965, 480), (1200, 480), (730, 530), (1200, 530)]
    elif n == 5:
        return [(730, 480), (1200, 480), (730, 530), (1200, 530)]
    elif n == 4:
        return [(730, 480), (965, 480), (1200, 480)]
    elif n == 3:
        return [(730, 480), (1200, 480)]
    elif n == 2:
        return [(730, 480)]
    
pos_names = ['lojack', 'hijack', 'cutoff', 'button', 'sb']
cp_names = ['hijack', 'cutoff', 'button', 'sb', 'bb']
ante_values = [0, 10, 13, 17, 25]

for i in reversed(range(2, 7)):
    if i != 6:
        pp(i)
    pos = getpositions(i)
    for p in range(len(pos)):
        click(*pos[p])
        sleep(0.5)
        cp = getcp(i, len(pos)-p)
        for x in range(len(cp)):
            click(*cp[x])
            sleep(0.5)
            for a in range(0, 5):
                ante(a)
                for b in range(1, 26):
                    blinds(b)
                    calculate()
                    win = get_range()
                    print pos_names[-i+1:][p], i, cp_names[-len(pos)+p:][x], ante_values[a], b, win
                    insert(pos_names[-i+1:][p], i, str(b), str(ante_values[a]), cp_names[-len(pos)+p:][x], str(win))




