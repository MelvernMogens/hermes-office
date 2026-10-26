"""CityWindow slot replacements: 100x80 cells (= 200x160 css at (319,30))."""
from px import C, OUT, dk, lt, mix

W, H = 100, 80

def bezel(c, col='#1a1d23', trim=None):
    c.box(0, 0, W, H, col)
    c.r(4, 4, W-8, H-8, '#05070a'); c.ol(3, 3, W-6, H-6, dk(col, .5))
    if trim: c.r(1, H-3, W-2, 1, trim); c.r(1, 1, W-2, 1, trim)

def hq_map():  # default / MEGATRON: command screen, world map, gold blips
    c = C(W, H); gold = '#e0b54a'; navy = '#1c2744'
    c.box(0, 0, W, H, navy); c.r(1, 1, W-2, 1, gold); c.r(1, H-2, W-2, 1, dk(gold, .3))
    sx, sy, sw, sh = 4, 12, 92, 60
    c.r(sx, sy, sw, sh, '#081226'); c.ol(sx-1, sy-1, sw+2, sh+2, OUT)
    for gx in range(sx, sx+sw, 8): c.r(gx, sy, 1, sh, '#0f1f3d')
    for gy in range(sy, sy+sh, 8): c.r(sx, gy, sw, 1, '#0f1f3d')
    land, land2 = '#2c6d8f', '#3a88ad'
    for (cx, cy, rx, ry) in [(22, 30, 11, 7), (16, 25, 6, 4), (31, 51, 5, 9), (29, 44, 4, 3), (50, 26, 6, 4), (53, 43, 7, 10),
                             (70, 29, 14, 8), (82, 36, 5, 4), (80, 57, 6, 4), (75, 44, 3, 3), (40, 18, 3, 2)]:
        c.ell(sx+cx, sy+cy-12+8, rx, ry, land)
    for (cx, cy, rx, ry) in [(20, 24, 6, 3), (68, 24, 8, 3), (51, 38, 4, 4)]:
        c.ell(sx+cx, sy+cy-12+8, rx, ry, land2)
    hq = (sx+75, sy+40)
    for tx, ty in [(sx+22, sy+24), (sx+50, sy+22), (sx+31, sy+50), (sx+82, sy+54), (sx+56, sy+44)]:
        c.line(hq[0], hq[1], tx, ty, dk(gold, .45))
        c.r(tx-1, ty-1, 3, 3, gold); c.p(tx, ty, '#fff4c8')
    c.ring(hq[0], hq[1], 5, gold); c.ring(hq[0], hq[1], 8, dk(gold, .5)); c.r(hq[0]-1, hq[1]-1, 3, 3, '#fff4c8')
    c.r(4, 3, 92, 7, '#111a30'); c.txt(6, 4, 'COMMAND', gold); c.txt(66, 4, 'LIVE', '#ff5a5a'); c.r(83, 5, 3, 3, '#ff5a5a')
    for i in range(5): c.r(88+i*0, 4, 1, 1, gold)
    c.r(4, 73, 92, 4, '#111a30')
    for i, wv in enumerate([10, 16, 7, 22, 12]): c.r(6+i*18, 74, wv, 2, gold if i % 2 == 0 else '#3a88ad')
    return c

