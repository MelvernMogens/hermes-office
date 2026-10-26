"""Content-floor cleaner: 'Inky' -- a WALKING VINTAGE TYPEWRITER creature. Chunky dark typewriter
body with brass trim, a sheet of paper sticking up as its head/crest (two ink-dot eyes near the
top), a platen roller with a side knob, and a carriage-return lever sticking out behind like a
tail. It scuttles on FOUR short spindly legs (two visible pairs, diagonal gait) -- no torso, no
arms, nothing humanoid. Canvas 40x36 cells, anchor bottom-centre (feet row 35, body centred x=20),
faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Inky', 'persona': 'A vintage typewriter that scuttled to life and now proof-reads the floor.',
        'fx': 'paper', 'fxColor': '#f4ecd8'}

W, H = 40, 36
BODY, BODY_D, BODY_L = '#3a2e22', '#241c14', '#5a4632'
BRASS, BRASS_D = '#e0a060', '#a86e3c'
KEY, KEY_L = '#241f1b', '#3a332c'
PAPER, PAPER_D = '#f4ecd8', '#cfc4a0'
INK = '#2a2018'
EYE = '#17130f'
LEVER, LEVER_D = '#9aa3ad', '#6b7580'
LEG, LEG_D = '#6b5842', '#3f3222'
CRATE, CRATE_D, CRATE_L = '#4a3522', '#2f2115', '#6e5138'
BOOK1, BOOK2 = '#a8452f', '#3f6b52'
CUP, CUP_D, STEAM = '#3a2a1a', '#241a10', '#d8d2c4'

HIPS = (13, 17, 23, 27)


def legs(c, y0, mode):
    """mode: ('A',) contact-pair at hips[0,3]; ('B',) contact-pair hips[1,2]; 'mid' pass frame."""
    hipy = y0 + 10
    for hx in HIPS:
        if mode == 'mid':
            knee = (hx + 1, hipy + 4); foot = (hx + 2, 34)
        elif (mode == 'A' and hx in (HIPS[0], HIPS[3])) or (mode == 'B' and hx in (HIPS[1], HIPS[2])):
            knee = (hx, hipy + 5); foot = (hx, 35)
        else:
            knee = (hx + 3, hipy + 3); foot = (hx + 5, 31)
        c.line(hx, hipy, knee[0], knee[1], LEG_D, 1)
        c.line(knee[0], knee[1], foot[0], foot[1], LEG, 1)
        c.p(foot[0], foot[1], LEG_D)


def keybed(c, y0, variant=0):
    for i, x in enumerate(range(12, 29, 2)):
        up = (i + variant) % 3 == 0
        col = BRASS if i % 5 == 0 else KEY
        c.r(x, 21 - (1 if up else 0), 2, 2, col)
        c.p(x, 20 - (1 if up else 0), lt(col, .3))


def roller(c, y0, dx=0):
    c.box(11 + dx, y0 - 4, 18, 5, BODY_L, out=None, hi=lt(BODY_L, .2), sh=BODY_D)
    c.r(12 + dx, y0 - 3, 16, 1, dk(BODY_L, .2))
    c.circ(30 + dx, y0 - 2, 2, BRASS)
    c.circ(30 + dx, y0 - 2, 1, lt(BRASS, .3))
    # carriage-return lever, tail sticking out to the back (left)
    c.line(11 + dx, y0 - 2, 6 + dx, y0 - 6, LEVER, 1)
    c.line(11 + dx, y0 - 1, 6 + dx, y0 - 5, LEVER_D, 1)
    c.circ(5 + dx, y0 - 6, 1, LEVER)


def crest(c, y0, dx=0, curl=False):
    if curl:
        c.box(15 + dx, y0 + 3, 10, 7, PAPER, out=None, hi=lt(PAPER, .15), sh=PAPER_D)
        c.r(15 + dx, y0 + 3, 3, 3, dk(PAPER, .1))     # curled corner
    else:
        c.box(15 + dx, y0, 10, 10, PAPER, out=None, hi=lt(PAPER, .15), sh=PAPER_D)
        for ry in (y0 + 3, y0 + 5, y0 + 7):
            c.r(16 + dx, ry, 7, 1, INK)
        c.p(17 + dx, y0 + 1, EYE); c.p(21 + dx, y0 + 1, EYE)   # two eye-dots near the top


def build(bob=0, carriage_dx=0, leg_mode='A', key_v=0, action=None, ext=0, wipe_x=24, ribbon=0):
    c = C(W, H)
    y0 = 16 - bob
    legs(c, y0, leg_mode)
    c.box(10, y0, 20, 10, BODY, out=None, hi=BODY_L, sh=BODY_D)
    c.r(10, y0 + 8, 20, 1, BRASS_D)                    # brass trim band low on the body
    c.r(10, y0, 20, 1, lt(BODY, .2))
    keybed(c, y0, key_v)
    roller(c, y0, carriage_dx)
    crest(c, y0 - 12, carriage_dx // 2 if carriage_dx else 0)
    if action == 'duster':
        hx, hy = 11 + carriage_dx, y0 - 6
        ex, ey = 8, y0 + 4 + ext
        c.line(hx, hy, ex, ey, LEVER, 2)
        fx, fy = wipe_x, 33
        c.line(ex, ey, fx, fy, LEVER, 2)
        c.box(fx - 3, fy - 4, 6, 5, PAPER, out=None, hi=lt(PAPER, .2), sh=PAPER_D)
        c.r(fx - 3, fy - 4, 6, 1, PAPER_D)
        for i in range(ribbon):
            c.p(fx + 4 + i, fy - 5 - i, PAPER_D)
    c.outline_alpha()
    return c


def walk():
    return [build(0, 0, 'A', 0),
            build(1, 1, 'mid', 1),
            build(0, 0, 'B', 2),
            build(1, -1, 'mid', 0)]


def clean():
    out = []
    for i, (wx, ext, rb) in enumerate(((24, 0, 1), (28, 1, 2), (32, 0, 3), (28, 1, 2))):
        out.append(build(i % 2, (i % 3) - 1, 'A' if i % 2 == 0 else 'B', i, action='duster',
                          ext=ext, wipe_x=wx, ribbon=rb))
    return out


BOOK3, BOOK3_D, BOOK3_L = '#7a5a2a', '#4f3a1a', '#a87d40'   # tall spine backrest book
SEAT_TOP = 22    # row of the top book-stack surface (character body rests here)


def seat():
    """Armchair built from stacked books: a wide low stack forms the seat cushion, a wide
    tall stack of books directly behind it forms a full backrest (chair-back silhouette,
    a few cells wider than the character so its edges peek out on both sides), plus a
    smaller side stack as an armrest. Spans floor (row35) up to backrest top (~row6)."""
    c = C(W, H)
    # wide backrest: 3 stacked hardcovers standing behind the seat, wider than the character
    # body (20 cells) so 2px of spine shows on each side -> reads as a chair-back panel
    bx, bw = 8, 24
    c.box(bx, 6, bw, 6, BOOK1, out=None, hi=lt(BOOK1, .2), sh=dk(BOOK1, .3))
    c.r(bx + 1, 8, bw - 2, 1, dk(BOOK1, .3))
    c.box(bx, 12, bw, 5, BOOK3, out=None, hi=BOOK3_L, sh=BOOK3_D)
    c.r(bx + 1, 14, bw - 2, 1, dk(BOOK3, .3))
    c.box(bx, 17, bw, 5, BOOK2, out=None, hi=lt(BOOK2, .2), sh=dk(BOOK2, .3))
    c.r(bx + bw - 2, 7, 1, 14, PAPER)                        # page-edge stripe down the right side
    for ry in range(9, 21, 3): c.p(bx + bw - 2, ry, PAPER_D)
    c.r(bx + 1, 7, 1, 14, PAPER)                              # page-edge stripe down the left side too
    # low wide stack of books forming the seat cushion (character sits on top, row SEAT_TOP)
    c.box(9, SEAT_TOP, 22, 13, CRATE, out=None, hi=CRATE_L, sh=CRATE_D)
    for i in range(3):
        c.r(10, SEAT_TOP + 3 + i * 3, 20, 1, dk(CRATE, .35))
    c.r(11, SEAT_TOP + 1, 6, 1, PAPER)
    # small armrest stack of books to the right, in front of the backrest
    c.box(31, SEAT_TOP - 8, 6, 10, BOOK2, out=None, hi=lt(BOOK2, .2), sh=dk(BOOK2, .3))
    c.box(31, SEAT_TOP - 12, 6, 5, BOOK1, out=None, hi=lt(BOOK1, .2), sh=dk(BOOK1, .3))
    # loose paper stack on top of the armrest for flourish
    c.r(32, SEAT_TOP - 15, 4, 3, PAPER); c.r(32, SEAT_TOP - 15, 4, 1, PAPER_D)
    c.r(6, 34, 28, 2, dk(CRATE_D, .3))
    c.outline_alpha()
    return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = SEAT_TOP - 10
        for hx in (14, 26):
            c.r(hx, y0 + 12, 2, 3, LEG_D)              # folded leg stubs
        c.box(10, y0, 20, 10, BODY, out=None, hi=BODY_L, sh=BODY_D)
        c.r(10, y0 + 8, 20, 1, BRASS_D)
        keybed(c, y0, 0)
        roller(c, y0, 0)
        crest(c, y0 - 12, curl=(k == 0))
        if k == 0:
            c.txt(29, y0 - 15, 'Z', lt(PAPER, .1), 1)
            c.txt(32, y0 - 18, 'Z', lt(PAPER, .1), 1)
        else:
            c.r(30, y0 + 1, 4, 4, CUP); c.r(30, y0, 4, 1, lt(CUP, .3))
            c.p(31, y0 - 1, STEAM); c.p(33, y0 - 2, STEAM)
        c.outline_alpha()
        out.append(c)
    return out
