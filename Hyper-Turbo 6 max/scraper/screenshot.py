import win32gui
import win32ui
import win32con
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageChops
import math
from time import sleep
import pytesseract
from pyocr import pyocr
import numpy as np
import sys
import os

def equal(img1, img2, threshold):  
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(img1.size[0] * img1.size[1]))

    # Might need to tweak the threshold.
    return rms < threshold

def string_to_number(s):
    num = [i for i in s if i.isdigit()]
    return int("".join(num))
    
class scraper:

    def __init__(self):
        self.board = list()
        self.hand = list()
        self.cardwidth = 25
        self.cardheight = 55
        self.windowtitle = self.get_window_title()
        self.clean_up()

    def get_screen(self):          
        hwnd = win32gui.FindWindow(None, self.windowtitle)
        wDC = win32gui.GetWindowDC(hwnd)
        self.dcObj=win32ui.CreateDCFromHandle(wDC)
        self.cDC=self.dcObj.CreateCompatibleDC()
        self.dataBitMap = win32ui.CreateBitmap()
        self.dataBitMap.CreateCompatibleBitmap(self.dcObj, self.cardwidth, self.cardheight)
        self.cDC.SelectObject(self.dataBitMap)
        try:
            my_turn = self.my_turn()
        except:
            my_turn = False
        if my_turn:
            if len(self.get_board()) > 0:
                my_turn = False
            else:
                self.blinds()
                self.players = self.get_players_seated()
                self.hand = self.get_hand()
                self.button = self.get_positions()
                self.stacksize = self.get_stacksize()
                self.bets = self.betsize()

        #Free Resources
        self.dcObj.DeleteDC()
        self.cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(self.dataBitMap.GetHandle())
        if my_turn:
            return self.bb, self.ante, self.players, self.hand, self.button, self.stacksize, self.bets
        else:
            return [False]

    def clean_up(self):
        for f in os.listdir('C:\Users\QQ\Dropbox\poker bot\Hyper-Turbo 2'):
            if f.endswith('.bmp'):
                try:
                    os.remove(f)
                except:
                    continue
                
    def get_board(self):
        self.board = list()
        self.cDC.BitBlt((0,0),(self.cardwidth, self.cardheight) , self.dcObj, (445,332), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'bcard1.bmp')
        self.cDC.BitBlt((0, 0),(self.cardwidth, self.cardheight) , self.dcObj, (536,332), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'bcard2.bmp')
        self.cDC.BitBlt((0, 0),(self.cardwidth, self.cardheight) , self.dcObj, (627,332), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'bcard3.bmp')
        self.cDC.BitBlt((0, 0),(self.cardwidth, self.cardheight) , self.dcObj, (718,332), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'bcard4.bmp')
        self.cDC.BitBlt((0, 0),(self.cardwidth, self.cardheight) , self.dcObj, (809,332), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'bcard5.bmp')

        for i in range(1, 6):
            im1 = Image.open("bcard%s.bmp" % (str(i)))
            for cards in range(1, 53):
                im2 = Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/%s.bmp" % (str(cards)))
                if equal(im1, im2, 8):
                    self.board.append(cards)
                    break
        return self.board

    def get_hand(self):
        hand = list()
        self.cDC.BitBlt((0,0),(self.cardwidth, self.cardheight) , self.dcObj, (586,597), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'hcard1.bmp')
        self.cDC.BitBlt((0, 0),(self.cardwidth, self.cardheight) , self.dcObj, (668,597), win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, 'hcard2.bmp')

        for i in range(1, 3):
            im1 = Image.open("hcard%s.bmp" % (str(i)))
            for cards in range(1, 53):
                im2 = Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/%s.bmp" % (str(cards)))
                if equal(im1, im2, 8):
                    hand.append(cards)
                    break
        return hand

    def create_bit_map(self, size, pos, name):
        self.dataBitMap.CreateCompatibleBitmap(self.dcObj, size[0], size[1])
        self.cDC.SelectObject(self.dataBitMap)
        self.cDC.BitBlt((0,0), size, self.dcObj, pos, win32con.SRCCOPY)
        self.dataBitMap.SaveBitmapFile(self.cDC, name)
        
    def enhance_image(self, enhance, name):
        im = Image.open(name)
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(enhance)
        return im

    def get_pot(self):
        self.create_bit_map( (180, 28), (580, 285), 'pot.bmp')
        im = Image.open('pot.bmp')
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(1)
        raw = pytesseract.image_to_string(im)
        self.pot = string_to_number(raw)
        
    def my_turn(self):
        self.create_bit_map( (53, 20), (725, 880), 'myturn.bmp')
        return equal(Image.open('C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/myturn.bmp'), Image.open('myturn.bmp'), 8)
 
    def get_active_opponents(self):
        self.create_bit_map( (40, 40), (178, 175), 'opp1_cardback.bmp')
        self.create_bit_map( (40, 40), (1170, 175), 'opp2_cardback.bmp')
        im = Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/cardback.bmp")
        im1 = Image.open("opp1_cardback.bmp")
        im2 = Image.open("opp2_cardback.bmp")
        self.active = [equal(im, im1, 50), equal(im, im2, 50)]
        
    def get_stacksize(self):
        self.create_bit_map( (100, 28), (650, 705), 'stack0.bmp')
        self.create_bit_map( (100, 28), (95, 547), 'stack1.bmp')
        self.create_bit_map( (100, 28), (95, 260), 'stack2.bmp')
        self.create_bit_map( (100, 28), (580, 150), 'stack3.bmp')
        self.create_bit_map( (100, 28), (1150, 260), 'stack4.bmp')
        self.create_bit_map( (100, 28), (1150, 547), 'stack5.bmp')
        return [self.get_number("stack%s.bmp" % (str(i)), 100, (192, 248, 181), "money") for i in range(6)]

    def get_positions(self):
        self.positions = [-1, -1, -1]
        self.create_bit_map( (45, 45), (760, 572), 'pos0.bmp')
        self.create_bit_map( (45, 45), (325, 512), 'pos1.bmp')
        self.create_bit_map( (45, 45), (284, 292), 'pos2.bmp')
        self.create_bit_map( (45, 45), (548, 205), 'pos3.bmp')
        self.create_bit_map( (45, 45), (1025, 300), 'pos4.bmp')
        self.create_bit_map( (45, 45), (969, 513), 'pos5.bmp')
        for i in range(6):
            im1 = Image.open('C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/the_button.bmp')
            im2 = Image.open('pos%s.bmp' % (str(i)))
            if equal(im1, im2, 150):
                return i

    def get_players_seated(self):
        self.create_bit_map( (30, 30), (245, 240), 'p1seated.bmp')
        self.create_bit_map( (30, 30), (245, 527), 'p2seated.bmp')
        self.create_bit_map( (30, 30), (565, 687), 'p3seated.bmp')
        self.create_bit_map( (30, 30), (735, 130), 'p4seated.bmp')
        self.create_bit_map( (30, 30), (1065, 240), 'p5seated.bmp')
        self.create_bit_map( (30, 30), (1065, 527), 'p6seated.bmp')
        return [equal(Image.open("p%sseated.bmp" % (str(i))),
                      Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/p%sseated.bmp" % (str(i))), 8) for i in range(1,7)].count(True)

    def blinds(self):
        blinds = self.windowtitle.split("Blinds ")[1].split(" ")[0].split("/")
        self.bb = int(blinds[1][1:])
        self.sb = int(blinds[0][1:])
        ante = self.windowtitle.split("Ante ")[1].split(" ")[0]
        self.ante = int(ante[1:])

    def get_number(self, name, l, color, og, tresh = 10):
        if "stack0" in name:
            color = (192, 248, 181)
            tresh = 50
            
        res = ""
        colums = list()
        im = Image.open(name)
        pixels = im.load()
        for col in range(l):
            colums.append( [pixels[col, i] for i in range(28)] )
            
        numbers = [i for i in range(len(colums)) if (color in colums[i] and color not in colums[i-1]) or
                                         ((color not in colums[i] and color in colums[i-1]))]

        for i in range(0, len(numbers), 2):
            fn = "%s%s.bmp" % (name.split(".")[0], str(i/2))
            lol = [q for q in range(28) if color in [x[q] for x in colums[numbers[i]:numbers[i+1]]]]
            im.crop((numbers[i], min(lol), numbers[i+1], max(lol))).save(fn)
            if equal(Image.open(fn), Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/allin.bmp"), 8):
                return "all"
            for a in range(10):
                im2 = Image.open("C:\Users\QQ\Documents\Hyper-Turbo\scraper\images/%s%s.bmp" % (og, str(a)))
                if equal(Image.open(fn), im2, tresh):
                    res += str(a)
                    break
        try:
            return int(res)
        except:
            return 0
                
        
    def betsize(self):
        self.create_bit_map( (220, 28), (505, 530), 'bet0.bmp')
        self.create_bit_map( (220, 28), (325, 480), 'bet1.bmp')
        self.create_bit_map( (220, 28), (345, 275), 'bet2.bmp')
        self.create_bit_map( (220, 28), (635, 220), 'bet3.bmp')
        self.create_bit_map( (220, 28), (760, 275), 'bet4.bmp')
        self.create_bit_map( (220, 28), (785, 485), 'bet5.bmp')
        return [self.get_number("bet%s.bmp" % (str(i)), 220, (221, 221, 221), "bet") for i in range(6)]
            
    
    def get_window_title(self):
        def callback(handle, data):
            titles.append(win32gui.GetWindowText(handle))
        titles = []
        win32gui.EnumWindows(callback, None)
        try: 
            return sorted([i[::-1] for i in titles if "Table" in i and "3.50" not in i])[0][::-1]
        except:
            sleep(5)
            self.get_window_title()
        

if __name__ == '__main__':
    ss = scraper()
    #print ss.get_screen() 
