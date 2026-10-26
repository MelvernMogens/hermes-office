"""EoM portraits per theme: 42x42 cells (same canvas/scale as eom_megatron). Original mascot busts, no IP."""
from px import C, OUT, dk, lt, mix

SKIN = {'light': '#f1c7a0', 'tan': '#d9a577', 'mid': '#b97d52', 'brown': '#8d5a3a', 'deep': '#5e3a26'}

def base(bg_top, bg_bot, skin, shirt, hair=None, hairstyle='short'):
    c = C(42, 42)
    for y in range(42): c.r(0, y, 42, 1, mix(bg_top, bg_bot, y/41))
    s = SKIN[skin]; sd = dk(s, .22)
    # shoulders / shirt
    c.ell(21, 42, 19, 10, shirt); c.r(2, 38, 38, 4, shirt)
    c.ell(21, 42, 17, 8, lt(shirt, .06))
    # neck
    c.r(17, 26, 8, 8, sd); c.r(18, 26, 6, 6, s)
    # head
    c.ell(21, 17, 9, 10.5, s)
    c.r(12, 16, 2, 4, s); c.r(28, 16, 2, 4, s)                  # ears
    c.p(12, 18, sd); c.p(29, 18, sd)
    c.r(24, 13, 5, 12, mix(s, sd, .35))                          # side shading
    c.r(15, 26, 12, 1, sd)                                       # jaw shadow
    # face
    c.r(16, 17, 2, 2, '#1a1410'); c.r(24, 17, 2, 2, '#1a1410'); c.p(16, 17, '#ffffff'); c.p(24, 17, '#ffffff')
    c.r(15, 15, 4, 1, dk(s, .45)); c.r(23, 15, 4, 1, dk(s, .45))    # brows
    c.r(20, 19, 2, 3, sd); c.r(18, 23, 6, 1, dk(s, .45)); c.r(19, 24, 4, 1, mix(s, '#c0504a', .35))
    if hair:
        h = hair; hl = lt(h, .18)
        if hairstyle == 'short':
            c.ell(21, 9, 10, 5, h); c.r(11, 9, 3, 7, h); c.r(28, 9, 3, 7, h); c.r(15, 6, 8, 1, hl)
        elif hairstyle == 'long':
            c.ell(21, 9, 10, 5, h); c.r(10, 9, 4, 20, h); c.r(28, 9, 4, 20, h); c.r(15, 6, 8, 1, hl)
        elif hairstyle == 'bun':
            c.ell(21, 9, 10, 5, h); c.circ(21, 3, 3, h); c.r(11, 9, 3, 6, h); c.r(28, 9, 3, 6, h); c.p(20, 2, hl)
        elif hairstyle == 'curly':
            for (x, y) in [(13, 9), (17, 6), (21, 5), (25, 6), (29, 9), (12, 13), (30, 13), (15, 7), (27, 7)]: c.circ(x, y, 3, h)
            c.p(20, 4, hl); c.p(26, 5, hl)
        elif hairstyle == 'white':
            c.r(11, 10, 3, 8, h); c.r(28, 10, 3, 8, h); c.ell(21, 8, 8, 3, h)
            for x in (11, 13, 29, 31): c.p(x, 9, lt(h, .2))
        elif hairstyle == 'beard':
            c.ell(21, 9, 10, 5, h); c.r(11, 9, 3, 7, h); c.r(28, 9, 3, 7, h)
            c.ell(21, 25, 8, 4, h); c.r(18, 23, 6, 1, dk(s, .45))
    return c

def glasses(c, col, rnd=False, lens=None):
    for x in (14, 22):
        if rnd: c.ring(x+2.5, 18, 3, col)
        else: c.ol(x, 16, 6, 4, col)
        if lens: c.r(x+1, 17, 4, 2, lens)
    c.r(20, 17, 2, 1, col); c.r(12, 17, 2, 1, col); c.r(28, 17, 2, 1, col)

