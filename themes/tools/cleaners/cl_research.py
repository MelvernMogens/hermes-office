"""Research floor cleaner: 'Old Librarian' - VERY TALL & THIN, strongly hunched forward,
long dark robe sweeping the floor (hides legs entirely - no leg stride, only hem wiggle),
small round gold spectacles, walking-cane in back hand, long feather duster on a pole in
front hand. Silhouette: a tall curved question-mark shape (head pushed far forward/down of
the hip line) with a wide sweeping hem triangle at the bottom - unlike the standard 2-leg
humanoid rig used elsewhere. Canvas 40x36 cells, anchor bottom-centre (hem on row 35,
body centred on x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Old Marginalia', 'persona': 'Ancient archivist who has shushed every desk on this floor twice.',
        'fx': 'dust', 'fxColor': '#c9a55a'}

W, H = 40, 36

ROBE, ROBE_D, ROBE_L = '#6b8450', '#435532', '#93ad72'   # mossy olive robe, brighter to pop off dark floor
SKIN, SKIN_D = '#d8b48c', '#a9805a'
GOLD, GOLD_D = '#c9a55a', '#8f7238'
WOOD, WOOD_D, WOOD_L = '#5a3c22', '#3a2c1c', '#7a5a36'
FEATH, FEATH_D = '#e8dcc0', '#b8a878'
WHITE = '#f0e8d8'
HAIR = '#9a9a90'


def head(c, hx, hy):
    """Small old head, pushed forward+down of the hunch. hx,hy = top-left of the 9x8 skin box."""
    c.box(hx, hy, 9, 8, SKIN, out=None, hi=lt(SKIN, .2), sh=SKIN_D)
    c.r(hx - 1, hy - 1, 10, 2, HAIR)          # wispy grey hair band
    c.r(hx - 1, hy + 1, 2, 4, HAIR)           # hair falling at the back (left side)
    c.ring(hx + 2, hy + 4, 2, GOLD, 1)        # round spectacles, glinting gold
    c.ring(hx + 6, hy + 4, 2, GOLD, 1)
    c.r(hx + 4, hy + 4, 2, 1, GOLD_D)
    c.p(hx + 1, hy + 3, WHITE)
    c.p(hx + 5, hy + 3, WHITE)
    c.r(hx + 7, hy + 5, 2, 1, SKIN_D)         # long nose tip
    c.p(hx + 3, hy + 7, SKIN_D)               # downturned mouth


def body(c, wiggle=0, cane=True):
    """Very tall thin, strongly hunched: head sits FAR forward+right and LOW, well below where
    an upright head would be, off the hip's x=19 vertical axis. Robe fans out into a wide
    dragging hem that fully hides the legs; no leg stride ever."""
    rows = [
        (9, 32, 4),    # near head/neck, far right and already low (the forward hunch curls down)
        (12, 29, 6),
        (15, 26, 7),
        (18, 24, 8),
        (21, 22, 9),
        (24, 20, 11),
        (27, 19, 13),
        (30, 19, 14),
        (32, 19 + wiggle, 15),
    ]
    for y, cx, hw in rows:
        c.r(cx - hw, y, hw * 2, 4, ROBE)
    for y, cx, hw in rows:
        c.r(cx - hw, y, hw * 2, 1, ROBE_L)
        c.r(cx - hw, y + 3, hw * 2, 1, ROBE_D)
    # ragged hem sweeping the floor, no legs ever visible, light rim strip for contrast
    hemx = 19 + wiggle
    c.r(4, 34, 32, 1, ROBE_L)
    for i, dx in enumerate((-15, -11, -7, -3, 1, 5, 9, 13, 16)):
        depth = 1 + (i + wiggle) % 2
        c.r(hemx + dx, 35 - depth, 3, depth, ROBE_D)
    c.r(3, 35, 34, 1, ROBE_D)
    # vertical drape folds following the forward lean for readability
    for i, fx in enumerate((6, 12, 18, 25, 31)):
        c.line(fx + wiggle, 18 + i, fx + wiggle * 2, 34, ROBE_D, 1)
    # back hand + cane: fixed vertical pole trailing behind the hunch (opposite the duster),
    # only the hem around its foot wiggles so it never looks like it's flapping loose
    if cane:
        cx6 = 6 + wiggle
        c.line(cx6, 13, cx6 - wiggle, 33, WOOD, 1)
        c.circ(cx6, 12, 2, WOOD_L)
        c.r(cx6 - 1, 21, 3, 1, WOOD_D)
    # big hunched hump: a high shoulder/back bulge that the head droops down in FRONT of,
    # selling the curved-spine silhouette (bulge sits up-left/behind, head is forward/below it)
    c.ell(21, 6, 9, 6, ROBE)
    c.ell(18, 3, 6, 4, ROBE_L)
    c.ell(24, 10, 6, 4, ROBE_D)
    c.ell(25, 8, 3, 3, ROBE_D)   # short neck shadow smoothing the head-to-hump seam
    head(c, 29, 8)
    # front arm slung forward-down to the duster pole, elbow bent
    c.line(25, 19, 31, 23, ROBE, 2)
    c.r(30, 22, 3, 3, SKIN)
    return 32, 23  # hand position for the duster base


def duster(c, base_x, base_y, tip_y, flick=0):
    """Long feather-duster on a pole held forward; tuft attached right at the pole tip
    (elongated, not a floating round blob) so it reads connected across all flick heights."""
    tx, ty = base_x + 5, tip_y
    c.line(base_x, base_y, tx, ty, WOOD, 1)
    c.circ(tx, ty, 1, GOLD)                       # ferrule ring
    # feather tuft: a small vertical column of alternating tone blocks right above the tip
    for i in range(5):
        col = FEATH if i % 2 == 0 else FEATH_D
        w = 3 - (i // 2)
        c.r(tx - w // 2, ty - 2 - i, max(w, 1) + 1, 1, col)
    c.p(tx - 2, ty - 6, FEATH_D); c.p(tx + 2, ty - 6, FEATH)


def walk():
    out = []
    # shuffle: hem wiggles, tiny 1-cell body sway — no leg stride at all, duster held steady
    for wiggle in (0, 1, 0, -1):
        c = C(W, H)
        hx, hy = body(c, wiggle=wiggle)
        duster(c, hx, hy, hy + 2, flick=0)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    out = []
    # duster flicks up/down high in front, big motion (tip travels y=2..24), 4 frames
    for wiggle, tip in ((0, 24), (0, 4), (0, 24), (0, 2)):
        c = C(W, H)
        hx, hy = body(c, wiggle=wiggle, cane=False)
        duster(c, hx, hy, tip, flick=0)
        c.outline_alpha(); out.append(c)
    return out


def seat():
    c = C(W, H)
    c.box(9, 6, 16, 4, WOOD, out=None, hi=WOOD_L, sh=WOOD_D)      # chair top/back crest
    c.r(10, 10, 3, 22, WOOD_D); c.r(22, 10, 3, 22, WOOD_D)         # back posts
    c.box(11, 12, 13, 17, mix(WOOD, '#000000', .1), out=None, hi=WOOD_L, sh=WOOD_D)  # backrest panel
    c.box(8, 26, 20, 5, WOOD, out=None, hi=WOOD_L, sh=WOOD_D)      # seat cushion base
    c.r(7, 30, 4, 5, WOOD_D); c.r(23, 30, 4, 5, WOOD_D)            # front legs
    c.r(7, 8, 3, 5, WOOD_D); c.r(27, 8, 3, 5, WOOD_D)              # armrests
    c.box(6, 12, 4, 12, WOOD, out=None, hi=WOOD_L, sh=WOOD_D)
    c.box(27, 12, 4, 12, WOOD, out=None, hi=WOOD_L, sh=WOOD_D)
    # small side table with a teacup
    c.box(30, 27, 8, 2, WOOD, out=None, hi=WOOD_L, sh=WOOD_D)
    c.r(31, 29, 1, 5, WOOD_D); c.r(36, 29, 1, 5, WOOD_D)
    c.r(33, 24, 3, 3, WHITE)
    c.r(33, 26, 3, 1, GOLD_D)
    c.p(37, 22, GOLD)
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = 3 + (1 if k == 1 else 0)   # frame B: whole body nods down 1 cell
        # hunched seated body, hips on cushion, robe draped, no legs visible (robe covers)
        c.box(13, y0 + 19, 14, 7, ROBE, out=None, hi=ROBE_L, sh=ROBE_D)   # lap/robe over seat
        c.ell(22, y0 + 12, 9, 8, ROBE)                                    # hunched torso, forward-leaning
        c.ell(20, y0 + 9, 5, 4, ROBE_L)
        for fx in (16, 20, 25, 29):
            c.line(fx, y0 + 12, fx, y0 + 24, ROBE_D, 1)
        head(c, 25, y0 - 1)
        if k == 0:
            # frame A: reading a book held up in both hands
            c.box(24, y0 + 12, 9, 6, FEATH, out=None, hi=lt(FEATH, .2), sh=FEATH_D)
            c.r(28, y0 + 12, 1, 6, WOOD_D)
            c.line(22, y0 + 10, 25, y0 + 14, ROBE, 2)
            c.line(24, y0 + 10, 30, y0 + 13, ROBE, 2)
        else:
            # frame B: teacup with steam pixel, head nodded
            c.r(27, y0 + 14, 3, 3, WHITE)
            c.r(27, y0 + 16, 3, 1, GOLD_D)
            c.p(28, y0 + 12, mix('#ffffff', GOLD, .3))
            c.p(29, y0 + 10, mix('#ffffff', GOLD, .3))
            c.line(24, y0 + 11, 28, y0 + 15, ROBE, 2)
        c.outline_alpha(); out.append(c)
    return out
