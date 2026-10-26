"""Coder-floor cleaner: 'Byte-Vac', a wide RGB-strip robo-vacuum base on wheels, with a tall
telescoping mast that carries a small monitor-screen head showing status text (raised well
above the base so overall height matches the office's agent capsules). A little claw arm holds
a nozzle for the clean animation. Canvas 40x36 cells, anchor bottom-centre, faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Byte-Vac', 'persona': "Low-profile robo-vacuum that moonlights as the lab's tidiest code reviewer.",
        'fx': 'pixels', 'fxColor': '#39ff9c'}

W, H = 40, 36
BASE, BASE_D, BASE_L = '#5d6b78', '#3c4652', '#8795a2'   # disc shell (lifted: must read on floor #191f21)
SCR, SCR_D = '#1d2a2e', '#0e1416'                          # monitor screen bezel
GRN, CYN = '#39ff9c', '#2ee6e6'                            # accent greens/cyan
AMB = '#f5c542'
CLAW = '#7c8790'
WHEEL, WHEEL_D = '#14181b', '#0a0c0e'
RGB_SEQ = [GRN, CYN, '#5ef2c0', CYN]


def base_disc(c, bob, spin=0, rgb=GRN):
    """Wide low base (~20 cells) rolling on 2 visible wheels. bob shifts +/-1 whole sprite."""
    y = 27 - bob
    c.ell(20, y + 4, 12, 5, BASE)
    c.r(8, y + 2, 24, 5, BASE)
    c.ol(8, y + 2, 24, 5, dk(BASE, .3))
    c.r(9, y + 2, 22, 1, lt(BASE, .25))
    c.r(9, y + 6, 22, 1, BASE_D)
    # wheels (round, spokes rotate with `spin`)
    for wx in (11, 29):
        c.circ(wx, y + 9, 3, WHEEL)
        c.circ(wx, y + 9, 1, WHEEL_D)
        for i in range(2):
            ang = (i * 90 + spin * 45) % 180
            if ang < 90:
                c.r(wx - 2, y + 9, 4, 1, dk(CLAW, .2))
            else:
                c.r(wx, y + 7, 1, 4, dk(CLAW, .2))
    # RGB light strip along the base front edge, colour cycles by frame
    for i, x in enumerate(range(10, 28, 3)):
        c.r(x, y + 6, 2, 1, rgb if (i + spin) % 3 == 0 else dk(rgb, .35))
    c.r(30, y + 3, 2, 2, CLAW)                                     # bump sensor
    return y


def mast_head(c, base_y, ext=4, line2=None):
    """Tall telescoping mast rising from the base top to a monitor-screen head, well clear of the base."""
    ny = base_y - 10 - ext
    c.r(18, ny + 6, 4, base_y + 2 - (ny + 6), BASE_D)               # mast column
    c.r(19, ny + 6, 1, base_y + 2 - (ny + 6), lt(BASE_D, .3))
    for seg_y in range(ny + 10, base_y, 6):                          # telescope seam rings
        c.r(17, seg_y, 6, 1, dk(BASE_D, .25))
    c.r(17, ny + 4, 6, 3, BASE)                                     # neck collar
    c.box(12, ny - 8, 16, 9, SCR_D, out=None, hi='#2a3438', sh='#060809')  # monitor bezel
    c.r(14, ny - 7, 12, 6, SCR)                                     # screen
    c.r(15, ny - 5, 1, 2, GRN)
    c.r(16, ny - 5, 5, 1, GRN)
    if line2:
        c.r(15, ny - 3, 6, 1, mix(GRN, '#000000', .1) if line2 == 'bar1' else GRN)
    c.r(12, ny - 9, 16, 1, lt(SCR_D, .2))
    c.r(11, ny - 4, 1, 3, BASE_D); c.r(29, ny - 4, 1, 3, BASE_D)    # antenna stubs
    c.r(11, ny - 5, 1, 1, AMB); c.r(29, ny - 5, 1, 1, AMB)
    return ny


def claw_arm(c, base_y, side, tool=False, t=0):
    """Small claw arm from the base side. side=-1 left(back), +1 right(front)."""
    if side > 0:
        ex = 6 if not tool else 9
        c.line(30, base_y + 1, 30 + ex, base_y - 3 - (t % 2), CLAW, 2)
        c.r(29 + ex, base_y - 5 - (t % 2), 3, 3, dk(CLAW, .15))
        if tool:
            bx, by = 32 + ex, base_y - 4 - (t % 2)
            c.line(bx, by, bx + 3, by - 2, '#c9a24a', 1)             # mini brush handle
            for i in range(3):
                c.r(bx + 3, by - 3 + i, 2, 1, '#e8d9a0' if (i + t) % 2 else '#c9a24a')
    else:
        c.line(9, base_y + 1, 5, base_y - 2, CLAW, 2)
        c.r(3, base_y - 4, 3, 3, dk(CLAW, .15))


def build(bob=0, spin=0, ext=4, rgb_i=0, arm_t=0, tool=False, line2=None):
    c = C(W, H)
    by = base_disc(c, bob, spin, RGB_SEQ[rgb_i % len(RGB_SEQ)])
    mast_head(c, by, ext, line2)
    claw_arm(c, by, -1)
    claw_arm(c, by, 1, tool=tool, t=arm_t)
    c.outline_alpha()
    return c


def walk():
    return [build(0, 0, 3, 0), build(1, 2, 4, 1), build(0, 4, 3, 2), build(1, 0, 4, 3)]


def clean():
    out = []
    for t in range(4):
        c = build(t % 2, t, 3, t, arm_t=t, tool=True)
        # spinning brush at the base front, alternating bristle angle
        by = 27 - (t % 2)
        bx = 22 + (t % 2)
        c.ell(bx, by + 9, 3, 2, dk('#c9a24a', .1))
        for i in range(4):
            ang = (i + t) % 2
            c.r(bx - 2 + i, by + 8 + ang, 1, 2, '#e8d9a0')
        c.outline_alpha()
        out.append(c)
    return out


def seat():
    """Charging pad + a tall back pylon/tower so the dock reads at agent scale even when parked."""
    c = C(W, H)
    c.r(6, 31, 28, 4, '#12181a')
    c.ol(6, 31, 28, 4, '#0a0d0e')
    c.r(7, 32, 26, 1, lt('#12181a', .2))
    for i, x in enumerate(range(8, 34, 4)):
        c.r(x, 32, 3, 2, GRN if i % 2 == 0 else dk(GRN, .4))
    c.r(4, 33, 32, 2, '#0a0d0e')
    # tall charging tower behind the pad
    c.r(29, 8, 4, 23, BASE_D)
    c.r(29, 8, 1, 23, lt(BASE_D, .3))
    c.r(28, 6, 6, 4, BASE)
    c.ol(28, 6, 6, 4, dk(BASE, .3))
    c.r(29, 7, 4, 1, lt(BASE, .3))
    c.box(24, 11, 9, 6, SCR_D, out=None, hi='#2a3438', sh='#060809')
    c.r(26, 12, 5, 4, SCR)
    c.r(27, 13, 3, 1, GRN)
    # charge LED strip down the tower
    for y in range(16, 30, 3):
        c.r(30, y, 2, 1, CYN)
    c.outline_alpha()
    return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        by = base_disc(c, 0, k * 2, RGB_SEQ[k])
        # mast partially retracted, screen sits mid-height, docked against the tower
        ny = mast_head(c, by, ext=1, line2=None)
        if k == 0:
            c.txt(16, ny - 5, 'ZZ', GRN, 1)
        else:
            c.r(15, ny - 4, 8, 2, dk(GRN, .5))
            c.r(15, ny - 4, 4, 2, GRN)                                # loading bar
        # blinking charge LED on the tower edge, in front of the character
        c.r(30, by - 6, 2, 1, CYN if k == 0 else dk(CYN, .5))
        claw_arm(c, by, -1)
        claw_arm(c, by, 1)
        c.outline_alpha()
        out.append(c)
    return out