def coder_terminal():
    c = C(W, H); g = '#39ff9c'; gd = '#1d8f5a'
    c.box(0, 0, W, H, '#16191e')
    c.r(4, 4, 92, 66, '#040806'); c.ol(3, 3, 94, 68, OUT)
    c.r(4, 4, 92, 6, '#11161a'); [c.r(6+i*5, 6, 3, 2, col) for i, col in enumerate(['#ff5f57', '#febc2e', '#28c840'])]
    c.txt(24, 5, 'ZSH - HERMES', '#5b6b66')
    y = 13
    rows = [('$ GIT PULL', g), ('> 3 FILES', gd), ('$ NPM TEST', g), ('> PASS 42', '#8affc8'), ('$ DEPLOY', g)]
    for t, col in rows: c.txt(6, y, t, col); y += 7
    c.r(49, 12, 1, 56, '#1a2a22')  # split pane divider
    # syntax-highlighted code bars on the right pane
    code = [(53, 6, '#ff79c6'), (53, 14, '#8be9fd'), (57, 10, '#50fa7b'), (57, 18, '#f1fa8c'), (61, 12, '#8be9fd'),
            (57, 8, '#ff79c6'), (53, 4, '#6272a4'), (53, 16, '#50fa7b'), (57, 22, '#f1fa8c'), (53, 10, '#ff79c6')]
    for i, (x, wv, col) in enumerate(code):
        c.r(x, 13+i*5, wv, 2, col)
        if x+wv+2 < 92: c.r(x+wv+2, 13+i*5, min(8 - (i % 3)*2, 92-(x+wv+2)), 2, '#4a5a55')
    c.r(34, 13+4*7, 3, 5, g)  # cursor
    c.r(6, 50, 40, 1, '#1a2a22')
    for i, hv in enumerate([3, 5, 4, 7, 6, 9, 8, 11, 7, 12]): c.r(7+i*4, 66-hv, 3, hv, gd)  # CPU mini graph
    # RGB LED strip under the bezel
    rgb = ['#ff3b5c', '#ff9f1c', '#ffe14d', '#39ff9c', '#2ee6e6', '#3b82ff', '#b04dff']
    for x in range(2, 98):
        c.p(x, 74, rgb[(x*len(rgb))//100]); c.p(x, 75, dk(rgb[(x*len(rgb))//100], .45))
    c.r(47, 71, 6, 2, '#2a2f36')
    return c

def designer_swatches():
    c = C(W, H); pinkish = '#d9a3c3'
    c.box(0, 0, W, H, '#2a2431'); c.r(2, 2, W-4, 1, pinkish)
    c.r(4, 4, 92, 72, '#211c27')
    cols = ['#f5a8c8', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff']
    for i, col in enumerate(cols):
        x = 7 + (i % 4)*22; y = 7 + (i//4)*35 + (1 if i in (1, 6) else 0) - (1 if i in (3, 4) else 0)
        c.box(x, y, 19, 30, '#ece7df', hi='#fbf8f3', sh='#c9c2b7')
        c.r(x+2, y+2, 15, 17, col); c.r(x+2, y+2, 15, 1, lt(col, .4)); c.r(x+2, y+18, 15, 1, dk(col, .15))
        c.r(x+3, y+22, 9, 1, '#6f6778'); c.r(x+3, y+25, 6, 1, '#a39bab')
        c.r(x+8, y-1, 3, 3, '#ff6fa6' if i % 2 else '#7ad3ff'); c.p(x+8, y-1, '#ffffff')
    return c

def content_storyboard():
    c = C(W, H); wood = '#6b4423'
    c.frame(0, 0, W, H, wood, 4)
    c.r(4, 4, 92, 72, '#7a5230')
    for i in range(0, 700, 7): c.p(4 + (i*13) % 92, 4 + (i*7) % 72, '#6c4628')  # cork speckle
    heads = [('HOOK', '#e85d4a'), ('BODY', '#e0a060'), ('CTA', '#7fbf6a')]
    pts = []
    for ci, (h, col) in enumerate(heads):
        x = 8 + ci*30
        c.box(x, 7, 26, 9, col); c.ctxt(x+13, 9, h, '#1a1208')
        for ri in range(3):
            y = 20 + ri*18
            c.box(x+1, y, 24, 15, '#efe3c8', hi='#fff7e4', sh='#cdbd9c')
            for li in range(3): c.r(x+4, y+4+li*3, 18 - ((ri+li+ci) % 3)*4, 1, '#8a7a5c')
            c.r(x+12, y-1, 2, 2, '#d63a3a'); pts.append((x+13, y))
    for a, b in [(0, 4), (4, 8), (1, 5)]:
        c.line(pts[a][0], pts[a][1], pts[b][0], pts[b][1], '#c0392b')
    return c

def video_timeline():
    c = C(W, H); pu = '#b36bff'
    c.box(0, 0, W, H, '#1a1622')
    c.r(4, 4, 92, 72, '#0a0810'); c.ol(3, 3, 94, 74, OUT)
    # preview monitor
    px0, py0, pw, ph = 22, 6, 56, 34
    sky = ['#2b1650', '#3d1c6b', '#5a2585', '#8a3a9a', '#c05a8a', '#f08a6a']
    for i in range(ph): c.r(px0, py0+i, pw, 1, sky[min(len(sky)-1, i*len(sky)//ph)])
    c.circ(px0+38, py0+24, 5, '#ffd08a')
    for x in range(pw): c.r(px0+x, py0+ph-5 - (abs((x % 14)-7))//2, 1, 6, '#1a0f2a')
    c.ol(px0-1, py0-1, pw+2, ph+2, '#3a3348')
    c.r(px0+2, py0+2, 3, 3, '#ff3b3b'); c.txt(px0+7, py0+1, 'REC', '#ffffff'); c.txt(px0+pw-22, py0+ph-7, '00:12', '#ffffff')
    # timeline
    ty = 44
    c.r(5, ty-2, 90, 1, '#2a2436')
    for t in range(0, 90, 6): c.r(5+t, ty-2, 1, 2, '#554b66')
    tracks = [[(6, 20, '#b36bff'), (28, 26, '#8f4de0'), (56, 36, '#c77dff')],
              [(12, 14, '#ff6fb5'), (30, 18, '#ff6fb5'), (62, 22, '#e0559c')],
              [(6, 88, '#2ec4b6')]]
    for ti, tr in enumerate(tracks):
        y = ty + 2 + ti*9
        c.r(5, y, 90, 7, '#14111b')
        for x, wv, col in tr:
            c.box(x, y, wv, 7, col, out=dk(col, .6))
            if ti == 2:
                for xx in range(x+1, x+wv-1):
                    a = [1, 2, 3, 2, 1, 2, 3, 3, 1][xx % 9]; c.r(xx, y+3-a//2, 1, a, dk(col, .45))
    c.r(47, ty-4, 1, 34, '#ff3b3b'); c.r(46, ty-5, 3, 2, '#ff3b3b')
    return c

def analyst_dashboard():
    c = C(W, H); b = '#4da3ff'; b2 = '#2e6fd8'; b3 = '#9fd0ff'; amber = '#ffc24d'
    c.box(0, 0, W, H, '#161d29')
    c.r(4, 4, 92, 72, '#07101c'); c.ol(3, 3, 94, 74, OUT)
    def panel(x, y, w, h): c.r(x, y, w, h, '#0d1a2c'); c.ol(x, y, w, h, '#1c3150')
    panel(6, 6, 34, 20); c.txt(9, 8, 'VIEWS', '#6f8fb8'); c.txt(9, 15, '1.2M', b3, 2)
    panel(42, 6, 52, 20)
    for i, hv in enumerate([5, 8, 6, 11, 9, 13, 12, 16]):
        c.r(45+i*6, 24-hv, 4, hv, b if i < 7 else amber); c.r(45+i*6, 24-hv, 4, 1, b3 if i < 7 else '#ffe3a3')
    panel(6, 28, 58, 46)
    pts = [(9, 66), (16, 60), (23, 63), (30, 52), (37, 55), (44, 44), (51, 47), (58, 36), (62, 34)]
    for gy in range(34, 72, 8): c.r(8, gy, 54, 1, '#132640')
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        c.line(x0, y0, x1, y1, b, 1)
    for (x, y) in pts: c.r(x-1, y-1, 2, 2, b3)
    c.txt(9, 30, 'RETENTION', '#6f8fb8')
    panel(66, 28, 28, 46)
    cx, cy, rr = 80, 46, 10
    import math
    for y in range(cy-rr-1, cy+rr+2):
        for x in range(cx-rr-1, cx+rr+2):
            d = math.hypot(x-cx, y-cy)
            if 5 < d <= rr:
                a = (math.degrees(math.atan2(y-cy, x-cx)) + 450) % 360
                c.p(x, y, b if a < 200 else (b2 if a < 300 else amber))
    c.ctxt(80, 61, '64%', b3); c.ctxt(80, 67, 'CTR', '#6f8fb8')
    return c

def research_library():
    c = C(W, H); wood = '#4a3020'; brass = '#c9a55a'
    c.box(0, 0, W, H, wood, hi='#5e3e29', sh='#2e1d12')
    books = ['#2f5d3a', '#6b1f24', '#1f3553', '#8a6a3a', '#3f7a4a', '#4a2a4f', '#7a2f2a', '#2a4a5a']
    for si in range(3):
        y0 = 4 + si*25
        c.r(3, y0, 94, 22, '#1d130c')
        x = 4; k = si*3
        while x < 94:
            wv = 4 + (k*7) % 3; hv = 17 + (k*5) % 5
            if si == 1 and 38 <= x <= 52:  # globe nook
                c.circ(45, y0+10, 6, '#2c6d8f'); c.ell(43, y0+8, 3, 2, '#3f7a4a'); c.ell(48, y0+12, 2, 2, '#3f7a4a')
                c.ring(45, y0+10, 7, brass); c.r(44, y0+17, 3, 4, brass); c.r(41, y0+20, 9, 2, dk(brass, .2))
                x = 54; continue
            if x + wv > 95: break
            col = books[k % len(books)]
            c.r(x, y0+22-hv, wv, hv, col); c.r(x, y0+22-hv, 1, hv, lt(col, .18)); c.r(x+wv-1, y0+22-hv, 1, hv, dk(col, .3))
            c.r(x, y0+22-hv+3, wv, 1, brass); c.r(x, y0+19, wv, 1, dk(brass, .2))
            x += wv + (1 if k % 4 == 0 else 0); k += 1
        c.r(2, y0+22, 96, 3, '#6b4a30'); c.r(2, y0+22, 96, 1, '#86603f')
    return c

BUG = ['#...#', '.###.', '#####', '.###.', '#.#.#']
def bug_icon(c, x, y, col):
    for yy, row in enumerate(BUG):
        for xx, v in enumerate(row):
            if v == '#': c.p(x+xx, y+yy, col)

def check_icon(c, x, y, col):
    for (a, b_) in [(0, 2), (1, 3), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)]: c.r(x+a, y+b_, 1, 1, col)

def qa_bugboard():
    c = C(W, H); red = '#e5484d'; grn = '#3ecf6e'
    c.box(0, 0, W, H, '#262222')
    c.r(4, 4, 92, 72, '#1a1717')
    c.r(4, 4, 45, 9, dk(red, .35)); c.ctxt(26, 6, 'BUGS 3', '#ffd1d1')
    c.r(51, 4, 45, 9, dk(grn, .45)); c.ctxt(73, 6, 'PASS 12', '#d1ffe0')
    c.r(49, 4, 2, 72, '#0e0c0c')
    for i in range(3):
        x, y = 7 + (i % 2)*20, 16 + i*19
        c.box(x, y, 18, 16, '#f2d4d4', hi='#fff0f0', sh='#c9a3a3'); bug_icon(c, x+3, y+3, red)
        c.r(x+10, y+4, 5, 1, '#8a5a5a'); c.r(x+10, y+7, 4, 1, '#8a5a5a'); c.r(x+3, y+11, 12, 1, '#a07070')
    for i in range(6):
        x, y = 54 + (i % 2)*21, 16 + (i//2)*19
        c.box(x, y, 18, 16, '#d4f2dc', hi='#effff3', sh='#a3c9ad'); check_icon(c, x+3, y+4, grn)
        c.r(x+11, y+4, 4, 1, '#5a8a66'); c.r(x+3, y+11, 12, 1, '#70a07c')
    return c

def ops_noc():
    c = C(W, H); o = '#ff8a1f'
    c.box(0, 0, W, H, '#1f1b18')
    c.r(3, 3, 94, 6, '#141110'); c.txt(5, 4, 'NOC', o); c.txt(20, 4, 'UPTIME 99.98%', '#8fd18f')
    c.r(90, 4, 3, 3, o)
    for i in range(6):
        x, y = 3 + (i % 3)*32, 11 + (i//3)*34
        alert = i == 4
        c.box(x, y, 30, 32, '#2b2724', out=OUT)
        c.r(x+2, y+2, 26, 24, '#050606')
        if alert: c.ol(x+1, y+1, 28, 26, o); c.ol(x+2, y+2, 26, 24, dk(o, .3))
        sx, sy = x+3, y+3
        if i == 0:
            for t in range(22): c.p(sx+t, sy+14 - int(5*abs(((t*3) % 20)-10)/10), '#3ecf6e')
            c.txt(sx, sy+17, 'CPU', '#5a7a5a')
        elif i == 1:
            for t, hv in enumerate([4, 7, 5, 9, 6, 11, 8]): c.r(sx+1+t*3, sy+16-hv, 2, hv, '#4da3ff')
            c.txt(sx, sy+17, 'NET', '#5a6a8a')
        elif i == 2:
            for r_ in range(4):
                c.r(sx, sy+1+r_*5, 3, 3, '#3ecf6e' if r_ != 2 else '#ffc24d'); c.r(sx+5, sy+2+r_*5, 14 - r_*2, 1, '#6a6a6a')
        elif i == 3:
            for t in range(22): c.p(sx+t, sy+10 + int(3*((t*7) % 5)/5) - 2, '#b36bff')
            c.txt(sx, sy+17, 'MEM', '#6a5a8a')
        elif i == 4:
            c.ctxt(x+15, sy+3, '!', o, 2); c.ctxt(x+15, sy+15, 'ALERT', o)
        else:
            c.r(sx+2, sy+2, 18, 12, '#0d1a12')
            for t in range(6): c.r(sx+3+t*3, sy+3 + (t % 3)*3, 2, 2, '#3ecf6e')
            c.txt(sx, sy+17, 'DB', '#5a7a5a')
        c.r(x+13, y+27, 4, 3, '#3a3531'); c.r(x+22, y+28, 3, 2, '#3ecf6e' if not alert else o)
    return c

def pm_kanban():
    c = C(W, H); teal = '#2ec4b6'
    c.box(0, 0, W, H, '#1a2b2b'); c.r(2, 2, W-4, 1, teal)
    c.r(4, 4, 92, 72, '#122020')
    notes = {'TODO': ['#ffd23f', '#ffd23f', '#ff8fab'], 'DOING': ['#7ae7e0', '#ffd23f'], 'DONE': ['#b5e48c', '#b5e48c', '#b5e48c', '#7ae7e0']}
    for ci, (h, ns) in enumerate(notes.items()):
        x = 6 + ci*30
        c.r(x, 6, 28, 7, '#0c1616'); c.ctxt(x+14, 7, h, teal)
        if ci: c.r(x-2, 6, 1, 68, '#274040')
        for ni, col in enumerate(ns):
            nx = x + 2 + (ni % 2)*13; ny = 16 + (ni//2)*15 + (ni % 2)*2
            c.r(nx+1, ny+1, 12, 12, dk(col, .6)); c.r(nx, ny, 12, 12, col); c.r(nx, ny, 12, 2, dk(col, .12))
            c.r(nx+2, ny+4, 7, 1, dk(col, .5)); c.r(nx+2, ny+7, 5, 1, dk(col, .5))
            if h == 'DONE': c.r(nx+7, ny+8, 3, 3, '#1e6b3a')
    c.r(6, 66, 88, 4, '#0c1616'); c.r(6, 66, 58, 4, teal); c.txt(68, 66, '66%', '#bff5ef')
    return c

def growth_chart():
    c = C(W, H); lime = '#a3e635'; ld = '#5f8a1c'
    c.box(0, 0, W, H, '#1c2216'); c.r(2, 2, W-4, 1, lime)
    c.r(4, 4, 92, 72, '#11160d')
    c.txt(8, 8, '+248%', lime, 2); c.txt(8, 20, 'FOLLOWERS', '#7d9a5a')
    for gy in range(30, 74, 8): c.r(6, gy, 88, 1, '#1b2414')
    hs = [6, 9, 8, 13, 17, 22, 28, 36]
    for i, hv in enumerate(hs):
        x = 10 + i*10
        c.r(x, 72-hv, 7, hv, ld if i < 6 else lime); c.r(x, 72-hv, 7, 1, lt(lime, .3)); c.r(x+6, 72-hv, 1, hv, dk(ld, .3))
    pts = [(13, 62), (23, 60), (33, 58), (43, 52), (53, 46), (63, 38), (73, 30), (83, 16)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]): c.line(x0, y0, x1, y1, '#e9ffb8', 1)
    c.r(80, 12, 7, 2, '#e9ffb8'); c.r(85, 12, 2, 7, '#e9ffb8')
    return c

ALL = {'hq_map': hq_map, 'coder_terminal': coder_terminal, 'designer_swatches': designer_swatches,
       'content_storyboard': content_storyboard, 'video_timeline': video_timeline, 'analyst_dashboard': analyst_dashboard,
       'research_library': research_library, 'qa_bugboard': qa_bugboard, 'ops_noc': ops_noc, 'pm_kanban': pm_kanban,
       'growth_chart': growth_chart}
