"""Analyst-floor cleaner: 'Tally' -- an ABACUS ROBOT riding a single big wheel (unicycle).
Body = a rectangular navy-steel abacus frame with 3 rods of sliding coloured beads, topped by a
small dome head (single blue eye-lens + thin antenna) and two thin stub arms. NO legs: the whole
rig balances on one large spoked wheel directly under the frame.
Canvas 40x36 cells, anchor bottom-centre (wheel touches row 35, body centred on x=20), faces right."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Tally', 'persona': 'An abacus-bot on a unicycle wheel that reconciles the aisles bead by bead.',
        'fx': 'pixels', 'fxColor': '#4da3ff'}

W, H = 40, 36
NAVY, NAVY_D, NAVY_L = '#1c3150', '#12213a', '#2f4a72'
FRAME, FRAME_D, FRAME_L = '#2c4468', '#1b2c47', '#4a6690'
WHEEL, WHEEL_D, HUB = '#232a35', '#141820', '#4da3ff'
ROD = '#c9a24a'
WHITE_B, AMBER_B, BLUE_B = '#e8edf5', '#f0a840', '#4da3ff'
ROD_BASE = [WHITE_B, AMBER_B, WHITE_B]
HEAD, HEAD_D, HEAD_L = '#26374f', '#16223690', '#3d5678'
HEAD_D = '#16223a'
ANT = '#7c8ba3'
AMB = '#f59e0b'
RUB, RUB_D = '#9fd0ff', '#5f9fe0'
DOCK, DOCK_D, DOCK_L = '#233246', '#141d2a', '#3a4f6c'
SCR_BEZ, SCR = '#12181a', '#16324a'


def wheel(c, cx, cy, r, spin=0):
    c.circ(cx, cy, r, WHEEL)
    c.ring(cx, cy, r, WHEEL_D, th=2)
    c.circ(cx, cy, 2, HUB)
    for i in range(4):
        a = math.pi * ((i + spin * .5) / 4)
        x2, y2 = cx + (r - 1) * math.cos(a), cy + (r - 1) * math.sin(a)
        c.line(cx, cy, x2, y2, lt(WHEEL_D, .3), 1)
    c.r(cx - r, cy + r - 1, r * 2, 1, dk(WHEEL_D, .3))


def rods(c, y0, frame_idx):
    for i, ry in enumerate((y0 + 3, y0 + 7, y0 + 11)):
        c.r(12, ry, 16, 1, ROD)
        base = ROD_BASE[i]
        active = (frame_idx + i * 2) % 5
        for j in range(5):
            bx = 13 + j * 3 + (1 if (j == active and frame_idx % 2 == 1) else 0)
            col = BLUE_B if j == active else base
            c.r(bx, ry - 1, 2, 2, col)
            c.p(bx, ry - 1, lt(col, .3))


def head(c, y0, eye_on=True, blink=False):
    c.box(15, y0, 10, 6, HEAD, out=None, hi=HEAD_L, sh=HEAD_D)
    c.r(16, y0, 8, 1, HEAD_L)
    eye_col = HUB if eye_on else dk(HUB, .55)
    c.circ(20, y0 + 3, 2, eye_col)
    c.circ(20, y0 + 3, 1, lt(eye_col, .35))
    c.line(20, y0 - 2, 20, y0, ANT, 1)
    c.p(20, y0 - 2, AMB if blink else dk(AMB, .45))


def arm_idle(c, y0):
    c.line(11, y0 + 6, 8, y0 + 9, FRAME_D, 1); c.r(7, y0 + 9, 2, 2, FRAME_D)
    c.line(29, y0 + 6, 32, y0 + 9, FRAME_D, 1); c.r(32, y0 + 9, 2, 2, FRAME_D)


def arm_wipe(c, y0, ext, wipe_x):
    hx, hy = 29, y0 + 6
    ex, ey = 31, 26 + ext
    c.line(hx, hy, ex, ey, FRAME_D, 2)
    fx, fy = wipe_x, 33
    c.line(ex, ey, fx, fy, FRAME_D, 2)
    c.r(fx - 3, fy, 7, 2, RUB)
    c.r(fx - 3, fy - 1, 7, 1, lt(RUB, .25))
    c.line(11, y0 + 6, 8, y0 + 9, FRAME_D, 1); c.r(7, y0 + 9, 2, 2, FRAME_D)


def build(bob=0, spin=0, frame_idx=0, eye_on=True, blink=False, clean_mode=False, wipe_x=24, ext=0):
    c = C(W, H)
    wheel(c, 20, 29, 6, spin)
    y0 = 8 - bob
    c.r(18, y0 + 13, 4, 4, FRAME_D)                        # axle strut into the wheel
    c.box(11, y0, 18, 14, FRAME, out=None, hi=FRAME_L, sh=FRAME_D)
    c.r(19, y0 + 1, 2, 12, dk(FRAME, .15))                 # centre seam
    rods(c, y0, frame_idx)
    if clean_mode:
        arm_wipe(c, y0, ext, wipe_x)
    else:
        arm_idle(c, y0)
    head(c, y0 - 6, eye_on, blink)
    c.outline_alpha()
    return c


def walk():
    return [build(0, 0, 0, True, False),
            build(1, 1, 1, True, False),
            build(0, 2, 2, False, True),
            build(1, 3, 3, True, False)]


def clean():
    out = []
    for i, (wx, ext) in enumerate(((24, 0), (29, 1), (34, 0), (29, 1))):
        out.append(build(0, i, i, True, False, clean_mode=True, wipe_x=wx, ext=ext))
    return out


def seat():
    c = C(W, H)
    c.box(8, 28, 24, 7, DOCK, out=None, hi=DOCK_L, sh=DOCK_D)
    c.r(9, 29, 22, 1, lt(DOCK, .2))
    c.ell(20, 29, 7, 3, DOCK_D)                            # wheel slot groove
    c.ring(20, 29, 7, dk(DOCK_D, .3), th=1)
    c.r(27, 17, 2, 11, DOCK_D)                             # terminal post
    c.box(23, 10, 10, 8, SCR_BEZ, out=None, hi=lt(SCR_BEZ, .2), sh='#060809')
    c.r(24, 11, 8, 6, SCR)
    for i, bh in enumerate((2, 4, 3, 5)):
        c.r(25 + i * 2, 16 - bh, 1, bh, HUB)
    c.r(6, 34, 28, 2, dk(DOCK_D, .3))
    c.outline_alpha()
    return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = 10
        c.r(18, y0 + 13, 4, 3, FRAME_D)
        c.box(11, y0, 18, 13, FRAME, out=None, hi=FRAME_L, sh=FRAME_D)
        c.r(19, y0 + 1, 2, 11, dk(FRAME, .15))
        rods(c, y0, 0 if k == 0 else 3)
        arm_idle(c, y0)
        head(c, y0 - 6, eye_on=(k == 1), blink=(k == 0))
        if k == 0:
            c.txt(29, y0 - 12, 'Z', lt(HUB, .35), 1)
            c.txt(32, y0 - 15, 'Z', lt(HUB, .35), 1)
        c.outline_alpha()
        out.append(c)
    return out
