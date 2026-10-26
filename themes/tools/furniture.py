"""rev3: themed furniture / architecture / capsule accessories. All original pixel art by @designer.
Cell = 2 css px. Sizes (css) equal the ref display sizes used by plugin.js v5:
 desk 140.5x73.9 -> 70x37 | chair 63.3x100.8 -> 32x50 | monitor 63x51.7 -> 32x26 | keyboard 52.6x14 -> 26x7
 elevatorFrame 154.4x144.3 -> 77x72 | elevatorDoor 50.8x123.5 -> 25x62 | floor tile 100x100 -> 50x50
 wall tile 128x240 -> 64x120 (repeat-x, y 0..240) | trim 64x10 -> 32x5 (repeat-x, y 240..250)
 capsule accessory 56x48 css box -> 28x24 cells, top-left at capsule centre + (-28,-56) (capsule top edge = cell row 8)
"""
import math
from px import C, OUT, dk, lt, mix
from props2 import emblem, glow

# ----------------------------------------------------------------- materials per theme
M = {
 'default':  dict(top='#3a3d4a', body='#2a2c35', leg='#23252d', edge='#a855f7', grain='plate', chair='mecha', seat='#2e3040', trimc='#a855f7',
                  mon='#34374a', monled='#a855f7', kb='#2a2c35', key='#4a4e60', keyacc='#ff2d3d', door='#3b3e4a', doorstyle='blast', frame='#2a2c35', light2='#ff2d3d',
                  floor=('#1d1e25', '#262833', '#2f3240'), floorstyle='deck', wall=('#1f1f27', '#262733', '#2d2f3c'), wallstyle='steel', trim=('#f0c419', '#1a1a1a'), trimstyle='hazard'),
 'coder':    dict(top='#1e2326', body='#15191c', leg='#2a3036', edge='#39ff9c', grain='carbon', chair='gaming', seat='#1a1f22', seatacc='#39ff9c', trimc='#39ff9c',
                  mon='#15191c', monled='rgb', kb='#111416', key='#262c30', keyacc='rgb', door='#1c2226', doorstyle='neon', frame='#161b1e', light2='#2ee6e6',
                  floor=('#181d1f', '#20272a', '#283034'), floorstyle='raised', wall=('#1b2123', '#20282a', '#263033'), wallstyle='cables', trim=('#39ff9c', '#10201a'), trimstyle='neon'),
 'designer': dict(top='#6e655c', body='#4a433d', leg='#d9a3c3', edge='#f5a8c8', grain='lightwood', chair='office', seat='#6b5a78', trimc='#f5a8c8',
                  mon='#8a8279', monled='#f5a8c8', kb='#6e675f', key='#b8b0a6', keyacc='#bdb2ff', door='#6b5a78', doorstyle='pastel', frame='#3a3040', light2='#bdb2ff',
                  floor=('#232126', '#2a282e', '#312e35'), floorstyle='concrete', wall=('#2a2530', '#322a38', '#3a3040'), wallstyle='brick', trim=('#d9a3c3', '#3a2c3c'), trimstyle='line'),
 'content':  dict(top='#7a4a26', body='#5e3a1e', leg='#4a2c16', edge='#e0a060', grain='wood', chair='wood', seat='#7a2f2a', trimc='#e0a060',
                  mon='#c9bfa3', monled='#e0a060', kb='#bdb398', key='#e8dfc8', keyacc='#a8452f', door='#6b4423', doorstyle='woodbrass', frame='#4a2e18', light2='#e0a060',
                  floor=('#2a2019', '#33281f', '#3c2f24'), floorstyle='parquet', wall=('#2e2721', '#362d25', '#3e3329'), wallstyle='panel', trim=('#8a5a30', '#2a1a0c'), trimstyle='wood'),
 'video':    dict(top='#1c1a20', body='#131116', leg='#2a2632', edge='#b36bff', grain='matte', chair='office', seat='#2a2236', trimc='#b36bff',
                  mon='#1c1a20', monled='bars', kb='#141217', key='#2e2a36', keyacc='#b36bff', door='#18161c', doorstyle='onair', frame='#131116', light2='#ff3b3b',
                  floor=('#141317', '#1a181e', '#211f26'), floorstyle='tape', wall=('#221c2c', '#2a2236', '#322840'), wallstyle='foam', trim=('#b36bff', '#1a1224'), trimstyle='line'),
 'analyst':  dict(top='#2a3a52', body='#1c2638', leg='#3a4a64', edge='#4da3ff', grain='glass', chair='office', seat='#1f3350', trimc='#4da3ff',
                  mon='#1d2636', monled='#4da3ff', kb='#1d2636', key='#34425a', keyacc='#4da3ff', door='#3a4a64', doorstyle='steelblue', frame='#1c2638', light2='#4da3ff',
                  floor=('#171c26', '#1c2230', '#222939'), floorstyle='carpetgrid', wall=('#1f2634', '#243044', '#2a364c'), wallstyle='navy', trim=('#4da3ff', '#101a2a'), trimstyle='line'),
 'research': dict(top='#5a3a22', body='#432a18', leg='#321f10', edge='#c9a55a', grain='oak', chair='wood', seat='#2f5d3a', trimc='#c9a55a',
                  mon='#2a2a26', monled='crt', kb='#3a3830', key='#5a574a', keyacc='#c9a55a', door='#c9a55a', doorstyle='cage', frame='#3a2616', light2='#c9a55a',
                  floor=('#1f1a14', '#272019', '#2f271e'), floorstyle='herringbone', wall=('#1f2a22', '#243228', '#2a3a2e'), wallstyle='greenwood', trim=('#6b4a30', '#1f140c'), trimstyle='wood'),
 'qa':       dict(top='#6a7078', body='#4a5058', leg='#3a3f45', edge='#3ecf6e', grain='steel', chair='stool', seat='#e5484d', trimc='#e5484d',
                  mon='#3a3f45', monled='#3ecf6e', kb='#2c3035', key='#50565e', keyacc='#e5484d', door='#5a6068', doorstyle='steel', frame='#2c3035', light2='#3ecf6e',
                  floor=('#1d1e20', '#242528', '#2c2d31'), floorstyle='labtile', wall=('#26262a', '#2e2e33', '#36363c'), wallstyle='labtile', trim=('#3ecf6e', '#e5484d'), trimstyle='split'),
 'ops':      dict(top='#4a4640', body='#35322e', leg='#2a2724', edge='#ff8a1f', grain='diamond', chair='office', seat='#3a3531', trimc='#ff8a1f',
                  mon='#2b2724', monled='rack', kb='#232120', key='#3e3a35', keyacc='#ff8a1f', door='#4a4640', doorstyle='freight', frame='#2b2724', light2='#ff8a1f',
                  floor=('#1d1b19', '#25221f', '#2e2a26'), floorstyle='diamond', wall=('#28231f', '#302923', '#382f28'), wallstyle='indbrick', trim=('#f0c419', '#1a1a1a'), trimstyle='hazard'),
 'pm':       dict(top='#9a8266', body='#3a4040', leg='#5a6468', edge='#2ec4b6', grain='lightwood', chair='office', seat='#1f4a47', trimc='#2ec4b6', standing=True,
                  mon='#253333', monled='#2ec4b6', kb='#253333', key='#3e5050', keyacc='#2ec4b6', door='#2a4a48', doorstyle='teal', frame='#1a2b2b', light2='#2ec4b6',
                  floor=('#172020', '#1c2727', '#222e2e'), floorstyle='carpet', wall=('#1c2929', '#213232', '#273a3a'), wallstyle='glass', trim=('#2ec4b6', '#0e2222'), trimstyle='line'),
 'growth':   dict(top='#4a5238', body='#343a28', leg='#2a2f22', edge='#a3e635', grain='modern', chair='office', seat='#3a4428', trimc='#a3e635',
                  mon='#2a2f22', monled='#a3e635', kb='#232820', key='#3e4634', keyacc='#a3e635', door='#3e4634', doorstyle='olive', frame='#232820', light2='#a3e635',
                  floor=('#1c1a16', '#23201b', '#2a2620'), floorstyle='planks', wall=('#232820', '#2a3026', '#31382c'), wallstyle='olive', trim=('#a3e635', '#1a2210'), trimstyle='neon'),
}
RGB = ['#ff3b5c', '#ff9f1c', '#ffe14d', '#39ff9c', '#2ee6e6', '#3b82ff', '#b04dff']

