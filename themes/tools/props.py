"""Floor/wall-standing prop replacements + desk accessories. Cell = 2 css px.
tall  (WaterCooler slot, center 1010,200)  : 20x62 cells  -> 40x124 css
unit  (CoffeeMachine slot, center 1081,191): 30x33 cells  -> 60x66 css
pot   (Plant slot, center 118,970)         : 24x31 cells  -> 48x62 css
desk accessories                           : 12x12 cells  -> 24x24 css
"""
import math
from px import C, OUT, dk, lt, mix

# ---------------- tall (20x62) ----------------
def flag_stand():  # default: navy/gold banner on pole
    c = C(20, 62); gold = '#e0b54a'; navy = '#1f3a78'
    c.r(9, 3, 2, 55, '#b8913a'); c.r(9, 3, 1, 55, '#e8c86a')
    c.circ(10, 2, 2, gold)
    c.r(11, 5, 8, 26, navy); c.r(11, 5, 8, 1, lt(navy, .3)); c.r(18, 5, 1, 26, dk(navy, .3))
    for i in range(4): c.r(11+i*2, 31+ (i % 2), 2, 1, navy)
    c.r(13, 9, 4, 1, gold); c.r(12, 10, 6, 1, gold); c.r(14, 11, 2, 7, gold); c.r(12, 18, 6, 1, gold)  # emblem
    c.r(13, 21, 4, 4, gold); c.r(14, 22, 2, 2, navy)
    c.r(4, 57, 12, 3, '#3a3024'); c.r(5, 56, 10, 1, '#5a4a34'); c.r(3, 60, 14, 1, '#221a12')
    c.outline_alpha(); return c

def server_rack(beacon=False, accent='#39ff9c'):
    c = C(20, 62)
    top = 6 if beacon else 2
    c.box(1, top, 18, 60-top, '#23272e')
    c.r(3, top+2, 14, 60-top-5, '#0d0f12')
    for i in range(10):
        y = top+3 + i*5
        if y+4 > 58: break
        c.r(3, y, 14, 4, '#1b1f25'); c.r(3, y, 14, 1, '#2c323b')
        for j in range(3):
            col = accent if (i*3+j) % 4 else ('#ffcf3a' if not beacon else '#ff8a1f')
            if (i + j) % 5 == 0: col = '#ff4d4d' if beacon else '#2ee6e6'
            c.p(4+j*2, y+2, col)
        c.r(11, y+2, 5, 1, '#3a414c')
    for y in range(top+3, 58, 2): c.p(16, y, '#2a3038')
    c.r(2, 60, 3, 2, '#111'); c.r(15, 60, 3, 2, '#111')
    if beacon:
        c.r(7, 3, 6, 3, '#ff8a1f'); c.r(8, 2, 4, 1, '#ffb366'); c.r(8, 4, 1, 1, '#ffe0c0')
        c.r(6, 6, 8, 1, '#444')
    c.outline_alpha(); return c

def easel():  # designer
    c = C(20, 62); wood = '#b07a4a'
    c.line(10, 4, 2, 60, wood, 2); c.line(10, 4, 17, 60, dk(wood, .15), 2); c.line(10, 20, 10, 58, dk(wood, .3), 1)
    c.box(1, 10, 18, 22, '#f3efe6', hi='#ffffff', sh='#d4cdbf')
    for (x, y, r, col) in [(6, 16, 3, '#f5a8c8'), (12, 18, 4, '#9bf6ff'), (8, 24, 3, '#caffbf'), (14, 26, 2, '#ffd6a5')]:
        c.circ(x, y, r, col)
    c.line(3, 28, 16, 14, '#bdb2ff')
    c.r(0, 32, 20, 2, wood); c.r(0, 32, 20, 1, lt(wood, .25))
    c.outline_alpha(); return c

def tall_bookcase():  # content (warm wood)
    c = C(20, 62); wood = '#7a4a26'
    c.box(0, 2, 20, 60, wood)
    books = ['#a8452f', '#d9a441', '#3f6b4a', '#6b3f7a', '#c9713a', '#2f4f6b']
    for s in range(5):
        y0 = 4 + s*11
        c.r(2, y0, 16, 9, '#2e1a0c')
        x = 2; k = s
        while x < 17:
            wv = 2 + (k % 2); hv = 6 + (k*3) % 3
            if x+wv > 18: break
            col = books[k % len(books)]
            if s == 2 and x > 11:
                c.r(12, y0+6, 5, 3, '#e8e0d0'); c.r(12, y0+5, 5, 1, '#c8c0b0'); break  # paper stack
            c.r(x, y0+9-hv, wv, hv, col); c.r(x, y0+9-hv, 1, hv, lt(col, .2)); x += wv; k += 1
        c.r(1, y0+9, 18, 2, lt(wood, .12))
    c.outline_alpha(); return c

