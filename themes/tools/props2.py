"""v5.2 rev2: chunkier, full-slot-width theme props (same slot sizes as the ref props) + MEGATRON/Decepticon-style set.
Emblem = original angular mask drawn by @designer (NOT the Hasbro Decepticon insignia)."""
import math
from px import C, OUT, dk, lt, mix
from wall_wide import bug_icon, check_icon

GM, GM2, PUR, RED, ENG = '#2a2c35', '#3b3e4a', '#a855f7', '#ff2d3d', '#22e3ff'

EMBLEM = ['#.........#', '##.......##', '###.....###', '.###...###.', '.#########.', '.##.###.##.',
          '..#######..', '..##...##..', '...#####...', '....###....', '.....#.....']
def emblem(c, x, y, col, eye=RED, sc=1):
    for yy, row in enumerate(EMBLEM):
        for xx, v in enumerate(row):
            if v == '#': c.r(x+xx*sc, y+yy*sc, sc, sc, col)
    c.r(x+3*sc, y+5*sc, sc, sc, eye); c.r(x+7*sc, y+5*sc, sc, sc, eye)

def glow(c, col, rad=2):
    """soft alpha halo around the opaque silhouette (added after outline)"""
    src = [row[:] for row in c.d]
    for y in range(c.h):
        for x in range(c.w):
            if src[y][x] is None:
                best = 99
                for dy in range(-rad, rad+1):
                    for dx in range(-rad, rad+1):
                        yy, xx = y+dy, x+dx
                        if 0 <= xx < c.w and 0 <= yy < c.h and src[yy][xx] is not None: best = min(best, max(abs(dx), abs(dy)))
                if best <= rad: c.d[y][x] = col + ('55' if best == 1 else '22')