# ----------------------------------------------------------------- desk 70x37
def desk(t):
    m = M[t]; c = C(70, 37); top, body, leg = m['top'], m['body'], m['leg']
    standing = m.get('standing')
    # legs (behind panel), then modesty panel, then top slab
    if standing:
        for x in (4, 63): c.r(x, 15, 3, 22, leg); c.r(x, 15, 1, 22, lt(leg, .3)); c.r(x-2, 35, 7, 2, dk(leg, .3))
    else:
        for x in (2, 65): c.r(x, 15, 3, 22, leg); c.r(x, 15, 1, 22, lt(leg, .25)); c.r(x+2, 15, 1, 22, dk(leg, .35))
    if not standing:
        c.r(5, 16, 60, 14, body); c.r(5, 16, 60, 1, dk(body, .45)); c.r(6, 18, 58, 10, mix(body, top, .15)); c.ol(6, 18, 58, 10, dk(body, .3))
        for x in (6, 62): c.r(x, 29, 2, 3, dk(leg, .2))
    # top slab: 0..12 surface, 12..15 front lip
    c.r(1, 0, 68, 12, top)
    g = m['grain']
    if g in ('wood', 'oak', 'lightwood'):
        gc = dk(top, .18) if g != 'lightwood' else dk(top, .1)
        for i, y in enumerate(range(2, 11, 2)):
            x0 = (i*17) % 23; c.r(2+x0, y, 18 + (i*5) % 9, 1, gc); c.r(34+(i*11) % 17, y+ (1 if i % 2 else 0), 14, 1, gc)
        if g == 'oak':
            c.ring(52, 6, 2, dk(top, .25)); c.p(52, 6, dk(top, .3))
    elif g == 'plate':
        c.r(1, 5, 68, 1, dk(top, .3)); c.r(34, 0, 1, 12, dk(top, .3))
        for (x, y) in [(3, 2), (31, 2), (37, 2), (66, 2), (3, 8), (31, 8), (37, 8), (66, 8)]: c.p(x, y, lt(top, .35))
        c.r(8, 9, 20, 1, lt(top, .12))
    elif g == 'carbon':
        for y in range(1, 12):
            for x in range(1, 69):
                if (x + y*2) % 4 == 0: c.p(x, y, lt(top, .07))
    elif g == 'glass':
        c.r(1, 0, 68, 12, mix(top, '#6fa8e8', .15))
        for k in range(3): c.line(10+k*20, 11, 18+k*20, 1, lt(top, .3))
    elif g == 'steel':
        for y in range(1, 12, 3): c.r(2, y, 66, 1, lt(top, .1))
        for (x, y) in [(3, 2), (66, 2), (3, 9), (66, 9)]: c.p(x, y, dk(top, .4))
    elif g == 'diamond':
        for y in range(1, 12, 3):
            for x in range(2 + (y % 2)*2, 68, 5): c.r(x, y, 2, 1, lt(top, .16))
    elif g == 'matte':
        c.r(1, 1, 68, 1, lt(top, .1))
    elif g == 'modern':
        c.r(1, 0, 68, 3, lt(top, .08)); c.r(20, 6, 30, 1, lt(top, .1))
    c.r(1, 0, 68, 1, lt(top, .25))
    c.r(0, 12, 70, 3, dk(top, .25)); c.r(0, 12, 70, 1, dk(top, .1))
    if m['edge']: c.r(1, 14, 68, 1, m['edge'])                      # accent list on the front edge
    if t == 'default':
        for x in range(4, 66, 12): c.r(x, 13, 2, 1, '#ff2d3d')
    c.outline_alpha(); return c