def ring_light():  # video
    c = C(20, 62); pu = '#c77dff'
    c.ring(10, 10, 8, '#f6efff', 3); c.ring(10, 10, 8, lt(pu, .6), 1); c.ring(10, 10, 5, '#2a2436', 1)
    c.r(9, 18, 2, 38, '#3a3446'); c.r(9, 18, 1, 38, '#5a526a')
    c.r(8, 34, 4, 2, '#2a2436')
    c.line(10, 55, 2, 61, '#3a3446', 1); c.line(10, 55, 18, 61, '#3a3446', 1); c.r(9, 55, 2, 6, '#3a3446')
    c.outline_alpha()
    return c

def data_totem():  # analyst: standing KPI screen
    c = C(20, 62); b = '#4da3ff'
    c.box(1, 2, 18, 34, '#1a2230')
    c.r(3, 4, 14, 30, '#07101c')
    c.txt(4, 6, 'KPI', '#9fd0ff')
    for i, hv in enumerate([4, 7, 5, 10]): c.r(4+i*3, 22-hv, 2, hv, b)
    c.line(4, 30, 8, 27, '#ffc24d'); c.line(8, 27, 11, 29, '#ffc24d'); c.line(11, 29, 16, 24, '#ffc24d')
    c.r(8, 36, 4, 22, '#2a3444'); c.r(8, 36, 1, 22, '#3c4a60')
    c.r(3, 58, 14, 3, '#1a2230'); c.r(4, 57, 12, 1, '#2a3444')
    c.outline_alpha(); return c

def floor_globe():  # research
    c = C(20, 62); brass = '#c9a55a'; wood = '#5a3a22'
    c.circ(10, 14, 8, '#2c5d7f')
    for (x, y, rx, ry) in [(7, 10, 3, 2), (12, 16, 3, 3), (6, 17, 2, 2), (13, 9, 2, 1)]: c.ell(x, y, rx, ry, '#4f8a4a')
    c.r(6, 8, 2, 1, lt('#2c5d7f', .3))
    c.ring(10, 14, 10, brass, 1)
    c.r(9, 24, 2, 4, brass)
    c.r(7, 28, 6, 3, wood)
    c.r(9, 31, 2, 22, wood); c.r(9, 31, 1, 22, lt(wood, .2))
    c.line(10, 50, 3, 60, wood, 2); c.line(10, 50, 16, 60, wood, 2); c.r(9, 52, 2, 9, dk(wood, .2))
    c.outline_alpha(); return c

def signal_pole():  # qa: red / amber / green test signal
    c = C(20, 62)
    c.box(4, 2, 12, 34, '#24272b')
    for i, col in enumerate(['#e5484d', '#3a3320', '#3ecf6e']):
        c.circ(10, 8+i*11, 4, col if i != 1 else '#4a3f1a')
        if i != 1: c.r(8, 6+i*11, 2, 1, lt(col, .5))
    c.r(9, 36, 2, 20, '#3a3f45'); c.r(9, 36, 1, 20, '#565d66')
    c.r(4, 56, 12, 5, '#e5484d'); for_x = [c.r(4+i*4, 56, 2, 5, '#f2f2f2') for i in range(3)]
    c.outline_alpha(); return c

def flip_chart():  # pm: gantt flip chart
    c = C(20, 62); teal = '#2ec4b6'
    c.line(10, 6, 2, 60, '#6b6f73', 1); c.line(10, 6, 18, 60, '#6b6f73', 1); c.r(9, 30, 2, 30, '#55595d')
    c.box(0, 4, 20, 28, '#f4f1ea', hi='#ffffff', sh='#d2cdc2'); c.r(0, 3, 20, 2, '#3a3f45')
    c.ctxt(10, 6, 'Q4', '#1a4a46')
    for i, (x, w, col) in enumerate([(2, 8, teal), (6, 7, '#ffd23f'), (9, 8, '#ff8fab'), (12, 6, teal)]):
        c.r(x, 13+i*4, w, 2, col)
    c.r(14, 12, 1, 18, '#e5484d')
    c.outline_alpha(); return c

