"""Fallback cleaner (floors without a theme): classic janitor, blue coverall + cap, yellow bucket + mop.
Also the TEMPLATE for the per-theme cleaners: copy the structure, not the look.
Canvas 40x36 cells, anchor bottom-centre (feet on row 35, body centred on x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Joe the Janitor', 'persona': 'Old-school janitor who has mopped every floor of this tower twice.',
        'fx': 'bubbles', 'fxColor': '#bfe6ff'}

W, H = 40, 36
SKIN, SKIN_D = '#e0a878', '#b87c52'
BLUE, BLUE_D, BLUE_L = '#3f6fd1', '#2a4c99', '#6a93e8'
CAP = '#2a4c99'
BOOT = '#2b2522'
YEL, YEL_D = '#f2c230', '#b88a10'
WOOD, WOOD_D = '#a57845', '#6e4b26'
MOP, MOP_D = '#e8e4d6', '#b0aa98'
WATER = '#7fc4ff'


def body(c, bob=0, legs=0, arm=None):
    """legs: 0 = stand, 1 = left fwd, 2 = right fwd. bob shifts upper body up by 1 cell."""
    y0 = 4 - bob
    # legs
    if legs == 0:
        c.r(16, 27, 3, 7, BLUE_D); c.r(21, 27, 3, 7, BLUE_D)
        c.r(15, 33, 5, 3, BOOT); c.r(21, 33, 5, 3, BOOT)
    elif legs == 1:
        c.r(14, 27, 3, 7, BLUE_D); c.r(22, 27, 3, 6, BLUE_D)
        c.r(12, 33, 5, 3, BOOT); c.r(22, 32, 5, 3, BOOT)
    else:
        c.r(16, 27, 3, 6, BLUE_D); c.r(22, 27, 3, 7, BLUE_D)
        c.r(15, 32, 5, 3, BOOT); c.r(23, 33, 5, 3, BOOT)
    # torso (coverall)
    c.box(14, y0 + 10, 12, 14 + bob, BLUE, out=None, hi=BLUE_L, sh=BLUE_D)
    c.r(16, y0 + 13, 8, 1, BLUE_D)            # bib seam
    c.r(21, y0 + 15, 2, 2, '#e8e8e8')          # name tag
    c.r(14, y0 + 21, 12, 1, dk(BLUE, .35))     # belt
    # head
    c.box(15, y0 + 3, 10, 8, SKIN, out=None, hi=lt(SKIN, .2), sh=SKIN_D)
    c.r(22, y0 + 6, 1, 1, '#1a1a1a')           # eye (facing right)
    c.r(21, y0 + 9, 3, 1, '#8a5a3a')           # moustache
    # cap with bill to the right
    c.r(14, y0 + 1, 11, 3, CAP); c.r(15, y0, 9, 1, CAP); c.r(24, y0 + 3, 4, 1, dk(CAP, .3))
    c.r(16, y0 + 1, 3, 1, lt(CAP, .25))
    # back arm
    c.r(14, y0 + 12, 2, 8, BLUE_D)


def mop(c, hx, hy, fx, fy):
    """handle from hand (hx,hy) down to mop head at (fx,fy)"""
    c.line(hx, hy, fx, fy - 2, WOOD, 1)
    c.line(hx + 1, hy, fx + 1, fy - 2, WOOD_D, 1)
    c.r(fx - 3, fy - 2, 8, 2, MOP_D)
    for i in range(0, 8, 2):
        c.r(fx - 3 + i, fy, 1, 2, MOP); c.r(fx - 2 + i, fy, 1, 1, MOP_D)


def bucket(c, x):
    c.box(x, 27, 9, 7, YEL, out=None, hi=lt(YEL, .3), sh=YEL_D)
    c.r(x + 1, 27, 7, 1, WATER)
    c.r(x + 1, 34, 2, 2, '#222'); c.r(x + 6, 34, 2, 2, '#222')


def front_arm(c, bob, hx, hy):
    c.line(22, 16 - bob, hx, hy, BLUE, 2); c.r(hx, hy, 2, 2, SKIN)


def walk():
    out = []
    for legs, bob in ((1, 0), (0, 1), (2, 0), (0, 1)):
        c = C(W, H)
        mop(c, 28, 8 - bob, 31, 33 - bob)  # mop carried upright, head just off the floor
        body(c, bob, legs)
        front_arm(c, bob, 27, 17 - bob)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    out = []
    for fx in (29, 33, 36, 32):
        c = C(W, H)
        bucket(c, 3)
        body(c, 0, 0)
        mop(c, 26, 14, fx, 34)
        front_arm(c, 0, 25, 17)
        c.outline_alpha(); out.append(c)
    return out


FRAME, FRAME_D, FRAME_L = '#6b7a8a', '#4a5663', '#8a9aaa'
PAN_Y = 21     # row of the folding-chair seat-pan surface (hips rest here)


def seat():
    """Metal folding chair (tall backrest, X-braced legs) + a yellow mop bucket parked
    beside it. Chair spans floor (row35) up to the backrest top (~row6): ~29 cells tall."""
    c = C(W, H)
    post_l, post_r = 13, 28
    # back posts: continuous vertical members from the floor up through the backrest
    c.r(post_l, 6, 2, 29, FRAME_D); c.r(post_l, 6, 1, 29, FRAME_L)
    c.r(post_r, 6, 2, 29, FRAME_D); c.r(post_r + 1, 6, 1, 29, FRAME_D)
    c.p(post_l, 35, '#2a2f36'); c.p(post_r + 1, 35, '#2a2f36')       # foot caps
    # backrest slats between the posts
    for ry in (9, 13, 17):
        c.r(post_l + 2, ry, post_r - post_l - 2, 2, FRAME)
        c.r(post_l + 2, ry, post_r - post_l - 2, 1, FRAME_L)
    # front legs bracing forward to the floor (X-brace look)
    c.line(post_l + 1, PAN_Y + 2, 17, 35, FRAME_D, 1)
    c.line(post_r, PAN_Y + 2, 24, 35, FRAME_D, 1)
    # seat pan (horizontal plank, character's hips rest on top edge)
    c.box(11, PAN_Y, post_r - 11 + 3, 3, FRAME, out=None, hi=FRAME_L, sh=FRAME_D)
    c.r(11, PAN_Y, post_r - 11 + 3, 1, FRAME_L)
    # yellow mop bucket parked beside the chair
    bx = 4
    c.box(bx, 27, 9, 7, YEL, out=None, hi=lt(YEL, .3), sh=YEL_D)
    c.r(bx + 1, 27, 7, 1, WATER)
    c.r(bx + 1, 34, 2, 2, '#222'); c.r(bx + 6, 34, 2, 2, '#222')
    c.line(bx + 4, 27, bx + 6, 22, WOOD, 1); c.r(bx + 3, 21, 6, 2, MOP_D)  # mop leaning in bucket
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)          # character ONLY; engine draws seat() underneath in the same box
        head_y, torso_y = 5, 12
        hip_y = PAN_Y - 1                                   # 20: hips rest just above the pan surface
        # torso + head drawn FIRST (legs/feet paint on top of the torso's bottom edge)
        c.box(14, torso_y, 12, hip_y - torso_y + 4, BLUE, out=None, hi=BLUE_L, sh=BLUE_D)
        c.box(15, head_y, 10, 8, SKIN, out=None, hi=lt(SKIN, .2), sh=SKIN_D)
        c.r(14, head_y - 2, 11, 3, CAP); c.r(24, head_y, 4, 1, dk(CAP, .3))
        c.r(16, head_y - 2, 3, 1, lt(CAP, .25))
        c.r(22, head_y + 3, 1, 1, '#1a1a1a' if k == 0 else SKIN_D)   # blink
        c.r(21, head_y + 6, 3, 1, '#8a5a3a')                          # moustache
        c.r(21, head_y + 10, 2, 2, '#e8e8e8')                          # name tag
        # hips/thighs band resting flat on the seat pan (drawn over the torso bottom)
        c.r(14, hip_y, 13, 4, BLUE_D)
        # front leg: shin + boot down to the floor
        c.r(23, hip_y + 3, 3, 10, BLUE_D); c.r(23, hip_y + 12, 5, 3, BOOT)
        # back leg: shin + boot down to the floor, offset to the left
        c.r(15, hip_y + 3, 3, 10, BLUE_D); c.r(14, hip_y + 12, 5, 3, BOOT)
        # back arm resting at the side
        c.r(14, torso_y + 2, 2, 8, BLUE_D)
        # coffee cup in hand + steam
        c.r(24, torso_y + 7, 3, 2, BLUE); c.r(26, torso_y + 5, 3, 4, '#f0f0f0'); c.r(26, torso_y + 5, 3, 1, '#6b4a2a')
        s = 4 + k
        c.r(27, torso_y + 5 - s, 1, 2, '#c8d0d8'); c.r(28 - k, torso_y + 2 - s, 1, 2, '#c8d0d8')
        c.outline_alpha(); out.append(c)
    return out