# ----------------------------------------------------------------- chair 32x50
def chair(t):
    m = M[t]; c = C(32, 50); s = m['seat']; kind = m['chair']; acc = m.get('seatacc', m['trimc'])
    metal = '#2a2d33'
    def base(col=metal):
        c.r(15, 30, 3, 9, col); c.r(15, 30, 1, 9, lt(col, .3))
        for (x0, x1, y1) in [(16, 4, 44), (16, 28, 44), (16, 9, 41), (16, 23, 41), (16, 16, 46)]:
            c.line(x0, 38, x1, y1, col, 2)
        for (x, y) in [(3, 45), (28, 45), (15, 47)]: c.r(x, y, 3, 3, '#15161a'); c.p(x+1, y, '#555')
    if kind == 'stool':
        c.r(15, 22, 3, 18, '#6a7078'); c.r(15, 22, 1, 18, '#9aa3ad'); c.ell(16, 21, 11, 4, s); c.r(6, 19, 21, 1, lt(s, .3))
        c.ring(16, 34, 6, '#6a7078'); base('#6a7078'); c.outline_alpha(); return c
    if kind == 'wood':
        w = m['leg']
        c.r(7, 0, 18, 18, w); c.r(9, 2, 14, 14, dk(w, .2))
        for x in range(11, 22, 4): c.r(x, 2, 2, 14, lt(w, .15))                   # spindles
        c.r(7, 0, 18, 2, lt(w, .25))
        c.r(5, 18, 22, 7, s); c.r(5, 18, 22, 1, lt(s, .3)); c.r(5, 24, 22, 2, dk(w, .1))
        for x in (6, 24): c.r(x, 25, 2, 23, w); c.r(x, 25, 1, 23, lt(w, .2))
        c.r(8, 38, 16, 1, w)
        c.outline_alpha(); return c
    if kind == 'mecha':
        g = '#3a3d4a'
        c.r(8, 0, 16, 18, g); c.r(6, 3, 2, 13, '#2a2c35'); c.r(24, 3, 2, 13, '#2a2c35')
        c.r(10, 2, 12, 5, '#23252d'); c.r(12, 4, 8, 1, '#ff2d3d'); c.p(13, 4, '#ffc0c8')        # red optic slit
        for y in range(8, 16, 2): c.r(10, y, 12, 1, dk(g, .25))
        c.r(10, 16, 12, 1, '#a855f7')
        c.r(4, 15, 4, 6, '#2a2c35'); c.r(24, 15, 4, 6, '#2a2c35')
        c.r(6, 19, 20, 6, s); c.r(6, 19, 20, 1, lt(s, .3)); c.r(8, 23, 16, 1, '#a855f7')
        base('#23252d'); glow(c, '#a855f7', 1) if False else None
        c.outline_alpha(); return c
    # office / gaming
    tall = kind == 'gaming'
    by = 0 if tall else 2
    c.r(8, by, 16, 17 - by, s); c.r(9, by+1, 14, 1, lt(s, .25))
    c.r(8, by, 1, 17-by, lt(s, .12)); c.r(23, by, 1, 17-by, dk(s, .3))
    c.r(11, by+3, 10, 11-by, lt(s, .06))
    if tall:
        c.r(6, 2, 2, 12, s); c.r(24, 2, 2, 12, s)                                        # wings
        c.r(10, 1, 2, 15, acc); c.r(20, 1, 2, 15, acc)                                    # racing stripes
        c.r(12, 3, 8, 3, dk(s, .3))                                                       # headrest cushion
    c.r(15, 17, 2, 2, '#2a2d33')
    c.r(4, 15, 4, 2, '#2a2d33'); c.r(4, 17, 2, 5, '#2a2d33'); c.r(24, 15, 4, 2, '#2a2d33'); c.r(26, 17, 2, 5, '#2a2d33')
    c.r(6, 19, 20, 7, s); c.r(6, 19, 20, 1, lt(s, .3)); c.r(6, 25, 20, 1, dk(s, .35))
    if tall: c.r(7, 22, 18, 1, acc)
    base(); c.outline_alpha(); return c