def megaphone_pole():  # growth
    c = C(20, 62); lime = '#a3e635'
    c.r(9, 16, 2, 40, '#454b3a'); c.r(9, 16, 1, 40, '#666d57')
    # horn pointing right-up
    for i in range(10):
        h = 3 + i
        c.r(4+i, 10 - h//2, 1, h, lime if i < 9 else lt(lime, .3))
    c.r(4, 8, 1, 5, dk(lime, .35)); c.r(1, 9, 3, 3, '#2a2f22')
    c.r(6, 9, 6, 1, lt(lime, .35))
    c.r(14, 2, 1, 2, '#e9ffb8'); c.r(16, 4, 2, 1, '#e9ffb8'); c.r(16, 16, 2, 1, '#e9ffb8'); c.r(14, 17, 1, 2, '#e9ffb8')
    c.r(7, 13, 6, 3, '#2a2f22')
    c.r(4, 56, 12, 3, '#2a2f22'); c.r(5, 55, 10, 1, '#454b3a')
    c.outline_alpha(); return c

# ---------------- unit (30x33) ----------------
def radar_console():  # default
    c = C(30, 33); navy = '#1c2744'; gold = '#e0b54a'
    c.box(2, 4, 26, 28, navy)
    c.r(5, 6, 20, 17, '#06101f'); c.circ(15, 14, 7, '#0a2a1a'); c.ring(15, 14, 7, '#2ecf6e'); c.ring(15, 14, 4, '#1a7a44')
    c.r(8, 14, 15, 1, '#1a7a44'); c.r(15, 7, 1, 15, '#1a7a44'); c.line(15, 14, 20, 9, '#8affc8')
    c.r(18, 11, 2, 2, '#ffe07a'); c.r(11, 17, 1, 1, '#ffe07a')
    for i, col in enumerate([gold, '#ff5a5a', '#2ecf6e', gold]): c.r(6+i*5, 26, 3, 2, col)
    c.r(2, 4, 26, 1, gold)
    c.outline_alpha(); return c

def neon_fridge():  # coder: energy drink fridge
    c = C(30, 33); cyan = '#2ee6e6'
    c.box(3, 1, 24, 31, '#1b2226')
    c.r(5, 3, 20, 25, '#07141a'); c.ol(5, 3, 20, 25, cyan)
    for s in range(3):
        y = 5 + s*8
        for i in range(5):
            col = ['#39ff9c', '#ff3bd4', '#2ee6e6'][ (s+i) % 3 ]
            c.r(7+i*4, y, 3, 6, col); c.r(7+i*4, y, 3, 1, '#d8d8d8'); c.r(7+i*4, y+2, 1, 3, lt(col, .4))
        c.r(6, y+6, 18, 1, '#23404a')
    c.r(23, 12, 1, 6, '#9aa'); c.r(8, 29, 14, 2, '#0a0e10'); c.txt(10, 29, '', cyan)
    c.r(6, 29, 18, 1, cyan)
    c.outline_alpha(); return c

def paint_stool():  # designer: stool with paint jars + brushes
    c = C(30, 33); wood = '#b07a4a'
    c.r(4, 16, 22, 3, wood); c.r(4, 16, 22, 1, lt(wood, .25))
    c.r(6, 19, 2, 13, dk(wood, .2)); c.r(22, 19, 2, 13, dk(wood, .2)); c.r(6, 26, 18, 1, dk(wood, .3))
    for i, col in enumerate(['#f5a8c8', '#9bf6ff', '#ffd6a5']):
        x = 6 + i*7
        c.r(x, 9, 6, 7, '#e8e4dc'); c.r(x, 9, 6, 2, col); c.r(x+1, 12, 4, 1, dk('#e8e4dc', .1))
    c.line(9, 9, 6, 1, '#7a5a3a'); c.p(6, 1, '#f5a8c8'); c.line(16, 9, 18, 2, '#7a5a3a'); c.p(18, 2, '#bdb2ff')
    c.line(23, 9, 26, 3, '#7a5a3a'); c.p(26, 3, '#caffbf')
    c.outline_alpha(); return c

def typewriter_table():  # content
    c = C(30, 33); wood = '#7a4a26'; body = '#2f3a2f'
    c.r(1, 20, 28, 3, wood); c.r(1, 20, 28, 1, lt(wood, .25)); c.r(3, 23, 2, 10, dk(wood, .25)); c.r(25, 23, 2, 10, dk(wood, .25))
    c.r(8, 1, 14, 9, '#f4ecd8'); c.r(10, 3, 8, 1, '#8a7a5c'); c.r(10, 5, 10, 1, '#8a7a5c'); c.r(10, 7, 6, 1, '#8a7a5c')
    c.box(4, 8, 22, 5, body); c.r(3, 9, 2, 3, '#b8b8b0'); c.r(25, 9, 2, 3, '#b8b8b0')
    c.box(3, 12, 24, 8, dk(body, .1))
    for r in range(2):
        for k in range(7): c.r(5+k*3+r, 14+r*3, 2, 2, '#e8e0cc')
    c.outline_alpha(); return c

def camera_tripod():  # video
    c = C(30, 33); pu = '#b36bff'
    c.box(6, 3, 16, 10, '#23202b'); c.circ(24, 8, 4, '#15131a'); c.ring(24, 8, 4, '#4a4458'); c.circ(24, 8, 2, '#3a2a6a'); c.p(23, 7, '#c9b6ff')
    c.r(8, 1, 6, 2, '#23202b'); c.r(8, 5, 2, 2, '#ff3b3b'); c.r(12, 5, 7, 1, pu)
    c.r(13, 13, 3, 5, '#3a3446')
    c.line(14, 17, 5, 32, '#3a3446', 1); c.line(14, 17, 23, 32, '#3a3446', 1); c.r(14, 17, 1, 15, '#3a3446')
    # clapperboard leaning
    c.r(0, 24, 10, 8, '#1a1a1a'); c.r(0, 21, 10, 3, '#f2f2f2')
    for i in range(0, 10, 3): c.r(i, 21, 2, 3, '#1a1a1a')
    c.r(1, 26, 7, 1, '#bdbdbd'); c.r(1, 28, 5, 1, '#bdbdbd')
    c.outline_alpha(); return c

def report_cabinet():  # analyst
    c = C(30, 33); b = '#4da3ff'
    c.box(3, 13, 24, 19, '#2a3444')
    for i in range(2):
        y = 15 + i*8; c.r(5, y, 20, 7, '#232c3a'); c.r(12, y+3, 6, 1, '#8fa4c0')
    for i, col in enumerate(['#4da3ff', '#2e6fd8', '#ffc24d', '#9fd0ff']):
        c.r(5+i*4, 3 + (i % 2), 3, 10 - (i % 2), col); c.r(5+i*4, 5, 3, 1, lt(col, .4))
    cx, cy = 23, 8
    for y in range(3, 14):
        for x in range(18, 29):
            d = math.hypot(x-cx, y-cy)
            if d <= 4.6:
                a = (math.degrees(math.atan2(y-cy, x-cx)) + 450) % 360
                c.p(x, y, b if a < 220 else '#ffc24d')
    c.outline_alpha(); return c

def microscope_table():  # research
    c = C(30, 33); wood = '#5a3a22'; brass = '#c9a55a'
    c.r(1, 21, 28, 3, wood); c.r(1, 21, 28, 1, lt(wood, .25)); c.r(3, 24, 2, 9, dk(wood, .25)); c.r(25, 24, 2, 9, dk(wood, .25))
    c.r(8, 18, 12, 3, '#2a2a2a'); c.r(9, 17, 10, 1, '#444')
    c.r(16, 6, 3, 12, '#2f5d3a'); c.r(16, 6, 1, 12, lt('#2f5d3a', .25))
    c.line(15, 3, 10, 12, '#dddddd', 2); c.r(14, 1, 3, 3, '#1a1a1a')
    c.r(9, 12, 3, 3, brass); c.r(8, 15, 8, 1, '#8a8a8a')
    c.r(21, 15, 5, 6, '#d8ecd8'); c.r(21, 17, 5, 4, '#6fcf8a'); c.r(21, 14, 5, 1, '#aaa')  # flask
    c.outline_alpha(); return c

def test_bench():  # qa: test tube rack
    c = C(30, 33); red = '#e5484d'; grn = '#3ecf6e'
    c.r(1, 21, 28, 3, '#3a3f45'); c.r(1, 21, 28, 1, '#565d66'); c.r(3, 24, 2, 9, '#2a2e33'); c.r(25, 24, 2, 9, '#2a2e33')
    c.r(3, 15, 24, 6, '#d6d6d6'); c.r(3, 15, 24, 1, '#f2f2f2')
    for i in range(6):
        x = 5 + i*4; col = grn if i not in (2, 4) else red
        c.r(x, 5, 2, 12, '#e6f0f0'); c.r(x, 10 + (i % 2), 2, 7 - (i % 2), col); c.r(x, 4, 2, 1, '#9aa')
    c.box(20, 25, 9, 8, '#f4f1ea'); c.r(22, 27, 1, 1, grn); c.r(24, 27, 3, 1, '#888'); c.r(22, 30, 1, 1, red); c.r(24, 30, 3, 1, '#888')
    c.outline_alpha(); return c

def alarm_console():  # ops
    c = C(30, 33); o = '#ff8a1f'
    c.box(2, 9, 26, 23, '#2b2724')
    c.r(4, 11, 22, 10, '#050606')
    for i in range(22): c.p(4+i, 16 + int(3*math.sin(i*.9)), '#3ecf6e')
    c.r(18, 12, 7, 3, o)
    for i in range(4): c.r(5+i*6, 24, 4, 3, [o, '#3ecf6e', '#3ecf6e', '#ffcf3a'][i])
    c.r(11, 2, 8, 6, o); c.r(12, 1, 6, 1, '#ffb366'); c.r(12, 3, 2, 3, '#ffe0c0'); c.r(10, 8, 10, 1, '#444')
    c.p(7, 3, dk(o, .2)); c.p(22, 3, dk(o, .2)); c.p(5, 2, dk(o, .4)); c.p(24, 2, dk(o, .4))
    c.outline_alpha(); return c

def wall_calendar():  # pm
    c = C(30, 33); teal = '#2ec4b6'
    c.r(14, 0, 2, 3, '#555')
    c.box(1, 3, 28, 29, '#f4f1ea', hi='#ffffff', sh='#d2cdc2')
    c.r(1, 3, 28, 7, teal); c.ctxt(15, 5, 'SEP', '#0e3a36')
    for r in range(4):
        for k in range(6):
            x, y = 3 + k*4, 12 + r*5
            col = '#c9c3b6'
            if (r, k) == (3, 2): col = '#e5484d'
            elif r*6+k < 20: col = '#7a9a96'
            c.r(x, y, 3, 3, col)
    c.ring(12, 28, 3, '#e5484d', 1)
    c.outline_alpha(); return c

def trophy_shelf():  # growth
    c = C(30, 33); lime = '#a3e635'; gold = '#f0c040'
    c.box(2, 20, 26, 12, '#2a2f22')
    c.r(4, 22, 22, 1, '#3a4130'); c.txt(6, 25, 'TOP1', lime)
    c.r(9, 3, 12, 8, gold); c.r(10, 11, 10, 2, gold); c.r(13, 13, 4, 4, dk(gold, .15)); c.r(10, 17, 10, 3, dk(gold, .3))
    c.r(6, 4, 3, 5, dk(gold, .1)); c.r(21, 4, 3, 5, dk(gold, .1)); c.r(7, 5, 1, 3, '#2a2f22'); c.r(22, 5, 1, 3, '#2a2f22')
    c.r(11, 4, 2, 5, lt(gold, .5)); c.r(14, 6, 2, 2, lime)
    c.outline_alpha(); return c

# ---------------- pot (24x31) ----------------
def pot_base(c, col='#a0522d'):
    c.r(6, 22, 12, 9, col); c.r(5, 21, 14, 2, lt(col, .15)); c.r(6, 22, 2, 9, lt(col, .12)); c.r(16, 22, 2, 9, dk(col, .25))

def cactus_led():  # coder
    c = C(24, 31); g = '#2f8a57'
    c.r(10, 4, 5, 18, g); c.r(10, 4, 1, 18, lt(g, .25)); c.r(14, 4, 1, 18, dk(g, .3))
    c.r(5, 10, 3, 7, g); c.r(5, 16, 5, 2, g); c.r(17, 7, 3, 7, g); c.r(15, 13, 5, 2, g)
    for (x, y) in [(12, 6), (11, 11), (13, 15), (6, 12), (18, 9)]: c.p(x, y, '#d8ffe8')
    c.p(12, 3, '#ff3bd4'); c.p(13, 3, '#ff3bd4')
    c.r(6, 22, 12, 9, '#1b2226'); c.r(5, 21, 14, 2, '#2a343a'); c.r(6, 27, 12, 1, '#2ee6e6'); c.r(6, 28, 12, 1, '#177a7a')
    c.outline_alpha(); return c

def flower_pastel():  # designer
    c = C(24, 31); leaf = '#6fbf7a'
    c.line(12, 21, 12, 9, '#4a8a54'); c.line(12, 18, 6, 12, '#4a8a54'); c.line(12, 16, 18, 10, '#4a8a54')
    c.ell(8, 17, 3, 1.5, leaf); c.ell(16, 18, 3, 1.5, leaf)
    for (x, y, col) in [(12, 7, '#f5a8c8'), (6, 11, '#bdb2ff'), (18, 9, '#ffd6a5')]:
        for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)): c.circ(x+dx, y+dy, 1.3, col)
        c.p(x, y, '#fff3b0')
    pot_base(c, '#e8b4c8')
    c.outline_alpha(); return c