def coder():
    c = base('#0e2a22', '#07110e', 'mid', '#1f2a2e', '#1a1410', 'short')
    c.ell(21, 11, 12, 9, '#26343a'); c.r(9, 11, 4, 22, '#26343a'); c.r(29, 11, 4, 22, '#26343a')   # hood
    c.ell(21, 17, 8.5, 9.5, SKIN['tan']); c.r(24, 13, 5, 11, mix(SKIN['tan'], dk(SKIN['tan'], .22), .35))  # face re-drawn inside hood
    c.ell(21, 10, 8, 3, '#1a1410'); c.r(14, 12, 3, 2, '#1a1410'); c.r(25, 12, 3, 2, '#1a1410')      # fringe (above brows)
    c.r(15, 15, 4, 1, '#5a3a22'); c.r(23, 15, 4, 1, '#5a3a22')
    c.r(20, 19, 2, 3, dk(SKIN['tan'], .22)); c.r(18, 23, 6, 1, dk(SKIN['tan'], .45))
    glasses(c, '#111', lens='#0a2a1a'); c.r(15, 17, 3, 1, '#39ff9c'); c.r(23, 18, 3, 1, '#39ff9c'); c.p(16, 18, '#39ff9c')
    c.r(10, 8, 22, 2, '#111'); c.r(8, 14, 4, 7, '#111'); c.r(30, 14, 4, 7, '#111'); c.r(8, 15, 1, 5, '#39ff9c'); c.r(33, 15, 1, 5, '#39ff9c')
    c.line(10, 21, 16, 25, '#111'); c.r(16, 25, 2, 1, '#39ff9c')
    c.r(18, 34, 1, 5, '#d8d8d8'); c.r(24, 34, 1, 5, '#d8d8d8')
    return c

def designer():
    c = base('#2a1f36', '#120e18', 'light', '#3a2c48', '#7a3a2a', 'long')
    c.ell(20, 8, 12, 4, '#e8779f'); c.r(9, 9, 22, 2, dk('#e8779f', .2)); c.r(20, 3, 2, 2, dk('#e8779f', .3)); c.r(13, 6, 6, 1, lt('#e8779f', .3))
    c.r(26, 23, 2, 2, '#f5a8c8'); c.r(15, 23, 2, 2, '#f5a8c8') if False else None
    c.line(32, 40, 36, 24, '#c08a55', 2); c.r(35, 21, 3, 4, '#f5a8c8')                 # brush
    c.r(30, 36, 5, 5, lt(SKIN['light'], .0) if False else SKIN['light'])                # hand
    for (x, y, col) in [(6, 34, '#9bf6ff'), (9, 36, '#caffbf'), (5, 38, '#ffd6a5')]: c.r(x, y, 2, 2, col)   # paint on shirt
    return c

def content():
    c = base('#2e2014', '#140d08', 'tan', '#5a3a1e', '#3a2616', 'bun')
    glasses(c, '#c9a55a')
    c.line(30, 12, 35, 6, '#e8b04a', 2); c.r(35, 5, 2, 2, '#f2c0b0'); c.p(30, 12, '#2a2a2a')     # pencil behind ear
    c.r(16, 32, 10, 10, '#e8dfc8'); c.r(17, 33, 8, 1, '#b8a888'); c.r(17, 36, 6, 1, '#b8a888')    # cardigan collar/shirt
    c.r(14, 32, 2, 10, '#7a4a26'); c.r(26, 32, 2, 10, '#7a4a26')
    return c

def video():
    c = base('#241836', '#0e0a16', 'brown', '#1c1a20', '#1a1410', 'short')
    c.ell(21, 9, 11, 4, '#2a2236'); c.r(9, 9, 10, 3, '#2a2236'); c.r(5, 10, 6, 2, '#2a2236'); c.r(22, 6, 2, 2, '#b36bff')   # backwards cap
    c.r(29, 15, 4, 6, '#15131a'); c.line(31, 21, 24, 25, '#15131a'); c.r(23, 25, 2, 1, '#ff3b3b')     # earpiece + boom mic
    c.r(6, 34, 8, 4, '#15131a'); c.r(7, 35, 2, 2, '#ff3b3b')                                           # radio clip
    c.r(18, 36, 6, 3, '#b36bff'); c.txt(18, 36, '', '#fff')
    return c

def analyst():
    c = base('#0e1a2e', '#070b14', 'light', '#1d2636', '#c9a060', 'short')
    for i, hv in enumerate([4, 7, 5, 10, 13]): c.r(2+i*3, 30-hv, 2, hv, '#1f4a7a' if i < 4 else '#4a3a14')   # chart bg left
    c.line(31, 12, 34, 8, '#2e6fd8'); c.line(34, 8, 37, 10, '#2e6fd8'); c.line(37, 10, 40, 4, '#2e6fd8')
    glasses(c, '#4da3ff')
    c.r(18, 32, 6, 10, '#e8eef5'); c.r(20, 33, 2, 9, '#2e6fd8'); c.r(19, 32, 4, 2, '#1f4a8a')          # shirt + tie
    c.r(34, 30, 1, 8, '#ffc24d')                                                                       # pen in pocket
    return c

