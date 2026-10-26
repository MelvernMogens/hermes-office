"""NOC/infra cleaner: 'Gus' — a BURLY technician PUSHING A WHEELED CART, not a walking humanoid
recolour. Silhouette = wide + low + long horizontally: huge barrel-chested body leaning into the
push on the LEFT half (x~4-20), low 2-wheel utility trolley carrying an oil drum, fire
extinguisher and coiled cable on the RIGHT half (x~20-39). Canvas 40x36 cells, anchor
bottom-centre (feet/wheels on row 35, whole composition centred on x=20), faces right."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Gus', 'persona': 'NOC infra tech who muscles the parts cart around and keeps the server room spotless.',
        'fx': 'oil', 'fxColor': '#8a5a1f'}

W, H = 40, 36
SKIN, SKIN_D = '#d99a6c', '#a86b45'
COVER, COVER_D, COVER_L = '#5a5148', '#37312a', '#7a6d5f'      # heavy canvas coverall (not ref's blue)
VEST, VEST_D, VEST_L = '#ff8a1f', '#c9650f', '#ffab5c'          # hi-vis orange (theme accent)
HAT, HAT_D, HAT_L = '#ff8a1f', '#c9650f', '#ffcf94'
LAMP = '#fff6c8'
BOOT, BOOT_D = '#221a12', '#120d08'
GLOVE, GLOVE_D = '#c9862f', '#8f5b1c'
CART, CART_D, CART_L = '#7c828a', '#454a50', '#9aa0a8'
WHEEL, WHEEL_D, HUB = '#161616', '#000000', '#9aa0a8'
DRUM, DRUM_D, DRUM_L = '#8a4a1f', '#5c2f10', '#b46a34'
STRIPE = '#e8b23a'
EXT, EXT_D = '#d1362f', '#8f2019'
CABLE, CABLE_L = '#2b2622', '#4a4038'
RAG, RAG_D = '#dedad0', '#b0aa98'
WRENCH, WRENCH_D = '#c9ccd1', '#8f939a'
OIL, OIL_D = '#1a130a', '#0c0904'
SPOOL, SPOOL_D, SPOOL_L = '#7a5230', '#4e3319', '#a3754c'
TOOLBOX, TOOLBOX_D = '#8a3a2a', '#5c2318'
TABLET = '#2a2620'
GLOW = '#ff8a1f'


def wheel(c, cx, cy, r, angle, jiggle=0):
    cy += jiggle
    c.circ(cx, cy, r, WHEEL_D)
    c.circ(cx, cy, r - 1, WHEEL)
    for i in range(3):
        a = angle + i * (math.pi * 2 / 3)
        c.line(cx, cy, cx + math.cos(a) * (r - 1), cy + math.sin(a) * (r - 1), HUB, 1)
    c.p(cx, cy, HUB)


def headlamp_beam(c, x, y, on):
    if not on:
        return
    for i, w in enumerate((3, 5, 7)):
        col = '#fff6c866' if i else '#fff6c8'
        c.r(x + 2 + i * 3, y - w // 2, 3, w, col)


LEGC, LEGC_D = '#736a5c', '#4a4438'   # lighter than COVER_D so legs read on dark floor


def legs(c, mode, y0):
    """mode: 0 stand-braced, 1 stride A, 2 stride B — short, THICK (burly) legs, wide stance."""
    if mode == 0:
        c.r(7, y0 + 22, 6, 9, LEGC); c.r(15, y0 + 22, 6, 9, LEGC)
        c.r(5, y0 + 30, 8, 4, BOOT); c.r(14, y0 + 30, 8, 4, BOOT)
    elif mode == 1:
        c.r(6, y0 + 21, 6, 9, LEGC); c.r(16, y0 + 23, 6, 8, LEGC)
        c.r(4, y0 + 29, 8, 4, BOOT); c.r(15, y0 + 30, 8, 4, BOOT)
    else:
        c.r(8, y0 + 23, 6, 8, LEGC); c.r(14, y0 + 21, 6, 9, LEGC)
        c.r(6, y0 + 30, 8, 4, BOOT); c.r(13, y0 + 29, 8, 4, BOOT)
    c.r(5, y0 + 33, 8, 1, BOOT_D); c.r(14, y0 + 33, 8, 1, BOOT_D)


def torso(c, y0, lean=2):
    """Barrel hips at the base, chest leaning `lean` cells forward (right) toward the cart."""
    c.box(4, y0 + 15, 17, 11, COVER, out=None, hi=COVER_L, sh=COVER_D)           # hips/belly barrel
    c.box(4 + lean, y0 + 3, 18, 14, COVER, out=None, hi=COVER_L, sh=COVER_D)     # leaning chest
    c.box(5 + lean, y0 + 3, 16, 9, VEST, out=None, hi=VEST_L, sh=VEST_D)         # hi-vis vest panel
    c.r(5 + lean, y0 + 6, 16, 1, '#e8e8e8')                                      # reflective stripe
    c.r(4, y0 + 24, 17, 2, mix(COVER_D, '#000000', .2))                          # belt


def head(c, y0, lean=2, blink=False):
    hx = 8 + lean
    c.box(hx, y0 - 4, 11, 8, SKIN, out=None, hi=lt(SKIN, .2), sh=SKIN_D)
    c.r(hx + 8, y0 - 1, 1, 1, SKIN_D if blink else '#1a1a1a')
    c.r(hx + 7, y0 + 2, 3, 1, '#8a5a3a')
    c.box(hx - 2, y0 - 8, 14, 5, HAT, out=None, hi=HAT_L, sh=HAT_D)              # hard hat, brim right
    c.r(hx + 10, y0 - 4, 4, 2, HAT_D)
    c.r(hx - 1, y0 - 8, 4, 1, HAT_L)
    c.circ(hx + 13, y0 - 6, 1, LAMP)                                             # headlamp lens
    return hx + 13, y0 - 6


def arms_to_cart(c, y0, lean, hx, hy):
    """Two thick arms bridging from the leaning shoulder to the cart handle."""
    sx, sy = 9 + lean, y0 + 8
    c.line(sx, sy, hx, hy, VEST, 4)
    c.line(sx, sy + 5, hx, hy + 4, VEST_D, 3)
    c.r(hx - 1, hy - 1, 4, 4, GLOVE); c.r(hx - 1, hy + 3, 4, 3, GLOVE_D)


def cart(c, jig=0, wheel_angle=0.0, spin=True):
    """Low 2-wheel utility trolley on the RIGHT half, x ~20-39."""
    c.r(21, 15, 2, 15, CART_D)                                                   # push-handle post
    c.r(20, 14, 4, 2, CART)
    c.box(20, 28, 19, 4, CART, out=None, hi=CART_L, sh=CART_D)                   # deck
    for wx in (25, 34):
        wheel(c, wx, 33, 3, wheel_angle if spin else 0.4, 0)
    c.box(23, 13 + jig, 8, 15, DRUM, out=None, hi=DRUM_L, sh=DRUM_D)             # oil drum
    c.ell(27, 13 + jig, 4, 1.4, lt(DRUM, .2))
    c.r(23, 19 + jig, 8, 2, STRIPE)
    c.box(32, 16 + jig, 4, 12, EXT, out=None, hi=lt(EXT, .25), sh=EXT_D)         # fire extinguisher
    c.r(33, 14 + jig, 2, 2, '#8a8f96')
    for i, rad in enumerate((3, 2, 1)):                                          # coiled cable
        c.ring(36 - i, 25 + jig, rad, lt(CABLE_L, .15) if i % 2 == 0 else CABLE_L, 1)


def gus(c, y0=4, bob=0, legmode=0, lean=2, blink=False, beam=True):
    legs(c, legmode, y0 - bob)
    torso(c, y0 - bob, lean)
    lx, ly = head(c, y0 - bob, lean, blink)
    headlamp_beam(c, lx, ly, beam)
    hx, hy = 21, y0 - bob + 12
    arms_to_cart(c, y0 - bob, lean, hx, hy)


def walk():
    out = []
    for i, (legmode, bob, jig, beam) in enumerate(((1, 0, 0, True), (0, 1, -1, False), (2, 0, 0, True), (0, 1, -1, False))):
        c = C(W, H)
        cart(c, jig=jig, wheel_angle=i * 1.1, spin=True)
        gus(c, 4, bob, legmode, lean=2, blink=(i == 2), beam=beam)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    out = []
    for i, tx in enumerate((19, 22, 20, 17)):
        c = C(W, H)
        cart(c, jig=0, wheel_angle=0.4, spin=False)                              # cart parked
        legs(c, 1, 4)
        torso(c, 8, lean=3)
        lx, ly = head(c, 8, lean=3, blink=(i == 2))
        headlamp_beam(c, lx, ly, i % 2 == 0)
        # arm reaches down from shoulder to the wrench/rag scrubbing the spill
        sx, sy = 12, 16
        c.line(sx, sy, tx, 30, VEST, 3)
        c.r(tx - 2, 29, 6, 3, RAG); c.r(tx - 1, 31, 4, 1, RAG_D)
        c.r(tx + 3, 27, 2, 5, WRENCH); c.r(tx + 3, 27, 2, 1, WRENCH_D)
        c.ell(21, 34, 8, 2, OIL); c.ell(21, 34, 5, 1, OIL_D)                      # oil puddle underfoot
        c.outline_alpha(); out.append(c)
    return out


def seat():
    c = C(W, H)
    x0, w = 6, 22
    c.box(x0, 15, w, 20, SPOOL, out=None, hi=SPOOL_L, sh=SPOOL_D)                # cable spool drum
    c.ell(x0 + w / 2, 15, w / 2, 3, lt(SPOOL, .2))
    for r in (9, 6, 3):
        c.ring(x0 + w / 2, 15 + 8, r, SPOOL_D, 1)
    c.r(x0, 21, w, 2, SPOOL_D)
    for gx in range(x0 + 2, x0 + w - 1, 4):
        c.r(gx, 15, 1, 20, mix(SPOOL_D, '#000000', .15))
    c.box(30, 27, 8, 8, TOOLBOX, out=None, hi=lt(TOOLBOX, .2), sh=TOOLBOX_D)      # small toolbox beside it
    c.r(31, 26, 6, 2, CART_D); c.r(33, 27, 2, 1, CART_L)
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        c.r(9, 15, 8, 10, COVER_D); c.r(19, 15, 8, 10, COVER_D)                  # thighs over the spool
        c.r(8, 24, 8, 4, BOOT); c.r(18, 24, 8, 4, BOOT)
        c.r(8, 27, 8, 1, BOOT_D); c.r(18, 27, 8, 1, BOOT_D)
        y0 = 6
        c.box(9, y0, 18, 12, COVER, out=None, hi=COVER_L, sh=COVER_D)
        c.box(10, y0, 15, 8, VEST, out=None, hi=VEST_L, sh=VEST_D)
        c.r(10, y0 + 3, 15, 1, '#e8e8e8')
        c.r(9, y0 + 2, 2, 7, VEST_D)
        if k == 0:
            hx, hy = head(c, y0 - 2, lean=1, blink=False)
            headlamp_beam(c, hx, hy, False)
            c.r(25, y0 + 3, 4, 6, CART); c.r(25, y0 + 2, 4, 1, CART_L)           # thermos
            c.line(24, y0 + 6, 26, y0 + 4, VEST, 2)
            for i in range(2):
                c.r(26 - i, y0 - 1 - i * 2, 1, 2, '#dfe6ea')
        else:
            # hard-hat tipped back, tablet glowing orange
            hx, hy = head(c, y0 - 1, lean=1, blink=True)
            c.r(hx - 12, y0 - 9, 12, 4, HAT_D)                                   # hat tipped further back
            c.box(24, y0 + 4, 8, 6, TABLET, out=None, hi=lt(TABLET, .3), sh='#0c0a08')
            c.r(25, y0 + 5, 6, 4, GLOW)
            c.line(23, y0 + 6, 25, y0 + 6, VEST, 2)
        c.outline_alpha(); out.append(c)
    return out