def fern_big():  # research
    c = C(24, 31); g = '#2f6b3a'; g2 = '#4f9a58'
    for ang in (-70, -45, -20, 0, 20, 45, 70):
        a = math.radians(ang - 90)
        for t in range(3, 14):
            x = 12 + math.cos(a)*t; y = 21 + math.sin(a)*t*1.1 + (t*t)/40
            c.r(round(x), round(y), 1, 1, g)
            if t % 2 == 0:
                c.p(round(x)+1, round(y), g2); c.p(round(x)-1, round(y)+1, g2)
    pot_base(c, '#6b4a30')
    c.outline_alpha(); return c

def extinguisher():  # ops
    c = C(24, 31); red = '#d9352b'
    c.r(8, 6, 8, 24, red); c.r(8, 6, 2, 24, lt(red, .25)); c.r(15, 6, 1, 24, dk(red, .3))
    c.r(9, 4, 6, 2, dk(red, .2)); c.r(10, 2, 4, 2, '#2a2a2a'); c.r(14, 2, 5, 1, '#2a2a2a'); c.r(6, 3, 3, 1, '#2a2a2a')
    c.line(9, 3, 5, 12, '#1a1a1a'); c.r(4, 12, 2, 4, '#1a1a1a')
    c.r(9, 13, 6, 7, '#f2f2f2'); c.r(10, 15, 4, 1, '#ff8a1f'); c.r(10, 17, 4, 1, '#888')
    c.r(7, 29, 10, 2, '#222')
    c.outline_alpha(); return c

