"""Growth desk floor cleaner: 'Sprout' - a LIVING POTTED CACTUS (non-humanoid). Terracotta pot
is the body, a saguaro-style cactus grows out of it with two arms bent upward, a flower on top,
a cute big-eyed face, tiny feet peeking under the pot, and one arm always carrying a small
watering can. Moves by HOPPING (the whole pot bounces).
Canvas 40x36 cells, anchor bottom-centre (row 35), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Sprout', 'persona': 'Potted cactus that hops the desk rows and waters every lead itself.',
        'fx': 'leaves', 'fxColor': '#a3e635'}

W, H = 40, 36
FLOOR = '#1e221b'
ACCENT = '#a3e635'
OLIVE = '#34401c'

POT, POT_D, POT_L = '#c9772a', '#8a4514', '#e0954a'
FOOT, FOOT_D = '#4a3520', '#2f2113'
CACT, CACT_D, CACT_L = '#3c8a3c', '#215c21', '#6bc06b'
SPINE = '#e8dcb0'
EYE_W = '#f2fbe9'
EYE_P = '#14180f'
BLUSH = '#e88a6b'
FLOWER, FLOWER_D, FLOWER_C = '#ff6b9d', '#c9447a', '#ffd23f'
CAN, CAN_D, CAN_L = '#d8b23a', '#8f6003', '#f0d46b'
WATER = '#7fc4ff'
WOOD, WOOD_D, WOOD_L = '#6b5a4a', '#493d32', '#8a7460'
SHADOW = '#12150d'
GLOW = mix(ACCENT, FLOOR, .55)
GLOW2 = mix(ACCENT, FLOOR, .75)

CX = 20
TRUNK_W = 9
TRUNK_H = 11            # standard trunk height (unsquashed, floor-standing)


def shadow(c, rx):
    c.ell(CX, 35, rx, 1, SHADOW)
    c.ell(CX, 34, max(1, rx - 2), 1, mix(SHADOW, FLOOR, .3))


def sprout(c, lift=0, squash=0, can_tilt=0, drops=0, flower_open=0, face='smile', zzz=False,
           drink=False, leaf_sway=0, seat_top=None):
    """Draw the whole cactus-in-a-pot. lift = cells raised off the floor (0-2, draws air
    shadow). squash = 0/1 squat-and-wide hop extreme. seat_top overrides pot bottom (for sit(),
    resting on a low saucer). All limb/flower positions are anchored to trunk_bottom / trunk_top
    so nothing drifts off-canvas as squash/lift change."""
    bottom = (seat_top if seat_top is not None else 35) - lift
    pot_h = 10 - squash
    pot_top = bottom - pot_h
    bw = 17 + squash * 2          # bottom width
    tw = 12 + squash              # top (opening) width

    if lift > 0 and seat_top is None:
        shadow(c, rx=max(2, 7 - lift))

    # tiny feet peeking under the pot
    c.r(CX - bw // 2 + 2, bottom - 1, 3, 2, FOOT); c.r(CX - bw // 2 + 2, bottom, 3, 1, FOOT_D)
    c.r(CX + bw // 2 - 5, bottom - 1, 3, 2, FOOT); c.r(CX + bw // 2 - 5, bottom, 3, 1, FOOT_D)

    # pot: tapered rows terracotta with bevel edges
    for i in range(pot_h):
        t = i / max(1, pot_h - 1)
        w = round(tw + (bw - tw) * t)
        x = CX - w // 2
        y = pot_top + i
        c.r(x, y, w, 1, POT)
        c.p(x, y, POT_L); c.p(x + w - 1, y, POT_D)
    c.r(CX - bw // 2, bottom - 1, bw, 1, POT_D)
    c.r(CX - tw // 2 - 1, pot_top, tw + 2, 2, POT_L)      # rim lip
    c.r(CX - tw // 2 - 1, pot_top + 1, tw + 2, 1, POT_D)
    for dx in (-tw // 2 + 2, 0, tw // 2 - 3):
        c.r(CX + dx, pot_top + pot_h // 2, 2, 2, POT_D)    # diamond studs
    # soil in the opening
    c.r(CX - tw // 2 + 1, pot_top - 1, tw - 2, 2, '#3d2b1a')
    c.r(CX - tw // 2 + 1, pot_top - 1, tw - 2, 1, '#241809')

    trunk_w = TRUNK_W
    trunk_bottom = pot_top + 1
    trunk_top = trunk_bottom - (TRUNK_H - squash * 2)
    tx = CX - trunk_w // 2

    # arms anchored to trunk_bottom (fixed offsets) so they never drift off-canvas
    armL_y = trunk_bottom - 9
    c.r(tx - 7, armL_y, 7 + trunk_w // 2, 3, CACT)
    c.r(tx - 7, armL_y, 7 + trunk_w // 2, 1, CACT_L)
    c.r(tx - 7, armL_y - 6, 3, 9, CACT)
    c.r(tx - 7, armL_y - 6, 1, 9, CACT_L); c.r(tx - 5, armL_y - 6, 1, 9, CACT_D)
    c.r(tx - 7, armL_y - 7, 3, 2, CACT_L)

    armR_y = trunk_bottom - 12 + leaf_sway
    can_hx, can_hy = tx + trunk_w + 9, armR_y - 5
    c.r(tx + trunk_w - 1, armR_y, 9, 3, CACT)
    c.r(tx + trunk_w - 1, armR_y, 9, 1, CACT_L)
    c.r(tx + trunk_w + 6, armR_y - 6, 3, 9, CACT)
    c.r(tx + trunk_w + 6, armR_y - 6, 1, 9, CACT_L); c.r(tx + trunk_w + 8, armR_y - 6, 1, 9, CACT_D)
    c.r(tx + trunk_w + 6, armR_y - 7, 3, 2, CACT_L)

    # watering can in the right hand (bright brass so it reads on green/olive)
    ccx, ccy = can_hx, max(2, can_hy - 3)
    ang = can_tilt
    c.r(ccx - 3 + ang, ccy, 6, 4, CAN)
    c.r(ccx - 3 + ang, ccy, 6, 1, CAN_L)
    c.r(ccx - 1 + ang, ccy - 2, 3, 2, CAN_D)              # handle nub
    c.line(ccx + 3 + ang, ccy + 1, ccx + 7 + ang, ccy - 1 + can_tilt, CAN_D, 1)  # spout
    c.p(ccx + 7 + ang, ccy - 1 + can_tilt, CAN_L)
    if drops:
        for i in range(drops):
            c.p(ccx + 8 + ang + i * 2, ccy + can_tilt + i, WATER)
    if drink:
        c.line(ccx + 7 + ang, ccy - 1 + can_tilt, tx + trunk_w - 1, trunk_top + 6, CAN_D, 1)

    # trunk (main saguaro column)
    c.box(tx, trunk_top, trunk_w, trunk_bottom - trunk_top, CACT, out=None, hi=CACT_L, sh=CACT_D)
    for yy in range(trunk_top + 2, trunk_bottom - 2, 3):
        c.p(tx + 1, yy, SPINE); c.p(tx + trunk_w - 2, yy + 1, SPINE)
    for yy in range(trunk_top + 2, trunk_bottom - 2, 4):
        c.p(tx - 1, yy, CACT_D)

    # face: big pale cartoon eyes with dark pupils, spaced apart with a gap so they read
    # as two distinct eyes (not one blob) even at tiny scale
    fy = trunk_top + 4
    ex0, ex1 = tx, tx + trunk_w - 3
    for ex in (ex0, ex1):
        c.r(ex, fy, 3, 4, EYE_W)
        c.r(ex, fy, 3, 1, mix(EYE_W, '#ffffff', .4))
    if face == 'smile':
        c.r(ex0 + 1, fy + 1, 1, 2, EYE_P); c.r(ex1 + 1, fy + 1, 1, 2, EYE_P)
        c.r(tx + 1, fy + 5, trunk_w - 2, 1, EYE_P)
        c.p(tx + 1, fy + 4, EYE_P); c.p(tx + trunk_w - 2, fy + 4, EYE_P)
    elif face == 'open':
        c.r(ex0, fy + 1, 1, 2, EYE_P); c.r(ex1 + 2, fy + 1, 1, 2, EYE_P)
        c.r(tx + 3, fy + 5, trunk_w - 6, 2, EYE_P)
    elif face == 'squint':
        c.r(ex0, fy + 2, 3, 1, EYE_P); c.r(ex1, fy + 2, 3, 1, EYE_P)
        c.r(tx + 1, fy + 5, trunk_w - 2, 1, EYE_P)
    c.p(tx - 1, fy + 3, BLUSH); c.p(tx + trunk_w, fy + 3, BLUSH)

    # flower on top
    fcx, fcy = CX, trunk_top - (2 if flower_open else 1)
    r = 3 if flower_open else 2
    for dx, dy in ((-r, 0), (r, 0), (0, -r), (0, r), (-r + 1, -r + 1)):
        c.circ(fcx + dx, fcy + dy, 2 if flower_open else 1, FLOWER)
    c.circ(fcx, fcy, 1, FLOWER_C)
    if not flower_open:
        c.r(fcx - 1, fcy - 3, 2, 2, CACT_D)             # closed bud cap

    if zzz:
        c.txt(min(CX + 13, W - 5), max(0, trunk_top - 7), 'Z', mix(ACCENT, '#ffffff', .3), 1)


def walk():
    """4-frame HOP: squash (anticipate), launch, descend, land squash. Max lift kept low so
    nothing clips the canvas top; lowest pixels always land back on row 34/35."""
    out = []
    cfgs = ((0, 1, 'squint', 0), (2, 0, 'open', -1), (1, 0, 'smile', 1), (0, 1, 'smile', 0))
    for lift, squash, face, tilt in cfgs:
        c = C(W, H)
        sprout(c, lift=lift, squash=squash, face=face, can_tilt=tilt)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    """Waters itself/the floor: can tilts, droplets arc out."""
    out = []
    cfgs = ((0, 0, 'squint'), (2, 2, 'open'), (3, 4, 'open'), (1, 1, 'smile'))
    for tilt, drops, face in cfgs:
        c = C(W, H)
        sprout(c, lift=0, squash=0, can_tilt=tilt, drops=drops, face=face)
        c.outline_alpha(); out.append(c)
    return out


def seat():
    c = C(W, H)
    # "sun lounger": tall gooseneck grow-lamp arching over a wide plant stand (reads as a rest spot alone)
    # soft light cone from the lamp shade (up-left) down onto the stand
    for y in range(6, 30):
        hw = 2 + (y - 6) * 9 // 24
        cx = 12 + (y - 6) * 8 // 24
        for x in range(cx - hw, cx + hw + 1):
            if (x + y) % 2 == 0 or abs(x - cx) <= 1:     # dithered beam = reads as light, not a solid shape
                c.p(x, y, GLOW if abs(x - cx) <= 1 else GLOW2)
    MET, MET_D, MET_L = '#8a8f7a', '#55594a', '#b8bda4'
    c.r(4, 5, 2, 30, MET)                       # pole on the LEFT (character's can arm is on the right)
    c.r(4, 5, 1, 30, MET_L)
    c.r(2, 33, 8, 2, MET_D); c.r(2, 33, 8, 1, MET)     # weighted foot
    c.r(4, 3, 5, 2, MET); c.r(4, 3, 5, 1, MET_L)       # gooseneck top bar
    # lamp shade
    c.r(7, 3, 11, 3, '#4a4536'); c.r(7, 3, 11, 1, '#6a6450')
    c.r(8, 6, 9, 1, mix(ACCENT, '#ffffff', .35)); c.r(10, 6, 4, 1, '#ffffff')
    # wooden saucer/plant stand, low to the floor
    c.ell(CX, 33, 13, 3, WOOD_D)
    c.ell(CX, 32, 13, 3, WOOD)
    c.r(9, 32, 22, 1, WOOD_L)
    c.r(11, 29, 2, 4, WOOD_D); c.r(27, 29, 2, 4, WOOD_D)
    c.ell(CX, 29, 9, 2, WOOD_L)
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        sprout(c, lift=0, seat_top=32,
               flower_open=(k == 0), zzz=(k == 0),
               drink=(k == 1), leaf_sway=(1 if k == 1 else 0),
               face='open' if k == 0 else 'smile')
        c.outline_alpha(); out.append(c)
    return out