def research():
    c = base('#15241a', '#080e0a', 'light', '#1a1a1a', '#e8e6e0', 'white')
    c.r(8, 3, 26, 3, '#1a1a1a'); c.r(12, 6, 18, 3, '#1a1a1a'); c.r(20, 2, 2, 1, '#c9a55a'); c.line(32, 5, 35, 13, '#c9a55a'); c.r(34, 13, 2, 2, '#c9a55a')   # mortarboard
    glasses(c, '#c9a55a', rnd=True)
    c.ell(21, 25, 6, 3, '#e8e6e0'); c.r(18, 23, 6, 1, '#8a6a5a')                                         # white beard
    c.r(17, 32, 8, 10, '#2f5d3a'); c.r(16, 32, 2, 10, '#c9a55a'); c.r(24, 32, 2, 10, '#c9a55a')           # gown trim
    return c

def qa():
    c = base('#261616', '#0e0a0a', 'deep', '#e8e8e8', '#1a1410', 'curly')
    c.r(10, 15, 22, 2, '#e5484d')
    for x in (13, 22): c.r(x, 14, 8, 6, '#2c3035'); c.r(x+1, 15, 6, 4, '#7fe0a0'); c.p(x+2, 15, '#e8fff0')
    c.r(18, 32, 6, 10, '#2a3a4a'); c.line(15, 32, 20, 41, '#c8c8c8'); c.line(27, 32, 22, 41, '#c8c8c8')  # lab coat lapels
    c.r(28, 33, 4, 5, '#d0d0d0'); c.r(29, 33, 1, 3, '#e5484d'); c.r(30, 33, 1, 3, '#3ecf6e')             # pocket pens
    return c

def ops():
    c = base('#2a1a0c', '#100a06', 'tan', '#ff8a1f', '#5a3a22', 'beard')
    c.ell(21, 8, 12, 6, '#f0c419'); c.r(8, 10, 26, 2, dk('#f0c419', .2)); c.r(20, 2, 2, 8, lt('#f0c419', .3))   # hard hat
    for y in (35, 39): c.r(4, y, 34, 2, '#e8e8a0')                                                       # reflective stripes
    c.r(18, 32, 6, 10, '#3a3531')
    c.r(29, 15, 3, 5, '#2b2724')
    return c

def pm():
    c = base('#0e2424', '#061010', 'brown', '#26343a', '#1a1410', 'long')
    c.line(15, 30, 21, 38, '#2ec4b6'); c.line(27, 30, 21, 38, '#2ec4b6')
    c.r(18, 37, 7, 5, '#f4f1ea'); c.r(19, 38, 3, 1, '#2ec4b6')                                           # badge
    c.r(29, 29, 10, 13, '#8a5a30'); c.r(30, 31, 8, 11, '#f4f1ea'); c.r(32, 28, 4, 2, '#888')              # clipboard
    for y in (33, 36, 39): c.p(31, y, '#3ecf6e'); c.r(33, y, 4, 1, '#999')
    return c

def growth():
    c = base('#1a2410', '#0a0e06', 'mid', '#343a28', '#2a1c10', 'short')
    c.ell(20, 9, 11, 4, '#a3e635'); c.r(9, 10, 22, 2, dk('#a3e635', .2)); c.r(19, 11, 15, 2, '#5f8a1c')  # cap w/ brim
    for i in range(8): c.r(30+i, 30 - (2+i)//2, 1, 3+i, '#a3e635')                                        # mini megaphone
    c.r(27, 29, 3, 3, '#2a2f22'); c.r(36, 22, 1, 1, '#e9ffb8'); c.r(39, 25, 1, 1, '#e9ffb8'); c.r(38, 33, 1, 1, '#e9ffb8')
    c.r(10, 34, 6, 5, '#232820'); c.txt(10, 34, '', '#a3e635'); c.r(11, 36, 4, 1, '#a3e635')
    return c

ALL = {'coder': coder, 'designer': designer, 'content': content, 'video': video, 'analyst': analyst,
       'research': research, 'qa': qa, 'ops': ops, 'pm': pm, 'growth': growth}