def money_sprout():  # growth
    c = C(24, 31); lime = '#a3e635'
    c.line(12, 21, 12, 6, '#5f8a1c', 1)
    for (x, y, s) in [(8, 16, -1), (16, 13, 1), (8, 10, -1), (16, 8, 1)]:
        c.ell(x, y, 3.2, 1.8, lime); c.r(min(x, 12), y, abs(12-x), 1, '#5f8a1c'); c.p(x - s, y - 1, '#e9ffb8')
    c.r(11, 2, 3, 1, '#e9ffb8'); c.r(12, 1, 1, 3, '#e9ffb8')
    pot_base(c, '#454b3a'); c.ctxt(12, 24, '$', lime)
    c.outline_alpha(); return c

def film_reels():  # video
    c = C(24, 31); pu = '#b36bff'
    for (cx, cy, r) in [(12, 22, 8), (12, 9, 7)]:
        c.circ(cx, cy, r, '#2a2436'); c.ring(cx, cy, r, '#6a5a82')
        for k in range(5):
            a = k*2*math.pi/5; c.circ(cx + math.cos(a)*r*.55, cy + math.sin(a)*r*.55, 1.2, '#0e0c12')
        c.circ(cx, cy, 1.2, pu)
    c.outline_alpha(); return c

def paper_bin():  # content
    c = C(24, 31)
    for (x, y) in [(9, 13), (14, 12), (12, 9), (7, 16), (17, 15)]:
        c.circ(x, y, 3, '#efe6d2'); c.p(x-1, y, '#c8bc9e'); c.p(x+1, y-1, '#c8bc9e')
    c.r(5, 16, 14, 14, '#6b4423'); c.r(5, 16, 14, 1, '#8a5a30')
    for x in range(7, 18, 3): c.r(x, 18, 1, 11, '#553518')
    c.outline_alpha(); return c

