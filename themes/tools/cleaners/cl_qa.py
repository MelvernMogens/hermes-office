"""QA lab floor cleaner: 'Sterile Sam' - a round hovering sterile lab pod (NOT a biped).
Glass-dome pod body drifts on a small anti-grav thruster ring (soft cyan glow, gap above the
floor, faint shadow keeps it anchored). Thin left arm holds a magnifier/checklist, thin right
arm holds a disinfectant spray wand. Docks nose-down in a UV sterilisation cradle to rest.
Canvas 40x36 cells, anchor bottom-centre (shadow on row 34-35, body centred on x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Sterile Sam', 'persona': 'Hovering cleanroom pod that disinfects every keyboard between builds.',
        'fx': 'mist', 'fxColor': '#b8ffcf'}

W, H = 40, 36
POD, POD_D, POD_L = '#eef0f2', '#c3c8cf', '#ffffff'
GLASS, GLASS_D, GLASS_L = '#2f6b85', '#1c4356', '#a9f2ff'
EYE, EYE_D = '#ff6b6f', '#a92e33'
GLOVE, GLOVE_D = '#3ecf6e', '#279650'          # sterile-green trim
THR, THR_D, THR_L = '#7c828c', '#565c66', '#aeb6c0'   # thruster housing
HOVER, HOVER_D = '#7ce8ff', '#2fb8d8'          # anti-grav glow
ARM, ARM_D = '#9aa2ac', '#6b727c'
SHADOW = '#0a0d1066'


def pod(c, bob=0, eye_on=True, tuck=0):
    """Round glass-dome pod. bob = whole-pod float offset (0/1). tuck<0 pulls arms inward (docked)."""
    cy = 12 - bob
    c.ell(20, cy + 1, 9, 8, POD)
    c.ell(17, cy - 2, 4, 3, POD_L)                      # top-left highlight
    c.ell(23, cy + 5, 5, 3, POD_D)                      # bottom-right shade
    c.ell(20, cy - 2, 7, 5, GLASS)                       # glass dome window
    c.ell(18, cy - 4, 3, 2, GLASS_L)                     # glass glare
    c.circ(24, cy - 1, 2, dk(GLASS, .1))
    c.circ(24, cy - 1, 1, EYE if eye_on else EYE_D)      # sensor eye, right-facing
    c.r(13, cy + 3, 14, 2, GLOVE)                        # sterile-green belt band
    c.r(13, cy + 4, 14, 1, GLOVE_D)
    # short skirt tapering to the thruster collar
    c.ell(20, cy + 9, 6, 3, POD_D)
    return cy


def thruster(c, base_y, flicker=0):
    """Anti-grav ring below the pod: housing + pulsing cyan glow, then a gap, then a floor shadow."""
    ty = base_y + 12
    c.ell(20, ty, 6, 2, THR)
    c.ell(20, ty, 6, 1, THR_L)
    c.ell(20, ty + 2, 5, 2, THR_D)
    glow = HOVER if flicker % 2 == 0 else lt(HOVER, .25)
    c.ell(20, ty + 4, 7 - (flicker % 2), 2, mix(glow, '#000000', .05))
    c.ell(20, ty + 4, 4, 1, lt(glow, .3))
    # floor shadow, further down with a visible transparent gap in between (hover anchor)
    c.ell(20, 35, 6 - (flicker % 2), 1, SHADOW)
    c.ell(20, 34, 4, 1, SHADOW)


def wand_arm(c, cy, hx, hy, spray=0):
    """Right thin arm reaching to a spray-wand hand."""
    c.line(27, cy + 2, hx, hy, ARM, 1)
    c.r(hx - 1, hy - 1, 3, 3, ARM_D)
    c.r(hx + 2, hy, 4, 2, THR)
    c.r(hx + 6, hy - 1, 2, 4, THR_D)
    if spray:
        for i in range(spray):
            col = GLOVE if i % 2 == 0 else lt(GLOVE, .4)
            c.circ(hx + 9 + i * 2, hy + 1 + (i % 3) - 1, 1, col)


def check_arm(c, cy, hx, hy):
    """Left thin arm holding a small magnifier/checklist."""
    c.line(13, cy + 2, hx, hy, ARM, 1)
    c.r(hx - 2, hy - 1, 3, 3, ARM_D)
    c.ring(hx - 4, hy + 2, 2, POD_L, th=1)
    c.p(hx - 2, hy + 4, ARM_D)


def build(bob=0, flicker=0, spray=0, eye_on=True):
    c = C(W, H)
    cy = pod(c, bob, eye_on)
    check_arm(c, cy, 8, 20 - bob)
    wand_arm(c, cy, 30, 21 - bob, spray)
    thruster(c, cy + 12, flicker)
    c.outline_alpha()
    return c


def walk():
    return [build(0, 0), build(1, 1), build(0, 2), build(1, 3)]


def clean():
    return [build(0, 0, spray=2), build(1, 1, spray=4), build(0, 2, spray=2), build(1, 3, spray=3)]


def seat():
    """UV sterilisation cradle: two side poles + an arch of UV lamps, base pad on the floor."""
    c = C(W, H)
    c.r(10, 33, 21, 2, THR_D)
    c.r(10, 33, 21, 1, THR)
    c.r(8, 35, 25, 1, dk(THR_D, .3))
    # yellow/black hazard stripe along the base front edge (sterile-zone marking)
    for i, x in enumerate(range(9, 30, 2)):
        c.r(x, 34, 1, 1, '#e8c94a' if i % 2 == 0 else '#1a1a1a')
    c.r(11, 10, 3, 24, THR)
    c.r(27, 10, 3, 24, THR)
    c.r(11, 10, 1, 24, THR_L); c.r(27, 10, 1, 24, THR_L)
    c.r(12, 33, 1, 1, THR_D); c.r(28, 33, 1, 1, THR_D)
    # arch across the top joining the poles
    c.r(11, 7, 19, 4, THR_D)
    c.r(11, 7, 19, 1, THR)
    c.r(13, 6, 15, 1, THR_L)
    # UV lamp strip along the underside of the arch
    for i, x in enumerate(range(13, 27, 3)):
        c.r(x, 11, 2, 1, mix('#b46cff', '#e9c8ff', .3) if i % 2 == 0 else '#7c3aed')
    c.r(13, 11, 14, 1, dk('#7c3aed', .2))
    # faint downward UV glow beam from the arch (purple wash between the poles)
    for i, y in enumerate(range(12, 24, 3)):
        w = 12 - i
        c.r(20 - w // 2, y, w, 1, mix('#7c3aed', THR, .75))
    # small status console at the base
    c.box(30, 24, 6, 6, THR, out=None, hi=THR_L, sh=THR_D)
    c.r(32, 26, 2, 1, GLOVE)
    c.r(32, 28, 2, 1, EYE_D)
    c.outline_alpha()
    return c


def sit():
    """Pod docked in the cradle: hovers just inside the arch, arms tucked, eye pulses."""
    out = []
    for k in range(2):
        c = C(W, H)
        cy = 14
        c.ell(20, cy + 1, 8, 7, POD)
        c.ell(17, cy - 2, 4, 3, POD_L)
        c.ell(22, cy + 4, 5, 3, POD_D)
        c.ell(20, cy - 2, 6, 4, GLASS)
        c.ell(18, cy - 3, 2, 2, GLASS_L)
        c.circ(23, cy - 1, 2, dk(GLASS, .1))
        c.circ(23, cy - 1, 1, EYE if k == 0 else EYE_D)
        c.r(13, cy + 2, 14, 2, GLOVE)
        c.r(13, cy + 3, 14, 1, GLOVE_D)
        # arms tucked close against the body (docked)
        c.line(27, cy + 1, 30, cy + 3, ARM, 1); c.r(29, cy + 2, 2, 2, ARM_D)
        c.line(13, cy + 1, 10, cy + 3, ARM, 1); c.r(9, cy + 2, 2, 2, ARM_D)
        # small under-glow while charging/sterilising (docked, no floor shadow needed here)
        glow = HOVER if k == 0 else lt(HOVER, .3)
        c.ell(20, cy + 10, 5, 2, mix(glow, '#000000', .1))
        c.outline_alpha()
        out.append(c)
    return out