# ---------------- tall 20x62 (slot 40x124 css) ----------------
def rack(accent, alt, beacon=False, body='#252a31'):
    c = C(20, 62)
    c.box(0, 0, 20, 62, body)
    c.r(1, 1, 18, 2, lt(body, .25)); c.r(1, 1, 1, 60, accent)             # accent edge strip
    top = 5 if beacon else 3
    if beacon:
        c.r(6, 1, 8, 3, '#ff8a1f'); c.r(7, 1, 3, 1, '#ffe0c0'); c.r(3, 3, 14, 1, '#111')
    c.r(3, top, 15, 55-top, '#08090c')
    for i in range(11):
        y = top + 1 + i*5
        if y + 4 > 57: break
        c.r(3, y, 15, 4, '#1c2128'); c.r(3, y, 15, 1, '#39414d')
        for j in range(4):
            col = accent if (i + j) % 3 else alt
            if (i*7 + j) % 11 == 0: col = '#ff4d4d'
            c.r(4 + j*2, y+2, 1, 1, col)
        for v in range(12, 17, 2): c.r(v, y+1, 1, 2, '#0d0f12')
    for k in range(0, 40, 9): c.line(5+k//4, top+2+k, 9+k//4, top+k-2, '#ffffff22' if False else '#3a4452')  # glass glint
    c.r(3, 58, 15, 2, accent)                                              # base glow bar
    c.r(1, 60, 4, 2, '#0e0e0e'); c.r(15, 60, 4, 2, '#0e0e0e')
    c.outline_alpha(); glow(c, accent, 1); return c

def energon_pylon():  # MEGATRON: energon dispenser (replaces water cooler)
    c = C(20, 62)
    c.box(1, 0, 18, 7, GM2); c.r(3, 2, 14, 3, '#15161c'); emblem(c, 4, 1, PUR, RED) if False else None
    c.r(8, 2, 4, 2, RED); c.r(9, 2, 1, 1, '#ffb0b8')                        # red optic
    c.box(0, 7, 20, 36, GM)
    c.r(3, 9, 14, 32, '#061a22')                                             # glass tank
    for y in range(20, 41): c.r(3, y, 14, 1, mix(ENG, '#0a6a8a', (y-20)/30))
    c.r(3, 19, 14, 1, lt(ENG, .5))
    for (x, y, s) in [(5, 24, 3), (11, 28, 4), (7, 33, 3), (12, 36, 2)]:   # floating energon cubes
        c.r(x, y, s, s, lt(ENG, .55)); c.p(x, y, '#ffffff')
    for (x, y) in [(6, 14), (13, 12), (9, 17)]: c.p(x, y, '#3fa9c4')        # bubbles
    c.r(4, 10, 1, 29, '#9ff4ff'); c.r(3, 9, 14, 1, '#1d4652')
    c.r(1, 8, 2, 34, PUR); c.r(17, 8, 2, 34, dk(PUR, .35))                   # purple frame rails
    c.box(0, 43, 20, 19, GM2)
    c.r(7, 45, 6, 3, '#15161c'); c.r(9, 48, 2, 2, ENG)                       # spigot
    emblem(c, 5, 50, lt(GM2, .45), RED)
    c.r(0, 60, 20, 2, '#15161c')
    c.outline_alpha(); glow(c, ENG, 1); return c

def easel2():  # designer
    c = C(20, 62); wood = '#c08a55'
    c.line(9, 0, 1, 61, wood, 2); c.line(10, 0, 18, 61, dk(wood, .12), 2); c.r(9, 30, 2, 31, dk(wood, .3))
    c.box(0, 4, 20, 28, '#f6f1e7', hi='#ffffff', sh='#d4cdbf')
    c.r(2, 6, 16, 24, '#2c2640')                                            # dark canvas, pastel painting
    c.circ(7, 12, 4, '#f5a8c8'); c.circ(13, 17, 5, '#9bf6ff'); c.circ(6, 24, 3, '#caffbf'); c.circ(14, 26, 2, '#ffd6a5')
    c.line(3, 28, 17, 8, '#bdb2ff'); c.p(8, 11, '#fff')
    c.r(0, 32, 20, 3, wood); c.r(0, 32, 20, 1, lt(wood, .3))
    for i, col in enumerate(['#f5a8c8', '#9bf6ff', '#ffd6a5', '#bdb2ff']): c.r(2+i*4, 30, 3, 2, col)  # paint tubes on tray
    c.ell(10, 46, 7, 4, '#e8d2b0'); c.circ(12, 47, 1, '#2c2640')             # palette hanging on legs
    for (x, y, col) in [(6, 45, '#f5a8c8'), (9, 43, '#9bf6ff'), (13, 44, '#caffbf'), (7, 48, '#bdb2ff')]: c.r(x, y, 2, 2, col)
    c.outline_alpha(); glow(c, '#f5a8c8', 1); return c

def bookcase2():  # content
    c = C(20, 62); wood = '#8a5530'
    c.box(0, 0, 20, 62, wood)
    books = ['#c4553a', '#e8b04a', '#4f8a5a', '#8a4fa0', '#e07a3a', '#3f6a9a', '#d8c8a0']
    for s in range(5):
        y0 = 2 + s*12
        c.r(2, y0, 16, 10, '#2a160a')
        x = 2; k = s*2
        while x < 18:
            wv = 2 + (k % 2); hv = 7 + (k*3) % 4
            if x + wv > 18: break
            col = books[k % len(books)]
            if s == 1 and x >= 12:
                c.r(12, y0+4, 6, 6, '#3a3a3a'); c.r(13, y0+5, 4, 3, '#e8e0cc'); c.r(12, y0+3, 6, 1, '#555'); break  # typewriter mini
            c.r(x, y0+10-hv, wv, hv, col); c.r(x, y0+10-hv, 1, hv, lt(col, .25)); c.r(x, y0+10-hv+2, wv, 1, lt(col, .45))
            x += wv; k += 1
        c.r(1, y0+10, 18, 2, lt(wood, .18))
    c.outline_alpha(); glow(c, '#e0a060', 1); return c

def softbox():  # video
    c = C(20, 62); pu = '#b36bff'
    c.r(0, 0, 20, 22, '#221d2c'); c.r(2, 2, 16, 18, '#f7f0ff'); c.r(2, 2, 16, 2, '#ffffff')
    c.r(4, 6, 12, 10, '#efe2ff'); c.ol(0, 0, 20, 22, OUT); c.r(0, 22, 20, 1, pu)
    c.r(8, 23, 4, 4, '#3a3446'); c.r(9, 27, 3, 26, '#3a3446'); c.r(9, 27, 1, 26, '#6a6280')
    c.r(12, 36, 5, 5, '#15131a'); c.r(13, 37, 2, 2, '#ff3b3b')              # REC tally box on stand
    c.line(10, 52, 1, 61, '#3a3446', 2); c.line(10, 52, 18, 61, '#3a3446', 2); c.r(9, 52, 3, 9, '#3a3446')
    c.outline_alpha(); glow(c, pu, 2); return c

def kpi_totem():  # analyst
    c = C(20, 62); b = '#4da3ff'
    c.box(0, 0, 20, 34, '#1d2636'); c.r(2, 2, 16, 30, '#06101d')
    c.txt(3, 3, 'KPI', '#9fd0ff'); c.r(14, 4, 3, 3, '#3ecf6e')
    for i, hv in enumerate([5, 8, 6, 11, 14]): c.r(3+i*3, 21-hv, 2, hv, b if i < 4 else '#ffc24d')
    c.line(3, 29, 7, 26, '#ffc24d'); c.line(7, 26, 11, 28, '#ffc24d'); c.line(11, 28, 16, 23, '#ffc24d')
    c.r(2, 22, 16, 1, '#1c3150')
    c.r(7, 34, 6, 22, '#2a3444'); c.r(7, 34, 1, 22, '#44546e'); c.r(9, 38, 2, 14, b)
    c.box(1, 56, 18, 6, '#1d2636'); c.r(3, 58, 14, 1, b)
    c.outline_alpha(); glow(c, b, 1); return c

def globe2():  # research
    c = C(20, 62); brass = '#d8b464'; wood = '#6a4428'
    c.circ(10, 11, 9, '#2c6d9f')
    for (x, y, rx, ry) in [(6, 7, 4, 3), (13, 13, 4, 4), (5, 15, 2, 2), (14, 5, 2, 2)]: c.ell(x, y, rx, ry, '#5fa85a')
    c.r(5, 5, 3, 1, lt('#2c6d9f', .4)); c.r(4, 6, 1, 2, lt('#2c6d9f', .4))
    c.ring(10, 11, 10, brass, 1); c.r(9, 21, 2, 4, brass)
    c.box(3, 25, 14, 4, wood); c.r(8, 29, 4, 20, wood); c.r(8, 29, 1, 20, lt(wood, .25))
    c.box(5, 36, 10, 7, '#2f5d3a'); c.r(6, 38, 8, 1, brass)                  # atlas book on stand
    c.line(10, 48, 1, 61, wood, 2); c.line(10, 48, 18, 61, wood, 2); c.r(9, 49, 3, 12, dk(wood, .2))
    c.outline_alpha(); glow(c, brass, 1); return c

def test_rig():  # qa
    c = C(20, 62); red, grn, amb = '#e5484d', '#3ecf6e', '#ffb224'
    c.box(6, 0, 8, 18, '#24272b')
    for i, col in enumerate([red, amb, grn]): c.r(7, 1+i*5, 6, 4, col); c.r(8, 2+i*5, 2, 1, lt(col, .6))
    c.box(0, 18, 20, 44, '#2c3035')
    c.r(2, 20, 16, 16, '#0a0c0d')
    c.txt(3, 21, 'PASS', grn); c.txt(3, 28, 'BUG 3', red)
    c.r(2, 38, 16, 1, '#1a1c1f')
    for i in range(3):
        y = 40 + i*7; c.r(2, y, 16, 6, '#363b42'); c.r(8, y+2, 4, 1, '#9aa3ad')
        c.r(15, y+2, 2, 2, [grn, grn, red][i])
    c.r(1, 60, 4, 2, '#111'); c.r(15, 60, 4, 2, '#111')
    c.outline_alpha(); glow(c, red, 1); return c

def flipchart2():  # pm
    c = C(20, 62); teal = '#2ec4b6'
    c.line(9, 4, 1, 61, '#6b7075', 2); c.line(10, 4, 18, 61, '#6b7075', 2); c.r(9, 32, 2, 29, '#55595d')
    c.r(0, 2, 20, 3, '#3a3f45')
    c.box(0, 4, 20, 30, '#f4f1ea', hi='#ffffff', sh='#d2cdc2')
    c.ctxt(10, 6, 'Q4', '#12524c')
    for i, (x, w, col) in enumerate([(2, 9, teal), (5, 8, '#ffd23f'), (9, 8, '#ff8fab'), (12, 6, teal), (3, 12, '#7ae7e0')]):
        c.r(x, 13+i*4, w, 3, col); c.r(x, 13+i*4, w, 1, lt(col, .35))
    c.r(14, 12, 1, 21, '#e5484d')
    c.r(1, 34, 18, 2, '#3a3f45'); c.r(3, 33, 3, 1, teal); c.r(8, 33, 3, 1, '#e5484d')
    c.outline_alpha(); glow(c, teal, 1); return c

def growth_kiosk():  # growth
    c = C(20, 62); lime = '#a3e635'
    for i in range(12):                                                        # big megaphone on top
        h = 3 + i // 1
        c.r(4+i, 8 - h//2, 1, h, lime if i < 11 else lt(lime, .35))
    c.r(1, 6, 3, 4, '#2a2f22'); c.r(6, 5, 7, 1, lt(lime, .45))
    c.box(0, 16, 20, 46, '#232a1c'); c.r(2, 18, 16, 22, '#0d1209')
    for k in range(6): c.r(9, 24+k, 2, 1, lime)                                # up arrow
    c.r(6, 24, 8, 1, lime); c.r(7, 23, 6, 1, lime); c.r(8, 22, 4, 1, lime); c.r(9, 21, 2, 1, lime)
    c.txt(3, 32, '+248', lime)
    for i, hv in enumerate([3, 5, 7, 10]): c.r(4+i*3, 56-hv, 2, hv, lime if i == 3 else '#5f8a1c')
    c.r(2, 42, 16, 1, '#3a4430')
    c.outline_alpha(); glow(c, lime, 1); return c

# ---------------- unit 30x33 ----------------
def energon_cubes():  # MEGATRON (coffee slot)
    c = C(30, 33)
    c.box(0, 26, 30, 7, GM2); c.r(2, 28, 26, 1, PUR); c.r(13, 29, 4, 2, RED)
    def cube(x, y, s):
        c.r(x, y+3, s, s, '#15b7d8')
        for i in range(3): c.r(x+3-i, y+i, s, 1, lt(ENG, .45 - i*.1))
        c.r(x+s, y+1, 2, s+1, '#0b7f99') if False else None
        c.r(x+2, y+5, s-4, s-4, lt(ENG, .25)); c.r(x+3, y+6, 2, 2, '#ffffff')
        c.ol(x, y+3, s, s, '#07404e')
    cube(2, 13, 12); cube(16, 13, 12); cube(9, 1, 12)
    c.outline_alpha(); glow(c, ENG, 1); return c

def neon_fridge2():  # coder
    c = C(30, 33); cyan = '#2ee6e6'
    c.box(0, 0, 30, 33, '#1b2226')
    c.r(2, 2, 26, 26, '#061318'); c.ol(2, 2, 26, 26, cyan)
    for s in range(3):
        y = 4 + s*8
        for i in range(6):
            col = ['#39ff9c', '#ff3bd4', '#2ee6e6'][(s + i) % 3]
            c.r(4+i*4, y, 3, 6, col); c.r(4+i*4, y, 3, 1, '#e8e8e8'); c.r(4+i*4, y+2, 1, 3, lt(col, .5))
        c.r(3, y+6, 24, 1, '#23404a')
    c.r(26, 10, 1, 9, '#9fb'); c.r(2, 29, 26, 2, cyan); c.r(10, 29, 10, 1, '#b8ffff')
    c.outline_alpha(); glow(c, cyan, 1); return c

def paint_cart():  # designer
    c = C(30, 33); frame = '#d9a3c3'
    c.box(0, 12, 30, 5, '#f3efe6'); c.box(0, 24, 30, 5, '#f3efe6')
    c.r(1, 12, 2, 20, frame); c.r(27, 12, 2, 20, frame)
    for i, col in enumerate(['#f5a8c8', '#9bf6ff', '#ffd6a5', '#bdb2ff', '#caffbf']):
        x = 2 + i*5; c.r(x, 4, 5, 8, '#ece8e0'); c.r(x, 4, 5, 3, col); c.r(x, 7, 1, 4, lt('#ece8e0', .5))
    c.line(6, 4, 3, 0, '#7a5a3a'); c.p(3, 0, '#f5a8c8'); c.line(21, 4, 24, 0, '#7a5a3a'); c.p(24, 0, '#9bf6ff')
    for i, col in enumerate(['#9bf6ff', '#f5a8c8', '#caffbf']): c.r(4+i*8, 19, 6, 5, col); c.r(4+i*8, 19, 6, 1, lt(col, .4))
    c.circ(4, 31, 1.5, '#333'); c.circ(25, 31, 1.5, '#333')
    c.outline_alpha(); glow(c, '#f5a8c8', 1); return c

# ---------------- pot 24x31 ----------------
def mech_plant():  # MEGATRON
    c = C(24, 31)
    for (x0, x1, y1) in [(12, 5, 4), (12, 12, 1), (12, 19, 5)]:
        c.line(x0, 21, x1, y1+4, '#6a6e7c', 2)
        c.r(x1-1, y1+1, 4, 4, RED); c.r(x1, y1+2, 1, 1, '#ffc0c8')
    c.line(12, 14, 7, 11, '#6a6e7c'); c.line(12, 12, 17, 10, '#6a6e7c')
    c.box(4, 20, 16, 11, GM2); c.r(5, 22, 14, 1, PUR); emblem(c, 7, 23, lt(GM2, .45), RED) if False else None
    c.r(9, 25, 6, 3, '#15161c'); c.r(11, 26, 2, 1, ENG)
    c.outline_alpha(); glow(c, RED, 1); return c

# ---------------- boss platform (rug slot 373x179 css -> 186x90 cells) ----------------
def hex_platform():
    W, H = 186, 90; c = C(W, H)
    def hexpoly(inset):
        return [(8+inset*1.6, 45), (50+inset, 4+inset), (136-inset, 4+inset), (178-inset*1.6, 45), (136-inset, 86-inset), (50+inset, 86-inset)]
    def inside(px, py, poly):
        n = len(poly); ins = False; j = n-1
        for i in range(n):
            xi, yi = poly[i]; xj, yj = poly[j]
            if (yi > py) != (yj > py) and px < (xj-xi)*(py-yi)/(yj-yi+1e-9)+xi: ins = not ins
            j = i
        return ins
    layers = [(0, PUR), (2, dk(PUR, .35)), (4, GM2), (7, GM), (18, '#23252d'), (30, '#1c1d24')]
    for y in range(H):
        for x in range(W):
            col = None
            for inset, lc in layers:
                if inside(x+.5, y+.5, hexpoly(inset)): col = lc
            if col: c.p(x, y, col)
    # panel seams radiating from centre
    for (vx, vy) in hexpoly(7): c.line(93, 45, vx, vy, '#1a1b21')
    c.ell(93, 45, 34, 16, '#1c1d24')
    for a in range(0, 360, 3):  # energon ring
        r = math.radians(a); c.p(93 + math.cos(r)*40, 45 + math.sin(r)*19, ENG if a % 12 else lt(ENG, .5))
    for (vx, vy) in hexpoly(1):  # red corner lights
        c.r(vx-2, vy-1, 4, 3, RED); c.p(vx-1, vy, '#ffc0c8')
    for x in range(58, 130, 8): c.r(x, 6, 3, 1, lt(PUR, .4)); c.r(x, 83, 3, 1, dk(PUR, .1))
    emblem(c, 20, 36, '#3a3d4a', RED, 2); emblem(c, 144, 36, '#3a3d4a', RED, 2)
    glow(c, PUR, 2); return c

# ---------------- desk accessories 12x12 ----------------
def d_energon():
    c = C(12, 12); c.r(2, 4, 8, 7, '#15b7d8'); c.r(4, 2, 8, 1, lt(ENG, .4)); c.r(3, 3, 8, 1, lt(ENG, .3)); c.r(4, 6, 3, 3, lt(ENG, .3)); c.p(4, 6, '#fff')
    c.outline_alpha(); glow(c, ENG, 1); return c
def d_emblem():
    c = C(12, 12); c.r(0, 0, 12, 12, GM2); emblem(c, 0, 0, PUR, RED); c.outline_alpha(); return c

TALL2 = {'energon_pylon': energon_pylon, 'server_rack': lambda: rack('#39ff9c', '#2ee6e6'), 'easel': easel2, 'tall_bookcase': bookcase2,
         'softbox': softbox, 'data_totem': kpi_totem, 'floor_globe': globe2, 'test_rig': test_rig,
         'noc_rack': lambda: rack('#ff8a1f', '#3ecf6e', True, '#2b2724'), 'flip_chart': flipchart2, 'growth_kiosk': growth_kiosk}
UNIT2 = {'energon_cubes': energon_cubes, 'neon_fridge': neon_fridge2, 'paint_cart': paint_cart}
POT2 = {'mech_plant': mech_plant}
RUG2 = {'hex_platform': hex_platform}
DESK2 = {'d_energon': d_energon, 'd_emblem': d_emblem}