def bonsai_check():  # qa: plant with check flag
    c = C(24, 31); g = '#3ecf6e'
    c.line(12, 21, 10, 13, '#6b4a30', 2); c.line(11, 15, 16, 11, '#6b4a30', 1)
    c.ell(9, 11, 5, 3, '#2f8a57'); c.ell(16, 9, 4, 3, '#2f8a57'); c.ell(10, 9, 3, 2, '#4fbf7a')
    c.r(18, 12, 1, 9, '#aaa'); c.r(19, 12, 4, 3, g); c.p(20, 13, '#fff')
    pot_base(c, '#3a3f45')
    c.outline_alpha(); return c

def printer_3d():  # coder: replaces old printer on the mini desk (64x60 css -> 32x30 cells)
    c = C(32, 30); cyan = '#2ee6e6'
    c.box(2, 1, 28, 28, '#1f252a')
    c.r(5, 4, 22, 18, '#0a1418'); c.r(5, 4, 22, 1, '#2e3a40')
    c.r(5, 8, 22, 1, '#56626a'); c.r(14, 8, 5, 3, '#ff8a1f'); c.r(16, 11, 1, 2, '#ffcf3a')
    c.r(9, 17, 14, 4, '#39ff9c'); c.r(10, 15, 12, 2, '#2fd684'); c.r(11, 13, 10, 2, '#39ff9c')
    c.r(5, 21, 22, 1, '#3a464e')
    c.r(5, 24, 10, 3, '#0a1418'); c.txt(6, 23, '', cyan); c.r(6, 25, 7, 1, cyan); c.r(20, 24, 3, 3, '#39ff9c')
    c.outline_alpha(); return c

# ---------------- desk accessories (12x12) ----------------
def d_flag():
    c = C(12, 12); c.r(3, 1, 1, 10, '#b8913a'); c.r(4, 1, 6, 4, '#1f3a78'); c.r(5, 2, 2, 2, '#e0b54a'); c.r(1, 10, 5, 2, '#3a3024'); c.outline_alpha(); return c
