"""Design floor cleaner: 'The Painter' - SHORT and ROUND/CHUBBY, defining silhouette is a
HUGE floppy beret (wider than the whole body) tipped to one side sitting low over the eyes,
splattered apron with paint dots, long paint roller resting diagonally on the shoulder.
Movement = WADDLE: whole body rocks/tilts left-right, tiny stubby-leg steps (no long stride).
Canvas 40x36 cells, anchor bottom-centre (feet on row 35, body centred on x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Rolo Blotch', 'persona': 'Studio muralist who waddles the halls touching up scuffs.',
        'fx': 'paint', 'fxColor': '#f5a8c8'}

W, H = 40, 36

SKIN, SKIN_D = '#e0b48c', '#b3855e'
BERET, BERET_D, BERET_L = '#9c4a70', '#651e3e', '#c86e94'   # brighter magenta-plum, pops on dark floor
SHIRT, SHIRT_D, SHIRT_L = '#5a3c78', '#3a2650', '#7a5ca0'    # brighter violet, distinct from floor #222027
APRON, APRON_D, APRON_L = '#e8e2d4', '#bcb4a0', '#f8f4ea'
SHOE, SHOE_D = '#2a1e38', '#160f20'
HANDLE, HANDLE_D = '#8a6a44', '#5a4228'
ROLL, ROLL_D = '#d8d0c0', '#a89c86'
PINK, VIOLET, YEL, CYAN = '#f5a8c8', '#c86ee0', '#f0d060', '#68c8d8'
DOTS = (PINK, VIOLET, YEL, CYAN)


def beret(c, cx, cy, tilt=0):
    """HUGE floppy beret - the single defining silhouette blob, much wider than the head/body,
    sitting low and tipped to one side. Drawn with a soft flop droop on the tilted side."""
    c.ell(cx + tilt, cy, 15, 6, BERET)                       # wide flat main disc
    c.ell(cx + tilt - 1, cy - 2, 12, 4, lt(BERET, .18))       # top highlight sheen
    c.ell(cx + tilt, cy + 3, 14, 4, BERET_D)                  # underside shade / brim
    c.ell(cx + tilt + 9, cy + 3, 5, 4, BERET_D)               # floppy droop on the tilted side
    c.ell(cx + tilt + 9, cy + 1, 4, 3, BERET)
    c.circ(cx + tilt - 2, cy - 3, 1, BERET_D)                 # little stem nub on top


def head(c, cx, cy, tilt=0):
    c.circ(cx, cy, 6, SKIN)
    c.circ(cx + 2, cy - 1, 3, lt(SKIN, .15))
    c.circ(cx - 3, cy + 3, 3, SKIN_D)
    c.p(cx - 3, cy + 1, mix(SKIN, PINK, .4)); c.p(cx + 3, cy + 1, mix(SKIN, PINK, .4))
    c.p(cx - 2, cy - 1, '#241a2e'); c.p(cx + 2, cy - 1, '#241a2e')
    c.r(cx - 1, cy + 2, 3, 1, SKIN_D)
    beret(c, cx, cy - 6, tilt)


def body(c, rock=0, step=0):
    """Short round chubby body, stubby short legs, apron with paint dots.
    rock: -1/0/1 tilts whole upper body left/right (waddle). step: which stubby leg is forward."""
    cx = 20
    top = 15
    # wide round torso built from stacked ellipses -> soft belly silhouette, not a boxy wedge
    c.ell(cx + rock, top + 9, 10, 8, SHIRT)
    c.ell(cx + rock, top + 12, 11, 6, SHIRT)          # belly bulge widest near the bottom
    c.ell(cx + rock - 3, top + 5, 6, 5, SHIRT_L)
    c.ell(cx + rock + 4, top + 14, 6, 5, SHIRT_D)
    # splattered apron bib, rounded
    c.ell(cx + rock, top + 11, 7, 8, APRON)
    c.r(cx + rock - 6, top + 5, 12, 2, APRON_L)
    c.ell(cx + rock + 2, top + 17, 4, 3, APRON_D)
    dots = ((-4, -4), (3, -5), (-2, 0), (5, 1), (-5, 5), (2, 6), (5, -2))
    for i, (dx, dy) in enumerate(dots):
        c.circ(cx + rock + dx, top + 11 + dy, 1, DOTS[i % 4])
    # stubby short legs, tiny steps, bright shoe colour for floor contrast
    lx = -4 if step == 0 else -5 if step == 1 else -3
    rx = 4 if step == 0 else 3 if step == 1 else 5
    c.r(cx + rock + lx, 28, 4, 5, SHIRT_D)
    c.r(cx + rock + rx, 28, 4, 5, SHIRT_D)
    c.r(cx + rock + lx - 1, 33, 6, 2, SHOE)
    c.r(cx + rock + rx - 1, 33, 6, 2, SHOE)
    c.r(cx + rock + lx - 1, 32, 6, 1, lt(SHOE, .25))
    c.r(cx + rock + rx - 1, 32, 6, 1, lt(SHOE, .25))
    return cx + rock, top


def roller_shoulder(c, cx, top):
    """Long paint roller resting diagonally on shoulder, sticking up behind (walk pose)."""
    bx, by = cx + 6, top + 5
    tx, ty = cx - 11, top - 17
    c.line(bx, by, tx, ty, HANDLE, 2)
    c.ell(tx, ty, 3, 5, ROLL)
    c.r(tx - 3, ty - 4, 6, 2, ROLL_D)
    c.p(tx - 2, ty - 5, PINK)


def roller_front(c, cx, top, phase=0):
    """Clean pose: roller swung down in front, rolling up/down leaving a pink streak."""
    bx, by = cx + 8, top + 3
    ry = top + 18 + phase
    c.line(bx, by, cx + 9, ry, HANDLE, 2)
    c.ell(cx + 9, ry, 4, 3, ROLL)
    c.r(cx + 6, ry - 2, 6, 1, ROLL_D)
    streak_h = 6 + abs(phase)
    c.r(cx + 7, top + 18, 3, streak_h, PINK)
    c.r(cx + 7, top + 18, 1, streak_h, mix(PINK, '#ffffff', .3))


def walk():
    out = []
    for rock, step in ((-1, 0), (0, 1), (1, 2), (0, 1)):
        c = C(W, H)
        cx, top = body(c, 0, step)            # body stays on x=20 (anchor rule); waddle = head/beret tilt + roller sway
        head(c, cx, top - 6, tilt=rock)
        roller_shoulder(c, cx + rock, top)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    out = []
    for rock, phase in ((0, -3), (0, 0), (0, 3), (0, 0)):
        c = C(W, H)
        cx, top = body(c, rock, 0)
        head(c, cx, top - 6, tilt=0)
        roller_front(c, cx, top, phase)
        c.outline_alpha(); out.append(c)
    return out


def seat():
    c = C(W, H)
    # folding artist stool (left side of the footprint)
    c.box(6, 22, 12, 4, HANDLE, out=None, hi=lt(HANDLE, .2), sh=HANDLE_D)
    c.line(7, 26, 4, 35, HANDLE_D, 2); c.line(17, 26, 20, 35, HANDLE_D, 2)
    c.line(12, 26, 9, 35, HANDLE, 2); c.line(12, 26, 15, 35, HANDLE, 2)
    c.r(3, 34, 4, 1, HANDLE_D); c.r(19, 34, 4, 1, HANDLE_D)
    c.r(8, 33, 3, 1, HANDLE_D); c.r(14, 33, 3, 1, HANDLE_D)
    # small easel further right, clear of the stool, footed on the floor row
    c.line(28, 34, 30, 10, HANDLE, 1)
    c.line(37, 34, 33, 10, HANDLE, 1)
    c.r(27, 21, 11, 1, HANDLE_D)
    c.box(29, 9, 8, 10, APRON, out=None, hi=APRON_L, sh=APRON_D)
    c.circ(31, 12, 1, PINK); c.circ(34, 14, 1, CYAN); c.circ(32, 16, 1, YEL)
    # small paint bucket in the gap between stool and easel
    c.box(21, 29, 6, 6, ROLL, out=None, hi=lt(ROLL, .2), sh=ROLL_D)
    c.r(22, 29, 4, 2, PINK)
    c.r(21, 28, 6, 1, HANDLE_D)
    c.line(22, 28, 25, 25, HANDLE, 1)   # small bucket handle arc
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = 4
        cx = 12   # seated over the stool footprint (left side of the seat canvas)
        c.ell(cx, y0 + 20, 9, 6, SHIRT)
        c.ell(cx, y0 + 16, 9, 8, SHIRT)
        c.ell(cx - 3, y0 + 12, 5, 4, SHIRT_L)
        c.ell(cx, y0 + 18, 7, 6, APRON)
        dots = ((-3, -2), (3, -3), (-2, 3), (3, 1))
        for i, (dx, dy) in enumerate(dots):
            c.circ(cx + dx, y0 + 18 + dy, 1, DOTS[i % 4])
        c.r(cx - 6, y0 + 24, 4, 6, SHIRT_D); c.r(cx + 3, y0 + 24, 4, 6, SHIRT_D)
        c.r(cx - 7, y0 + 29, 6, 2, SHOE); c.r(cx + 2, y0 + 29, 6, 2, SHOE)
        head(c, cx, y0 + 6, tilt=0)
        if k == 0:
            # frame A: sipping from paint-splattered mug
            c.r(cx + 8, y0 + 12, 4, 5, APRON_L)
            c.circ(cx + 9, y0 + 13, 1, PINK); c.circ(cx + 10, y0 + 15, 1, VIOLET)
            c.r(cx + 12, y0 + 12, 2, 3, HANDLE)
            c.line(cx + 5, y0 + 13, cx + 9, y0 + 13, SHIRT, 2)
        else:
            # frame B: sketching on a small pad
            c.r(cx + 6, y0 + 15, 7, 5, APRON_L)
            c.r(cx + 7, y0 + 16, 5, 1, APRON_D)
            c.r(cx + 7, y0 + 18, 3, 1, APRON_D)
            c.line(cx + 5, y0 + 14, cx + 11, y0 + 16, SHIRT, 2)
            c.p(cx + 11, y0 + 16, HANDLE)
        c.outline_alpha(); out.append(c)
    return out
