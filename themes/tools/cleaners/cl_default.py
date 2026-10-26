"""Default (MEGATRON floor) cleaner: 'Scrap-7', a squat angular mecha maintenance drone.
Gunmetal + silver plating, purple pauldrons, single red visor slit, digitigrade (reverse-knee)
legs, backpack energon-vacuum tank with a hose nozzle that glows cyan when sucking up spills.
Canvas 40x36 cells, anchor bottom-centre (feet row 35, body centre x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Scrap-7',
        'persona': 'Squat maintenance drone that vacuums spilled energon and quietly dreams of conquest.',
        'fx': 'energon', 'fxColor': '#22e3ff'}

W, H = 40, 36
G1, G2, G3 = '#6b6f80', '#454955', '#2b2d36'       # gunmetal light/mid/dark
SIL, SIL_D = '#b8bfca', '#838a97'                  # silver plate
PUR, PUR_D = '#a855f7', '#7c3aed'                  # purple accent
RED, RED_D = '#ff2d3d', '#8a141d'                  # visor glow / dim
CY, CY_D = '#22e3ff', '#0fa8bf'                    # energon cyan
NOZ, NOZ_D = '#3a3f4c', '#22242c'                  # dark metal feet/nozzle


def head(c, y0, dim=False):
    """Angular boxy head, y0 = top of skull. Faces right (visor + brow on the right)."""
    c.box(15, y0, 10, 7, G1, out=None, hi=lt(G1, .2), sh=G3)
    c.r(15, y0 - 1, 5, 1, SIL)                          # crest fin left
    c.r(16, y0 - 2, 3, 1, SIL_D)
    c.r(23, y0 + 1, 3, 3, G3)                            # brow/snout block right
    c.r(24, y0 + 2, 2, 1, RED_D if dim else RED)          # visor slit
    c.r(15, y0 + 2, 2, 2, PUR)                            # ear plate
    c.r(15, y0 + 6, 10, 1, G3)
    c.r(17, y0 + 6, 3, 3, G3)                             # neck stub
    return y0 + 9  # neck bottom


def torso(c, ny, bob=0):
    """ny = neck bottom (torso top). Wide chest block + pauldrons + backpack tank."""
    y0 = ny
    c.box(6, y0 + 1, 6, 9, G3, out=None, hi=G2, sh='#181920')   # backpack tank (behind, left)
    c.r(7, y0 + 2, 3, 3, mix(CY, CY_D, .3))                      # tank window (energon level)
    c.r(7, y0 + 6, 4, 1, SIL_D)
    c.r(8, y0 + 8, 1, 1, CY)                                     # status LED
    c.box(13, y0, 15, 12, G2, out=None, hi=G1, sh=G3)            # chest block
    c.r(13, y0 + 11, 15, 1, G3)
    c.r(10, y0 + 1, 3, 6, PUR_D); c.r(10, y0 + 1, 3, 1, PUR)     # L pauldron
    c.r(27, y0 + 1, 3, 6, PUR_D); c.r(27, y0 + 1, 3, 1, PUR)     # R pauldron
    c.r(17, y0 + 2, 7, 4, SIL)                                   # chest plate
    c.r(18, y0 + 6, 5, 2, SIL_D)
    c.r(19, y0 + 3, 4, 2, PUR); c.r(19, y0 + 3, 4, 1, lt(PUR, .3))  # core
    c.r(15, y0 + 8, 4, 3, G1); c.r(22, y0 + 8, 4, 3, G1)         # ab plates
    c.r(19, y0 + 8, 3, 3, G3)
    return y0 + 12  # hip line


def legs(c, hy, pose):
    """Digitigrade reverse-knee legs. pose: 0 stand, 1 L fwd, 2 R fwd."""
    if pose == 0:
        c.r(15, hy, 4, 5, G2); c.r(21, hy, 4, 5, G2)                     # thighs
        c.r(13, hy + 5, 4, 4, G1); c.r(23, hy + 5, 4, 4, G1)             # shins (knee kink out)
        c.r(11, hy + 9, 7, 4, NOZ); c.r(22, hy + 9, 7, 4, NOZ)           # feet
        c.r(11, hy + 9, 7, 1, NOZ_D); c.r(22, hy + 9, 7, 1, NOZ_D)
    elif pose == 1:  # left foot forward, right back
        c.r(15, hy, 4, 4, G2); c.r(22, hy, 4, 6, G2)
        c.r(12, hy + 4, 4, 5, G1); c.r(24, hy + 6, 4, 4, G1)
        c.r(9, hy + 9, 7, 4, NOZ); c.r(24, hy + 10, 7, 3, NOZ)
        c.r(9, hy + 9, 7, 1, NOZ_D); c.r(24, hy + 10, 7, 1, NOZ_D)
    else:  # right foot forward, left back
        c.r(15, hy, 4, 6, G2); c.r(22, hy, 4, 4, G2)
        c.r(12, hy + 6, 4, 4, G1); c.r(24, hy + 4, 4, 5, G1)
        c.r(9, hy + 10, 7, 3, NOZ); c.r(24, hy + 9, 7, 4, NOZ)
        c.r(9, hy + 10, 7, 1, NOZ_D); c.r(24, hy + 9, 7, 1, NOZ_D)


def arm_hose(c, ny, hx, hy, on=False, t=0):
    """Right arm reaching to hose grip, hose down to nozzle sucking energon puddle at (hx,hy)."""
    c.line(27, ny + 3, 30, ny + 9, G2, 2)
    c.r(30, ny + 8, 3, 3, SIL_D)                                    # claw hand
    c.line(31, ny + 10, hx, hy - 6, NOZ, 1)
    c.line(32, ny + 10, hx + 1, hy - 6, NOZ_D, 1)
    r = 3 if not on else 3 + (1 if t % 2 else 0)
    c.r(hx - 1, hy - 3, 4, 3, NOZ)                                  # nozzle head
    if on:
        glow = CY if t % 2 == 0 else lt(CY, .3)
        c.ell(hx + 1, hy + 1, r, r - 1, mix(glow, '#000000', .0))
        c.ell(hx + 1, hy + 1, max(1, r - 2), max(1, r - 2), lt(glow, .3))


def build(bob, legpose, hose_on=False, t=0, hx=32, hy=34, dim=False):
    c = C(W, H)
    ny = head(c, 4 - bob, dim=dim)
    hy2 = torso(c, ny, bob)
    legs(c, hy2, legpose)
    arm_hose(c, ny, hx, hy, hose_on, t)
    c.outline_alpha()
    return c


def walk():
    return [build(0, 1), build(1, 0), build(0, 2), build(1, 0)]


def clean():
    out = []
    for t in range(4):
        c = C(W, H)
        ny = head(c, 4)
        hy2 = torso(c, ny, 0)
        legs(c, hy2, 0)
        pr = 3 + (t % 2)
        glow = CY if t % 2 == 0 else lt(CY, .25)
        c.ell(33, 34, pr, 2, dk(glow, .2))
        c.ell(33, 34, max(1, pr - 2), 1, lt(glow, .2))
        arm_hose(c, ny, 32, 34, on=True, t=t)
        c.outline_alpha()
        out.append(c)
    return out


def seat():
    """Hex charging dock: low platform + short pylon, purple/cyan glow."""
    c = C(W, H)
    c.r(8, 32, 24, 3, G3)
    c.r(8, 32, 24, 1, G2)
    c.r(6, 34, 28, 2, '#1d1e24')
    c.r(10, 30, 20, 2, G2)
    c.r(12, 29, 16, 1, SIL_D)
    for x in (11, 17, 23, 28):
        c.r(x, 30, 1, 2, mix(PUR, CY, .5))
    c.r(17, 20, 6, 10, G3, )
    c.ol(17, 20, 6, 10, dk(G3, .4))
    c.r(18, 21, 4, 8, G2)
    c.r(19, 15, 2, 6, PUR_D)
    c.r(19, 13, 2, 3, PUR)
    c.circ(20, 12, 2, mix(PUR, CY, .4))
    c.circ(20, 12, 1, lt(CY, .3))
    c.outline_alpha()
    return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = 12
        c.r(13, y0 + 10, 6, 6, G1); c.r(21, y0 + 10, 6, 6, G1)       # crouched thighs
        c.r(11, y0 + 15, 8, 4, NOZ); c.r(21, y0 + 15, 8, 4, NOZ)     # folded feet
        c.box(12, y0 + 2, 16, 9, G2, out=None, hi=G1, sh=G3)         # crouched torso
        c.r(9, y0 + 2, 3, 7, PUR_D); c.r(28, y0 + 2, 3, 7, PUR_D)
        c.r(17, y0 + 4, 6, 3, SIL)
        c.r(18, y0 + 4, 4, 1, mix(PUR, CY, .3) if k == 0 else PUR)
        dim = (k == 1)
        head(c, y0 - 6, dim=dim)
        if k == 0:
            c.r(27, y0 - 8, 1, 3, lt(CY, .2)); c.r(28, y0 - 6, 1, 2, lt(CY, .2))  # charge bolt
        else:
            c.txt(27, y0 - 10, 'Z', mix(PUR, CY, .5), 1)
        c.outline_alpha()
        out.append(c)
    return out