def d_medal():
    c = C(12, 12); c.line(3, 0, 6, 5, '#1f3a78', 2); c.line(9, 0, 6, 5, '#e5484d', 2); c.circ(6, 8, 3, '#e0b54a'); c.p(6, 8, '#fff4c8'); c.outline_alpha(); return c
def d_can():
    c = C(12, 12); c.r(4, 1, 4, 10, '#1b2226'); c.r(4, 1, 4, 1, '#bbb'); c.r(4, 4, 4, 3, '#39ff9c'); c.r(4, 4, 1, 3, '#b8ffd8'); c.outline_alpha(); return c
def d_rgbfan():
    c = C(12, 12); c.box(1, 1, 10, 10, '#15191d'); c.ring(6, 6, 3.6, '#ff3bd4'); c.ring(6, 6, 2.2, '#2ee6e6'); c.p(6, 6, '#fff'); c.outline_alpha(); return c
def d_palette():
    c = C(12, 12); c.ell(6, 6, 5.5, 4.2, '#e8d2b0'); c.circ(8, 7, 1, '#211c27')
    for (x, y, col) in [(3, 5, '#f5a8c8'), (5, 3, '#9bf6ff'), (8, 3, '#caffbf'), (4, 8, '#bdb2ff')]: c.r(x, y, 2, 2, col)
    c.outline_alpha(); return c
def d_tablet():
    c = C(12, 12); c.box(0, 2, 11, 9, '#2a2431'); c.r(2, 4, 7, 5, '#bdb2ff'); c.line(3, 8, 7, 5, '#f5a8c8'); c.line(9, 1, 11, 7, '#ececec'); c.outline_alpha(); return c
def d_notebook():
    c = C(12, 12); c.r(1, 2, 10, 9, '#a8452f'); c.r(2, 2, 8, 8, '#f4ecd8'); [c.r(3, 4+i*2, 6, 1, '#b8a888') for i in range(3)]; c.line(7, 9, 11, 1, '#2a2a2a'); c.outline_alpha(); return c
def d_bookstack():
    c = C(12, 12); [c.r(1+(i % 2), 8-i*3, 10-(i % 2), 3, col) for i, col in enumerate(['#3f6b4a', '#a8452f', '#d9a441'])]; c.outline_alpha(); return c
def d_clapper():
    c = C(12, 12); c.r(1, 5, 10, 6, '#1a1a1a'); c.r(1, 2, 10, 3, '#f2f2f2'); [c.r(2+i*3, 2, 2, 3, '#1a1a1a') for i in range(3)]; c.r(2, 7, 6, 1, '#b36bff'); c.outline_alpha(); return c
def d_minicam():
    c = C(12, 12); c.box(0, 3, 8, 7, '#23202b'); c.circ(9, 6, 2, '#15131a'); c.p(9, 6, '#b36bff'); c.r(1, 1, 3, 2, '#23202b'); c.p(2, 5, '#ff3b3b'); c.outline_alpha(); return c
def d_calc():
    c = C(12, 12); c.box(2, 0, 8, 12, '#2a3444'); c.r(3, 1, 6, 3, '#9fd0ff')
    for i in range(3):
        for j in range(3): c.p(3+j*2, 6+i*2, '#dfe8f5')
    c.outline_alpha(); return c
def d_miniPie():
    c = C(12, 12)
    for y in range(12):
        for x in range(12):
            d = math.hypot(x-6, y-6)
            if d <= 5: a = (math.degrees(math.atan2(y-6, x-6)) + 450) % 360; c.p(x, y, '#4da3ff' if a < 230 else '#ffc24d')
    c.outline_alpha(); return c
def d_openbook():
    c = C(12, 12); c.r(0, 4, 12, 6, '#f4ecd8'); c.r(6, 4, 1, 6, '#b8a888'); [c.r(1, 5+i*2, 4, 1, '#b8a888') for i in range(2)]; [c.r(8, 5+i*2, 3, 1, '#b8a888') for i in range(2)]; c.r(0, 10, 12, 1, '#2f5d3a'); c.outline_alpha(); return c
def d_magnifier():
    c = C(12, 12); c.circ(5, 5, 3.5, '#bfe3f0'); c.ring(5, 5, 3.8, '#c9a55a'); c.line(8, 8, 11, 11, '#5a3a22', 2); c.p(4, 3, '#fff'); c.outline_alpha(); return c
def d_bugjar():
    c = C(12, 12); c.r(2, 3, 8, 8, '#cfe8e8'); c.r(2, 2, 8, 1, '#888'); c.r(3, 3, 1, 7, '#fff')
    from wall_wide import bug_icon
    bug_icon(c, 4, 5, '#e5484d'); c.outline_alpha(); return c