# ----------------------------------------------------------------- monitor 32x26 (back view)
def monitor(t):
    m = M[t]; c = C(32, 26); sh = m['mon']; led = m['monled']
    if led == 'crt':                                                        # research: deep CRT back
        c.r(3, 0, 26, 20, sh); c.r(6, 2, 20, 15, dk(sh, .2)); c.r(3, 0, 26, 1, lt(sh, .25))
        for y in range(4, 15, 2): c.r(9, y, 14, 1, dk(sh, .4))                 # vents
        c.r(3, 18, 26, 2, '#33ff66' if False else dk(sh, .3)); c.r(26, 16, 2, 2, '#33ff66')
        c.r(11, 20, 10, 3, dk(sh, .1)); c.r(8, 23, 16, 3, sh)
        c.outline_alpha(); return c
    c.r(0, 0, 32, 19, sh); c.r(0, 0, 32, 1, lt(sh, .25)); c.r(0, 0, 1, 19, lt(sh, .15)); c.r(31, 0, 1, 19, dk(sh, .3))
    c.r(4, 2, 24, 11, lt(sh, .08)); c.ol(4, 2, 24, 11, dk(sh, .25))              # recessed back panel
    c.r(13, 13, 6, 6, dk(sh, .2)); c.r(13, 19, 6, 4, sh); c.r(13, 19, 1, 4, lt(sh, .2)); c.r(8, 23, 16, 3, sh); c.r(8, 23, 16, 1, lt(sh, .2))
    for x in (6, 8, 23): c.r(x, 15, 1, 1, dk(sh, .5))
    if led == 'rgb':
        for x in range(1, 31): c.p(x, 18, RGB[(x*7)//31])
        c.r(6, 5, 20, 1, '#39ff9c')
    elif led == 'bars':
        for i, col in enumerate(['#f2f2f2', '#ffe14d', '#2ee6e6', '#39ff9c', '#ff3bd4', '#ff3b3b', '#3b82ff']): c.r(6+i*3, 15, 3, 2, col)
    elif led == 'rack':
        c.r(0, 3, 2, 13, '#4a4640'); c.r(30, 3, 2, 13, '#4a4640'); c.p(0, 5, '#111'); c.p(31, 5, '#111'); c.p(0, 13, '#111'); c.p(31, 13, '#111')
        c.r(24, 15, 2, 2, '#ff8a1f'); c.r(21, 15, 2, 2, '#3ecf6e')
    else:
        c.r(1, 17, 30, 1, led); c.r(27, 15, 2, 1, led)
    if t == 'default':
        emblem(c, 11, 3, dk(sh, .4) if False else '#4a4e60', '#ff2d3d')
    if t == 'content':
        c.r(12, 4, 8, 6, dk(sh, .15)); c.r(3, 0, 26, 1, lt(sh, .35))
    c.outline_alpha(); return c

# ----------------------------------------------------------------- keyboard 26x7 (back view, keys visible)
def keyboard(t):
    m = M[t]; c = C(26, 7); b, k, a = m['kb'], m['key'], m['keyacc']
    c.r(0, 0, 26, 7, b); c.r(0, 0, 26, 1, lt(b, .2)); c.r(0, 6, 26, 1, dk(b, .3))
    for row in range(3):
        for i in range(11 - (row % 2)):
            x = 1 + i*2 + (row % 2); col = k
            if a == 'rgb': col = RGB[(i + row*2) % len(RGB)]
            elif (row, i) in ((0, 0), (2, 9), (1, 4)): col = a
            c.p(x, 1 + row*2, col)
    c.r(8, 5, 10, 1, k if a != 'rgb' else '#39ff9c')
    if a == 'rgb': c.r(0, 6, 26, 1, '#2ee6e6')
    c.outline_alpha(); return c

# ----------------------------------------------------------------- elevator frame 77x72 + door 25x62
def elevator_frame(t):
    m = M[t]; c = C(77, 72); f = m['frame']; st = m['doorstyle']; acc = m['trimc']
    c.r(0, 0, 77, 72, f)
    c.r(0, 0, 77, 1, lt(f, .3)); c.r(0, 0, 2, 72, lt(f, .15)); c.r(75, 0, 2, 72, dk(f, .35))
    c.r(8, 9, 61, 63, dk(f, .45)); c.r(12, 10, 53, 62, '#0b0b0e')                      # jamb + dark shaft
    c.r(13, 12, 51, 1, '#1a1a20'); c.r(13, 40, 51, 1, '#15151a')
    c.r(9, 9, 3, 63, lt(f, .1)); c.r(65, 9, 3, 63, dk(f, .2))
    c.r(33, 1, 11, 7, '#0a0a0c')                                                        # slot for plugin indicator light (81..91,111..119 world)
    if st == 'blast':
        for x in range(2, 75, 4): c.line(x, 8, x+3, 1, '#f0c419'); c.line(x+1, 8, x+4, 1, '#f0c419')
        c.r(2, 1, 75, 1, f); c.r(31, 0, 15, 9, f); c.r(33, 1, 11, 7, '#0a0a0c')
        for y in range(12, 70, 8): c.r(3, y, 3, 3, '#ff2d3d'); c.r(71, y, 3, 3, '#a855f7')
        emblem(c, 3, 0, '#4a4e60', '#ff2d3d') if False else None
    elif st == 'neon':
        c.r(8, 9, 1, 63, acc); c.r(68, 9, 1, 63, acc); c.r(8, 8, 61, 1, acc); c.r(4, 3, 26, 2, '#12181b'); c.r(47, 3, 26, 2, '#12181b')
        for x in range(5, 29, 3): c.p(x, 3, '#39ff9c')
    elif st == 'woodbrass':
        for x in range(2, 75, 6): c.r(x, 1, 1, 71, dk(f, .2))
        c.r(8, 8, 61, 2, '#c9a55a'); c.r(7, 9, 2, 63, '#c9a55a'); c.r(68, 9, 2, 63, '#c9a55a')
        c.circ(20, 4, 3, '#c9a55a'); c.circ(57, 4, 3, '#c9a55a'); c.p(20, 4, '#4a2e18'); c.p(57, 4, '#4a2e18')
    elif st == 'cage':
        c.r(7, 8, 63, 2, '#c9a55a'); c.r(6, 9, 3, 63, '#a8884a'); c.r(68, 9, 3, 63, '#a8884a')
        for x in range(3, 31, 5): c.ring(x+2, 4, 2, '#c9a55a')
        for x in range(46, 74, 5): c.ring(x+2, 4, 2, '#c9a55a')
    elif st == 'onair':
        c.r(4, 2, 24, 6, '#2a0a0e'); c.txt(6, 3, 'ON AIR', '#ff3b3b'); c.ol(4, 2, 24, 6, '#ff3b3b')
        c.r(8, 9, 1, 63, acc)
    elif st == 'freight':
        for x in range(0, 77, 6): c.line(x, 8, x+5, 1, '#f0c419')
        c.r(31, 0, 15, 9, f); c.r(33, 1, 11, 7, '#0a0a0c')
        for y in range(10, 72, 6): c.r(2, y, 5, 3, '#f0c419'); c.r(70, y+3, 5, 3, '#f0c419')
    elif st == 'steel':
        c.r(4, 3, 4, 3, '#3ecf6e'); c.r(69, 3, 4, 3, '#e5484d'); c.r(8, 8, 61, 1, lt(f, .3))
    else:  # pastel / steelblue / teal / olive: coloured jamb + small accent lamps
        c.r(8, 8, 61, 1, acc); c.r(7, 9, 1, 63, acc); c.r(69, 9, 1, 63, acc)
        c.r(6, 3, 20, 2, dk(acc, .5)); c.r(51, 3, 20, 2, dk(acc, .5))
    c.outline_alpha(); return c

def elevator_door(t):
    m = M[t]; c = C(25, 62); d = m['door']; st = m['doorstyle']; acc = m['trimc']
    if st == 'cage':                                                          # folding brass gate (lattice, see-through)
        for x in range(0, 25, 4): c.r(x, 0, 1, 62, d); c.r(x, 0, 1, 62, d)
        for y in range(0, 62, 6):
            for x in range(0, 24, 4): c.line(x, y, x+4, y+6, dk(d, .15)); c.line(x+4, y, x, y+6, dk(d, .15))
        c.r(0, 0, 25, 2, d); c.r(0, 60, 25, 2, d); c.r(0, 30, 25, 1, lt(d, .2))
        return c
    c.r(0, 0, 25, 62, d); c.r(0, 0, 25, 1, lt(d, .25)); c.r(0, 0, 1, 62, lt(d, .15)); c.r(24, 0, 1, 62, dk(d, .35))
    if st == 'blast':
        c.r(2, 2, 21, 58, dk(d, .12)); c.ol(2, 2, 21, 58, dk(d, .35))
        for y in range(40, 58, 1):
            for x in range(2, 23):
                if ((x + y) // 3) % 2 == 0: c.p(x, y, '#f0c419')
                else: c.p(x, y, '#1a1a1a')
        for y in (6, 20, 34): c.r(4, y, 17, 2, dk(d, .35)); c.r(4, y, 17, 1, lt(d, .2))
        for (x, y) in [(3, 3), (21, 3), (3, 38), (21, 38)]: c.p(x, y, lt(d, .45))
        c.r(10, 12, 5, 2, '#a855f7'); c.r(23, 0, 2, 62, '#a855f7')
    elif st == 'neon':
        c.r(3, 3, 19, 56, dk(d, .25)); c.r(23, 0, 1, 62, '#39ff9c'); c.r(3, 3, 1, 56, '#1f3a30')
        for y in range(8, 56, 8): c.r(5, y, 15, 1, lt(d, .08))
        c.r(18, 28, 2, 6, '#2ee6e6')
    elif st == 'woodbrass':
        for x in range(2, 24, 4): c.r(x, 1, 1, 60, dk(d, .18))
        c.ol(3, 4, 19, 24, '#c9a55a'); c.ol(3, 33, 19, 24, '#c9a55a'); c.r(20, 29, 3, 3, '#c9a55a')
    elif st == 'onair':
        c.r(3, 3, 19, 56, lt(d, .04)); c.r(23, 0, 2, 62, '#b36bff')
        c.r(6, 26, 13, 1, '#2a2632')
    elif st == 'freight':
        for y in range(1, 62, 7): c.r(1, y, 23, 1, lt(d, .15)); c.r(1, y+1, 23, 1, dk(d, .2))
        for y in range(52, 61):
            for x in range(1, 24):
                c.p(x, y, '#f0c419' if ((x + y) // 3) % 2 else '#1a1a1a')
    elif st == 'steel':
        for y in range(2, 60, 3): c.r(2, y, 21, 1, lt(d, .08))
        c.r(10, 28, 4, 6, dk(d, .3)); c.r(23, 0, 1, 62, lt(d, .35))
    elif st == 'steelblue':
        c.r(3, 3, 19, 56, lt(d, .06)); c.line(4, 55, 20, 5, lt(d, .2)); c.r(23, 0, 1, 62, '#4da3ff')
    else:  # pastel / teal / olive
        c.r(3, 3, 19, 56, lt(d, .08)); c.ol(3, 3, 19, 56, dk(d, .25)); c.r(23, 0, 1, 62, acc); c.r(5, 30, 15, 1, acc)
    c.ol(0, 0, 25, 62, OUT)
    return c

# ----------------------------------------------------------------- floor tile 50x50 (rendered at 2px/cell = 100px)
def floor_tile(t):
    m = M[t]; a, b, h = m['floor']; st = m['floorstyle']; c = C(50, 50); c.r(0, 0, 50, 50, b)
    if st == 'deck':
        for (x0, y0) in [(0, 0), (25, 0), (0, 25), (25, 25)]:
            c.r(x0, y0, 25, 25, b if (x0 + y0) % 50 == 0 else a); c.r(x0, y0, 25, 1, h); c.r(x0, y0, 1, 25, h)
            c.r(x0, y0+24, 25, 1, dk(a, .35)); c.r(x0+24, y0, 1, 25, dk(a, .35))
            for (dx, dy) in [(3, 3), (21, 3), (3, 21), (21, 21)]: c.p(x0+dx, y0+dy, lt(h, .2)); c.p(x0+dx+1, y0+dy+1, dk(a, .4))
        c.r(10, 24, 30, 2, '#2a1f3a')                                  # purple seam glow line (subtle)
    elif st == 'raised':
        for (x0, y0) in [(0, 0), (25, 0), (0, 25), (25, 25)]:
            c.r(x0, y0, 25, 25, b); c.r(x0, y0, 25, 1, h); c.r(x0, y0, 1, 25, h); c.r(x0, y0+24, 25, 1, dk(a, .4)); c.r(x0+24, y0, 1, 25, dk(a, .4))
            if (x0 + y0) % 50 == 0:
                for y in range(y0+4, y0+22, 3):
                    for x in range(x0+4, x0+22, 3): c.p(x, y, dk(a, .35))
    elif st == 'concrete':
        c.r(0, 0, 50, 50, b)
        for i in range(90): c.p((i*37) % 50, (i*23) % 50, h if i % 3 else a)
        c.r(0, 0, 50, 1, dk(a, .2)); c.r(0, 0, 1, 50, dk(a, .2))
    elif st in ('parquet', 'planks'):
        pw = 5 if st == 'parquet' else 8
        for i, y in enumerate(range(0, 50, pw)):
            col = [a, b, h][i % 3]; c.r(0, y, 50, pw, col); c.r(0, y, 50, 1, dk(a, .3))
            off = (i*17) % 50; c.r(off, y, 1, pw, dk(a, .3)); c.r((off+25) % 50, y, 1, pw, dk(a, .3))
            c.r((off+6) % 50, y+2, 8, 1, lt(col, .06))
    elif st == 'tape':
        c.r(0, 0, 50, 50, a)
        for i in range(40): c.p((i*31) % 50, (i*17) % 50, b)
        c.r(0, 46, 50, 2, '#6a5a2a')                                    # yellow floor-marking tape (dim)
        c.r(46, 0, 2, 50, '#3a3346')
    elif st in ('carpetgrid', 'carpet'):
        for y in range(50):
            for x in range(50):
                if (x*7 + y*13) % 5 == 0: c.p(x, y, a)
                elif (x*3 + y*5) % 11 == 0: c.p(x, y, h)
        if st == 'carpetgrid':
            c.r(0, 0, 50, 1, mix(h, '#4da3ff', .15)); c.r(0, 0, 1, 50, mix(h, '#4da3ff', .15)); c.r(0, 25, 50, 1, h); c.r(25, 0, 1, 50, h)
    elif st == 'herringbone':
        c.r(0, 0, 50, 50, a)
        for k in range(-50, 100, 10):
            for i in range(0, 60):
                x = k + i; y = i
                if 0 <= x < 50 and 0 <= y < 50 and (i // 5) % 2 == 0: c.r(x, y, 5, 1, b if (k // 10) % 2 else h)
        for y in range(0, 50, 5): c.r(0, y, 50, 1, dk(a, .25))
    elif st == 'labtile':
        for (x0, y0) in [(0, 0), (25, 0), (0, 25), (25, 25)]:
            c.r(x0, y0, 25, 25, b if (x0 + y0) % 50 else a); c.r(x0, y0, 25, 1, dk(a, .3)); c.r(x0, y0, 1, 25, dk(a, .3)); c.r(x0+1, y0+1, 23, 1, h)
    elif st == 'diamond':
        c.r(0, 0, 50, 50, b)
        for y in range(1, 50, 5):
            for x in range(1 + ((y // 5) % 2)*3, 50, 6): c.r(x, y, 3, 1, h); c.p(x+1, y+1, dk(a, .2))
        c.r(0, 0, 50, 1, dk(a, .35)); c.r(0, 0, 1, 50, dk(a, .35))
    return c

# ----------------------------------------------------------------- wall tile 64x120 + trim 32x5
def wall_tile(t):
    m = M[t]; a, b, h = m['wall']; st = m['wallstyle']; c = C(64, 120); c.r(0, 0, 64, 120, b)
    if st == 'steel':
        for x0 in (0, 32):
            c.r(x0, 0, 32, 120, b if x0 == 0 else mix(a, b, .5)); c.r(x0, 0, 1, 120, h); c.r(x0+31, 0, 1, 120, dk(a, .35))
            for y in range(0, 120, 30):
                c.r(x0, y, 32, 1, dk(a, .35))
                for dx in (3, 28): c.p(x0+dx, y+3, lt(h, .15)); c.p(x0+dx, y+26, lt(h, .15))
        c.r(0, 100, 64, 2, dk(a, .4)); c.r(0, 102, 64, 1, '#3a2a55')
    elif st == 'cables':
        for x0 in (0, 32):
            c.r(x0, 0, 1, 120, dk(a, .3)); c.r(x0+1, 0, 1, 120, h)
        for x, col in [(10, '#1d3a30'), (13, '#2a2f36'), (47, '#1d3a30'), (50, '#30283a')]:
            c.r(x, 0, 2, 120, col); c.r(x, 0, 1, 120, lt(col, .15))
        for y in range(10, 120, 28): c.r(8, y, 8, 3, '#11161a'); c.p(9, y+1, '#39ff9c')
    elif st == 'brick':
        for r in range(0, 120, 6):
            off = 0 if (r // 6) % 2 == 0 else 8
            for x in range(-16 + off, 64, 16):
                col = [a, b, h][((x + r) // 16) % 3]; c.r(x+1, r+1, 15, 5, col)
            c.r(0, r, 64, 1, dk(a, .35))
    elif st == 'panel':
        for x in range(0, 64, 8): c.r(x, 0, 8, 120, [b, a][(x // 8) % 2]); c.r(x, 0, 1, 120, dk(a, .3))
        c.r(0, 72, 64, 3, '#5a3a20'); c.r(0, 72, 64, 1, '#7a5230')                     # chair rail
        for x in range(0, 64, 16): c.ol(x+2, 78, 12, 36, dk(a, .25))                      # wainscot panels
    elif st == 'foam':
        for y in range(0, 120, 8):
            for x in range(0, 64, 8):
                c.r(x, y, 8, 8, b)
                for i in range(4): c.r(x+i, y+i, 8-2*i, 1, lt(b, .03*i)); c.r(x+i, y+7-i, 8-2*i, 1, dk(b, .12))
                c.r(x+3, y+3, 2, 2, h)
    elif st == 'navy':
        for x0 in (0, 32):
            c.r(x0+1, 4, 30, 112, a if x0 else b); c.ol(x0+1, 4, 30, 112, dk(a, .3)); c.r(x0+2, 5, 28, 1, h)
    elif st == 'greenwood':
        c.r(0, 0, 64, 120, b)
        for x in range(0, 64, 16): c.ol(x+2, 6, 12, 60, dk(a, .3)); c.r(x+3, 7, 10, 1, h)
        c.r(0, 70, 64, 4, '#3a2616'); c.r(0, 70, 64, 1, '#5a3a22')
        for x in range(0, 64, 4): c.r(x, 74, 3, 46, '#2a1c10' if (x // 4) % 2 else '#321f10')   # low wood wainscot
    elif st == 'labtile':
        for y in range(0, 120, 10):
            for x in range(0, 64, 10): c.r(x, y, 10, 10, [a, b][((x+y)//10) % 2]); c.r(x, y, 10, 1, dk(a, .3)); c.r(x, y, 1, 10, dk(a, .3))
    elif st == 'indbrick':
        for r in range(0, 120, 5):
            off = 0 if (r // 5) % 2 == 0 else 6
            for x in range(-12 + off, 64, 12): c.r(x+1, r+1, 11, 4, [a, b, h][((x*3 + r) // 12) % 3])
            c.r(0, r, 64, 1, dk(a, .4))
        c.r(0, 18, 64, 4, '#4a4640'); c.r(0, 18, 64, 1, '#6a655c'); c.r(0, 22, 64, 1, '#1a1816')   # horizontal pipe
        for x in (14, 46): c.r(x, 16, 3, 8, '#3a3631')
    elif st == 'glass':
        for x0 in (0, 32):
            c.r(x0+1, 2, 30, 96, mix(a, '#2ec4b6', .06)); c.ol(x0, 1, 32, 98, '#101a1a'); c.line(x0+4, 90, x0+26, 10, lt(a, .1))
        c.r(0, 98, 64, 22, a)
    elif st == 'olive':
        for x in range(0, 64, 16): c.r(x, 0, 1, 120, dk(a, .3))
        c.r(0, 14, 64, 1, '#a3e635'); c.r(0, 15, 64, 1, '#4a6a1c')                            # neon strip
    return c

def trim_tile(t):
    m = M[t]; a, b = m['trim']; st = m['trimstyle']; c = C(32, 5); c.r(0, 0, 32, 5, b)
    if st == 'hazard':
        for x in range(-5, 32, 1):
            for y in range(5):
                if ((x + y) // 3) % 2 == 0: c.p(x, y, a)
        c.r(0, 0, 32, 1, dk(a, .3))
    elif st == 'neon':
        c.r(0, 0, 32, 1, a); c.r(0, 1, 32, 1, dk(a, .5))
    elif st == 'wood':
        c.r(0, 0, 32, 2, a); c.r(0, 0, 32, 1, lt(a, .2)); c.r(0, 4, 32, 1, dk(b, .3))
    elif st == 'split':
        c.r(0, 0, 16, 1, a); c.r(16, 0, 16, 1, b); c.r(0, 1, 32, 4, '#2e2a2a')
    else:
        c.r(0, 0, 32, 1, a); c.r(0, 1, 32, 3, mix(b, a, .15))
    return c

# ----------------------------------------------------------------- boss mat for coder (rug slot)
def pcb_mat():
    W, H = 186, 90; c = C(W, H); g = '#39ff9c'
    c.r(0, 0, W, H, '#0e1714'); c.ol(0, 0, W, H, '#1f3a30'); c.ol(2, 2, W-4, H-4, g); c.ol(3, 3, W-6, H-6, '#16402e')
    for y in range(8, H-6, 6): c.r(6, y, W-12, 1, '#12211c')
    traces = [(8, 14, 60, 14, 70, 24), (8, 70, 40, 70, 52, 58), (178, 20, 130, 20, 118, 32), (178, 64, 140, 64, 128, 76),
              (60, 6, 60, 12, 70, 12), (126, 84, 126, 76, 116, 76), (20, 40, 38, 40, 38, 30)]
    for (x0, y0, x1, y1, x2, y2) in traces:
        c.line(x0, y0, x1, y1, '#1f7a52'); c.line(x1, y1, x2, y2, '#1f7a52'); c.r(x2-1, y2-1, 3, 3, g)
    for (x, y) in [(30, 50), (150, 42), (100, 12), (84, 80)]:
        c.r(x-6, y-4, 12, 8, '#1a1f22'); c.ol(x-6, y-4, 12, 8, '#2e3a40')
        for i in range(4): c.p(x-5+i*3, y-5, '#8a9a9a'); c.p(x-5+i*3, y+4, '#8a9a9a')
    c.ell(93, 45, 38, 17, '#101d18'); c.ring(93, 45, 1, g)
    for a in range(0, 360, 4):
        r = math.radians(a); c.p(93 + math.cos(r)*42, 45 + math.sin(r)*20, g if a % 16 else '#b8ffd8')
    glow(c, g, 1); return c

# ----------------------------------------------------------------- capsule accessories 28x24 (capsule top = row 8, eye row ~18)
ACC_OFF = {'x': -28, 'y': -56}   # css, relative to capsule centre (agent: pos+(0,-16); boss: (bx, by+6))
def acc(t, boss=False):
    c = C(28, 24); gold = '#f0c040'
    if t == 'default':
        c.r(4, 16, 20, 4, '#1a1a1f'); c.r(5, 17, 18, 2, '#ff2d3d'); c.r(7, 17, 3, 1, '#ffc0c8'); c.r(18, 17, 3, 1, '#ffc0c8')
        if boss:
            for i in range(7): c.r(6+i, 8-i, 2, 2, '#6a6e7c'); c.r(20-i, 8-i, 2, 2, '#6a6e7c')           # big V-crest horns
            c.r(12, 2, 4, 7, '#a855f7'); c.r(13, 3, 2, 2, '#ff2d3d'); c.r(4, 8, 20, 2, '#3a3d4a')
        else:
            c.r(13, 2, 2, 7, '#6a6e7c'); c.r(12, 1, 4, 2, '#a855f7'); c.r(10, 7, 8, 2, '#3a3d4a')
        c.outline_alpha(); glow(c, '#ff2d3d', 1); return c
    if t == 'coder':
        c.r(3, 7, 22, 2, '#1c2226'); c.r(3, 7, 2, 6, '#1c2226'); c.r(23, 7, 2, 6, '#1c2226')
        c.r(1, 12, 4, 7, '#1c2226'); c.r(23, 12, 4, 7, '#1c2226'); c.r(1, 13, 1, 5, '#39ff9c'); c.r(26, 13, 1, 5, '#39ff9c')
        c.line(4, 18, 9, 21, '#2a3036'); c.r(9, 21, 2, 2, '#39ff9c')
        c.r(9, 23, 1, 1, '#e8e8e8'); c.r(18, 23, 1, 1, '#e8e8e8')                                           # hoodie strings
    elif t == 'designer':
        c.ell(12, 8, 10, 3, '#e8779f'); c.r(4, 9, 17, 2, dk('#e8779f', .2)); c.r(12, 4, 2, 2, dk('#e8779f', .3)); c.r(8, 7, 5, 1, lt('#e8779f', .3))
    elif t == 'content':
        for x in (6, 16): c.ol(x, 16, 7, 5, gold); c.r(x+1, 17, 5, 3, '#d8e8f080'[:7])
        c.r(13, 17, 3, 1, gold); c.r(3, 17, 3, 1, gold); c.r(22, 17, 3, 1, gold)
    elif t == 'video':
        c.ell(14, 9, 11, 3, '#2a2236'); c.r(2, 9, 8, 2, '#2a2236'); c.r(4, 8, 1, 1, '#b36bff')             # backwards cap
        c.r(23, 15, 3, 4, '#15131a'); c.line(24, 19, 19, 22, '#15131a'); c.r(18, 22, 2, 1, '#ff3b3b')        # earpiece + mic
    elif t == 'analyst':
        for x in (5, 15): c.ol(x, 16, 8, 4, '#4da3ff')
        c.r(13, 17, 2, 1, '#4da3ff'); c.r(3, 17, 2, 1, '#4da3ff'); c.r(23, 17, 2, 1, '#4da3ff')
        c.line(24, 9, 26, 16, '#ffc24d'); c.p(26, 16, '#1d2636')                                             # pen behind ear
    elif t == 'research':
        c.r(4, 5, 20, 2, '#1a1a1a'); c.r(9, 7, 10, 3, '#1a1a1a'); c.r(13, 4, 2, 1, gold); c.line(21, 6, 23, 12, gold); c.r(22, 12, 2, 2, gold)
        for x in (9, 17): c.ring(x, 18, 3, '#c9a55a')
        c.r(12, 18, 2, 1, '#c9a55a')
    elif t == 'qa':
        c.r(1, 16, 26, 2, '#e5484d')
        for x in (5, 15): c.r(x, 14, 8, 6, '#2c3035'); c.r(x+1, 15, 6, 4, '#7fe0a0'); c.p(x+2, 15, '#e8fff0')
    elif t == 'ops':
        c.ell(14, 8, 11, 5, '#ff8a1f'); c.r(1, 10, 26, 2, dk('#ff8a1f', .2)); c.r(13, 3, 2, 7, lt('#ff8a1f', .3)); c.r(3, 10, 22, 1, '#f0c419')
        c.r(1, 14, 3, 5, '#2b2724'); c.line(2, 19, 7, 22, '#2b2724'); c.r(7, 22, 2, 1, '#ff8a1f')
    elif t == 'pm':
        c.line(8, 14, 14, 21, '#2ec4b6'); c.line(20, 14, 14, 21, '#2ec4b6'); c.r(11, 20, 7, 4, '#f4f1ea'); c.r(12, 21, 3, 1, '#2ec4b6'); c.r(12, 22, 5, 1, '#999')
    elif t == 'growth':
        c.ell(13, 8, 10, 4, '#a3e635'); c.r(3, 9, 20, 2, dk('#a3e635', .2)); c.r(14, 10, 12, 2, '#5f8a1c'); c.r(12, 5, 3, 2, '#232820')
    if boss:
        c.r(21, 21, 5, 3, gold); c.p(23, 21, '#fff4c8')                                                      # boss pin
    c.outline_alpha(); return c

# ----------------------------------------------------------------- EoM portrait for MEGATRON (84x84 css -> 42x42 cells)
def robot_portrait():
    c = C(42, 42); c.r(0, 0, 42, 42, '#15131d')
    for y in range(42): c.r(0, y, 42, 1, mix('#2a1f40', '#0e0c14', y/42))
    g = '#5a5e70'
    c.r(9, 8, 24, 26, g); c.r(9, 8, 24, 2, lt(g, .3)); c.r(31, 8, 2, 26, dk(g, .3))
    for i in range(8): c.r(10+i, 7-i if i < 6 else 1, 2, 2, '#6a6e7c'); c.r(30-i, 7-i if i < 6 else 1, 2, 2, '#6a6e7c')   # crest
    c.r(18, 2, 6, 8, '#a855f7'); c.r(20, 3, 2, 3, '#ff2d3d')
    c.r(11, 16, 20, 5, '#101014'); c.r(12, 17, 7, 3, '#ff2d3d'); c.r(23, 17, 7, 3, '#ff2d3d'); c.p(13, 17, '#ffc0c8'); c.p(24, 17, '#ffc0c8')
    c.r(14, 25, 14, 6, '#2a2c35')
    for x in range(15, 28, 3): c.r(x, 26, 2, 4, '#6a6e7c')
    c.r(5, 12, 4, 14, '#3a3d4a'); c.r(33, 12, 4, 14, '#3a3d4a'); c.r(6, 14, 2, 3, '#a855f7'); c.r(34, 14, 2, 3, '#a855f7')
    c.r(4, 34, 34, 8, '#2a2c35'); c.r(4, 34, 34, 1, '#a855f7'); emblem(c, 15, 35, '#4a4e60', '#ff2d3d') if False else None
    return c

# ----------------------------------------------------------------- MEGATRON fabricator (printer slot 32x30)
def fabricator():
    c = C(32, 30); g = '#3b3e4a'
    c.box(1, 3, 30, 26, g); c.r(1, 3, 30, 1, '#a855f7')
    c.r(4, 7, 24, 15, '#07060c'); c.ol(4, 7, 24, 15, '#2a2c35')
    c.r(8, 17, 16, 4, '#2a2c35'); c.r(9, 16, 14, 1, '#a855f7')                         # build plate
    c.r(12, 11, 8, 5, '#15b7d8'); c.r(13, 12, 3, 2, '#bff6ff')                           # energon cube being fabricated
    c.r(15, 7, 2, 4, '#6a6e7c'); c.r(14, 10, 4, 1, '#ff2d3d')                            # nozzle + laser
    for x in range(6, 27, 4): c.p(x, 8, '#ff2d3d' if x % 8 == 6 else '#4a4e60')
    c.r(4, 24, 10, 3, '#15161c'); c.r(5, 25, 6, 1, '#22e3ff'); c.r(22, 24, 5, 3, '#ff2d3d')
    c.r(10, 0, 12, 3, '#2a2c35'); c.r(12, 1, 8, 1, '#a855f7')
    c.outline_alpha(); glow(c, '#a855f7', 1); return c

# ----------------------------------------------------------------- per-theme capsule palettes / chrome v3
CAPS = {
 'default':  (['#7c3aed', '#9ca3af', '#6b7280', '#a855f7', '#dc2626', '#0891b2', '#4b5563', '#c026d3'], '#d8b4fe', '#2a2c35', False),
 'coder':    (['#16a34a', '#0d9488', '#0891b2', '#65a30d', '#15803d', '#0e7490', '#4d7c0f', '#047857'], '#86efac', '#15191c', False),
 'designer': (['#ec4899', '#a78bfa', '#f472b6', '#818cf8', '#fb7185', '#c084fc', '#f9a8d4', '#93c5fd'], '#fbcfe8', '#3a2c48', True),
 'content':  (['#b45309', '#a16207', '#9a3412', '#c2410c', '#78716c', '#b91c1c', '#854d0e', '#a8a29e'], '#fcd9a8', '#3a2a1a', True),
 'video':    (['#9333ea', '#c026d3', '#7c3aed', '#db2777', '#6d28d9', '#a21caf', '#be185d', '#8b5cf6'], '#e9d5ff', '#22163a', False),
 'analyst':  (['#2563eb', '#0284c7', '#3b82f6', '#0ea5e9', '#1d4ed8', '#f59e0b', '#6366f1', '#0369a1'], '#bfdbfe', '#12243c', True),
 'research': (['#15803d', '#a16207', '#166534', '#b45309', '#4d7c0f', '#92400e', '#3f6212', '#78716c'], '#e8d9a8', '#1f3a28', False),
 'qa':       (['#dc2626', '#16a34a', '#e11d48', '#15803d', '#b91c1c', '#059669', '#9f1239', '#4d7c0f'], '#fecaca', '#2a2a2e', True),
 'ops':      (['#ea580c', '#d97706', '#c2410c', '#ca8a04', '#b45309', '#dc2626', '#9a3412', '#a16207'], '#fed7aa', '#3a2410', False),
 'pm':       (['#0d9488', '#0891b2', '#14b8a6', '#0e7490', '#059669', '#eab308', '#0f766e', '#06b6d4'], '#99f6e4', '#10302e', True),
 'growth':   (['#65a30d', '#4d7c0f', '#84cc16', '#15803d', '#a16207', '#3f6212', '#16a34a', '#ca8a04'], '#d9f99d', '#243016', False),
}