def d_clipboard():
    c = C(12, 12); c.r(1, 1, 10, 11, '#8a5a30'); c.r(2, 2, 8, 9, '#f4f1ea'); c.r(4, 0, 4, 2, '#888')
    c.p(3, 4, '#3ecf6e'); c.r(5, 4, 4, 1, '#999'); c.p(3, 7, '#e5484d'); c.r(5, 7, 4, 1, '#999'); c.outline_alpha(); return c
def d_walkie():
    c = C(12, 12); c.r(8, 0, 1, 4, '#222'); c.box(3, 3, 7, 9, '#2b2724'); c.r(4, 5, 5, 2, '#ff8a1f'); c.r(5, 8, 3, 3, '#555'); c.outline_alpha(); return c
def d_beacon():
    c = C(12, 12); c.r(3, 3, 6, 6, '#ff8a1f'); c.r(4, 2, 4, 1, '#ffb366'); c.r(4, 4, 2, 3, '#ffe0c0'); c.r(2, 9, 8, 3, '#2a2a2a'); c.outline_alpha(); return c
def d_sticky():
    c = C(12, 12); c.r(2, 4, 8, 8, '#ff8fab'); c.r(0, 2, 8, 8, '#ffd23f'); c.r(1, 4, 5, 1, '#a88a10'); c.r(1, 6, 4, 1, '#a88a10'); c.outline_alpha(); return c
def d_hourglass():
    c = C(12, 12); c.r(2, 0, 8, 2, '#2ec4b6'); c.r(2, 10, 8, 2, '#2ec4b6')
    for y in range(2, 10):
        w = abs(6 - y)*1 + 1; c.r(6 - w//2 - (1 if y < 6 else 0), y, w + 1, 1, '#e8f6f4')
    c.r(5, 7, 2, 3, '#e0b54a'); c.p(6, 5, '#e0b54a'); c.outline_alpha(); return c
def d_megaphone():
    c = C(12, 12); [c.r(2+i, 6 - (2+i)//2, 1, 2+i, '#a3e635') for i in range(8)]; c.r(0, 5, 2, 3, '#2a2f22'); c.r(4, 8, 2, 3, '#2a2f22'); c.outline_alpha(); return c
def d_rocket():
    c = C(12, 12); c.r(5, 1, 3, 8, '#e8e8e8'); c.r(6, 0, 1, 1, '#e8e8e8'); c.p(6, 3, '#4da3ff'); c.r(4, 7, 1, 3, '#a3e635'); c.r(8, 7, 1, 3, '#a3e635'); c.r(5, 9, 3, 2, '#ff8a1f'); c.p(6, 11, '#ffcf3a'); c.outline_alpha(); return c

TALL = {'flag_stand': flag_stand, 'server_rack': lambda: server_rack(False), 'easel': easel, 'tall_bookcase': tall_bookcase,
        'ring_light': ring_light, 'data_totem': data_totem, 'floor_globe': floor_globe, 'signal_pole': signal_pole,
        'noc_rack': lambda: server_rack(True, '#3ecf6e'), 'flip_chart': flip_chart, 'megaphone_pole': megaphone_pole}
UNIT = {'radar_console': radar_console, 'neon_fridge': neon_fridge, 'paint_stool': paint_stool, 'typewriter_table': typewriter_table,
        'camera_tripod': camera_tripod, 'report_cabinet': report_cabinet, 'microscope_table': microscope_table, 'test_bench': test_bench,
        'alarm_console': alarm_console, 'wall_calendar': wall_calendar, 'trophy_shelf': trophy_shelf}
POT = {'cactus_led': cactus_led, 'flower_pastel': flower_pastel, 'fern_big': fern_big, 'extinguisher': extinguisher,
       'money_sprout': money_sprout, 'film_reels': film_reels, 'paper_bin': paper_bin, 'bonsai_check': bonsai_check}
MISC = {'printer_3d': printer_3d}
DESK = {'d_flag': d_flag, 'd_medal': d_medal, 'd_can': d_can, 'd_rgbfan': d_rgbfan, 'd_palette': d_palette, 'd_tablet': d_tablet,
        'd_notebook': d_notebook, 'd_bookstack': d_bookstack, 'd_clapper': d_clapper, 'd_minicam': d_minicam, 'd_calc': d_calc,
        'd_minipie': d_miniPie, 'd_openbook': d_openbook, 'd_magnifier': d_magnifier, 'd_bugjar': d_bugjar, 'd_clipboard': d_clipboard,
        'd_walkie': d_walkie, 'd_beacon': d_beacon, 'd_sticky': d_sticky, 'd_hourglass': d_hourglass, 'd_megaphone': d_megaphone,
        'd_rocket': d_rocket}
