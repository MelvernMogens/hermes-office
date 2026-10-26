"""Video/production floor cleaner: 'Grip' - a big FLYING CAMERA DRONE (non-humanoid,
NO legs). Round camera-lens eye up front, blinking red tally light, two rotor masts with
spinning-blur propellers on top, a microfiber cloth dangling from a hook-claw underneath.
It hovers at head height: body floats well clear of the floor, only a soft dark ground
shadow touches the floor as the anchor.
Canvas 40x36 cells, anchor bottom-centre (shadow on row 35, body centred on x=20), faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Grip', 'persona': 'Autonomous gimbal drone that chases the shot and polishes its own lens.',
        'fx': 'sparkle', 'fxColor': '#d9b8ff'}

W, H = 40, 36
FLOOR = '#1f1b27'
ACCENT = '#b36bff'
PURPLE = '#3a2452'

BODY, BODY_D, BODY_L = '#4a4058', '#2a2434', '#6b6080'
RING, RING_D = '#8f84a3', '#5c5468'
LENS_RIM = '#171219'
LENS_GLASS, LENS_GLASS_D = mix(ACCENT, '#000000', .35), mix(ACCENT, '#000000', .6)
LENS_HI = '#f2e8ff'
REC, REC_D = '#ff3b4e', '#8a1622'
ARM, ARM_D = '#26202f', '#140f1a'
PROP, PROP_MID, PROP_FAINT = '#f0ecf7', '#c9beDF'.lower(), mix('#c9beDF'.lower(), FLOOR, .55)
CABLE = '#5b4f6e'
CLAW = '#171219'
CLOTH, CLOTH_D, CLOTH_L = '#dfe6f5', '#a9b4cc', '#ffffff'
SHADOW = '#0f0c14'
PAD, PAD_D, PAD_L = '#241a30', '#140e1c', '#3a2a4c'
PAD_RING = '#c9a9f2'
SCREEN, SCREEN_D = '#120d18', '#3a2a4c'
LED_ON, LED_OFF = '#6bff9c', '#2a4a38'
GLOW = mix(ACCENT, FLOOR, .55)
GLOW2 = mix(ACCENT, FLOOR, .75)

CX = 20
BODY_W, BODY_H = 20, 16              # big hover body: 20 wide x 16 tall
X0 = CX - BODY_W // 2                # 10


def shadow(c, rx=8):
    c.ell(CX, 35, rx, 1, SHADOW)
    c.ell(CX, 34, max(1, rx - 2), 1, mix(SHADOW, FLOOR, .3))


def blur_bar(c, hubx, huby, w, phase=0):
    """A spinning-propeller motion blur disc: wide faint halo ellipse, a brighter inner
    streak, and two diagonal tick marks (angle flips with `phase`) so it reads as a blade
    sweeping through rather than a static bar."""
    c.ell(hubx, huby, w // 2, 1, PROP_FAINT)                    # soft wide blur halo
    c.r(hubx - w // 2 + 2, huby, w - 4, 1, PROP)                # brighter core streak
    c.p(hubx - w // 2 + 1, huby, PROP_MID); c.p(hubx + w // 2 - 2, huby, PROP_MID)
    if phase == 0:
        c.p(hubx - 3, huby - 1, PROP_MID); c.p(hubx + 3, huby + 1, PROP_MID)
    else:
        c.p(hubx - 3, huby + 1, PROP_MID); c.p(hubx + 3, huby - 1, PROP_MID)
    c.p(hubx, huby - 1, PROP_FAINT); c.p(hubx, huby + 1, PROP_FAINT)  # blade sweep hint


def drone(c, top, rec_on=False, propL=13, propR=13, cloth_dx=0, cloth_len=4, glint=False, sparkle=False):
    """Draw the whole hovering drone. top = y of body's top-left."""
    bx0, by0 = X0, top
    c.r(bx0 + 1, by0 + BODY_H - 1, BODY_W - 2, 2, mix(BODY_D, '#000000', .3))  # under-vent
    # dangling cable + hook claw + cloth (behind body)
    cx0, cy0 = CX, by0 + BODY_H - 1
    cx1, cy1 = CX + cloth_dx, cy0 + cloth_len
    c.line(cx0, cy0, cx1, cy1, CABLE, 1)
    c.r(cx1 - 3, cy1, 6, 2, CLAW)                                    # claw housing
    c.p(cx1 - 3, cy1 + 1, CLOTH); c.p(cx1 + 2, cy1 + 1, CLOTH)        # two claw tips gripping
    c.r(cx1 - 5, cy1 + 2, 11, 6, CLOTH)                               # draped fabric body
    c.r(cx1 - 5, cy1 + 2, 11, 1, CLOTH_L)
    c.line(cx1 - 4, cy1 + 6, cx1, cy1 + 5, CLOTH_D, 1)                # fold crease
    c.line(cx1 + 1, cy1 + 5, cx1 + 5, cy1 + 7, CLOTH_D, 1)            # second fold
    c.p(cx1 - 5, cy1 + 7, CLOTH_D); c.p(cx1 + 5, cy1 + 7, CLOTH_D)    # ragged bottom corners
    c.p(cx1 - 1, cy1 + 7, CLOTH_D)
    if sparkle:
        c.p(cx1 + 6, cy1 + 3, '#ffffff'); c.p(cx1 + 7, cy1 + 5, LENS_HI)
        c.p(cx1 - 7, cy1 + 4, LENS_HI)
    # rotor masts (drawn before body so body overlaps mast roots)
    mLx, mRx = bx0 + 4, bx0 + BODY_W - 5
    mTop = by0 - 9
    hubL, hubR = (mLx - 3, mTop), (mRx + 3, mTop)
    c.line(mLx, by0, hubL[0], hubL[1], ARM, 1)
    c.line(mRx, by0, hubR[0], hubR[1], ARM, 1)
    c.p(hubL[0], hubL[1], ARM_D); c.p(hubR[0], hubR[1], ARM_D)
    blur_bar(c, hubL[0], hubL[1], propL, phase=0)
    blur_bar(c, hubR[0], hubR[1], propR, phase=1)
    # main body shell
    c.box(bx0, by0, BODY_W, BODY_H, BODY, out=None, hi=BODY_L, sh=BODY_D)
    c.r(bx0 + 2, by0 + 1, BODY_W - 4, 1, BODY_L)
    c.r(bx0 + 2, by0 + BODY_H - 2, BODY_W - 4, 1, BODY_D)
    c.ring(CX, by0 + BODY_H // 2, 5, RING_D, th=1)
    # camera lens up front (right side), protruding past the body edge
    lcx, lcy = bx0 + BODY_W + 3, by0 + BODY_H // 2
    c.circ(lcx, lcy, 5, LENS_RIM)
    c.ring(lcx, lcy, 5, RING, th=1)
    c.circ(lcx, lcy, 4, LENS_GLASS_D)
    c.circ(lcx - 1, lcy - 1, 3, LENS_GLASS)
    c.p(lcx - 2, lcy - 2, LENS_HI); c.p(lcx - 3, lcy - 1, LENS_HI)
    if glint:
        c.p(lcx + 3, lcy - 5, '#ffffff'); c.p(lcx + 4, lcy - 4, '#ffffff')
        c.p(lcx + 2, lcy - 6, LENS_HI)
    # tally / REC light on top of the body
    c.r(bx0 + BODY_W - 5, by0 - 3, 4, 3, REC if rec_on else REC_D)
    c.p(bx0 + BODY_W - 4, by0 - 4, '#ffffff' if rec_on else REC_D)


def walk():
    out = []
    tops = (14, 13, 14, 13)
    props = ((13, 8), (8, 13), (13, 8), (8, 13))
    recs = (True, False, True, False)
    cdx = (-2, 0, 2, 0)
    for top, (pl, pr), rec, dx in zip(tops, props, recs, cdx):
        c = C(W, H)
        shadow(c, rx=8 - abs(top - 14))
        drone(c, top, rec_on=rec, propL=pl, propR=pr, cloth_dx=dx, cloth_len=4)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    out = []
    tops = (15, 14, 15, 14)
    cdx = (-9, -3, 5, 9)
    glints = (False, True, False, True)
    sparkles = (True, False, True, False)
    props = ((13, 8), (8, 13), (13, 8), (8, 13))
    for top, dx, gl, sp, (pl, pr) in zip(tops, cdx, glints, sparkles, props):
        c = C(W, H)
        shadow(c, rx=6)
        drone(c, top, rec_on=True, propL=pl, propR=pr, cloth_dx=dx, cloth_len=9, glint=gl, sparkle=sp)
        c.outline_alpha(); out.append(c)
    return out


PAD_TOP = 10   # row of the landing pad's flat top surface - shared by seat() and docked()


def seat():
    """Charging tripod stand: splayed 3-leg base + centre pole + a FLAT rectangular landing
    pad plate on top that the drone docks onto. Stand spans floor (row 35) up to the pad."""
    c = C(W, H)
    LEG_COL, LEG_COL_D = mix(ARM, '#ffffff', .18), ARM_D   # lighter leg tone, reads against dark floor
    # 3 splayed tripod legs, hub near row 23
    hub = (CX, 23)
    feet = ((10, 35), (CX, 35), (30, 35))
    for fx, fy in feet:
        c.line(hub[0], hub[1], fx, fy, LEG_COL, 2)
        c.line(hub[0] + 1, hub[1], fx + 1, fy, LEG_COL_D, 1)
        c.r(fx - 2, fy - 1, 4, 2, LEG_COL_D)                   # foot pad
    c.circ(hub[0], hub[1], 3, LEG_COL_D)
    # centre pole up to the landing pad
    c.r(CX - 1, PAD_TOP + 3, 2, hub[1] - (PAD_TOP + 3), LEG_COL_D)
    c.r(CX - 1, PAD_TOP + 3, 1, hub[1] - (PAD_TOP + 3), LEG_COL)
    # FLAT rectangular landing pad plate: square corners, crisp flat top edge (no round dome)
    plate_w = 21
    px0 = CX - plate_w // 2
    c.r(px0, PAD_TOP, plate_w, 4, PAD_D)                              # base slab
    c.r(px0, PAD_TOP, plate_w, 1, PAD_L)                              # crisp flat top highlight edge
    c.r(px0, PAD_TOP + 1, plate_w, 2, PAD)                            # body of the plate
    c.r(px0, PAD_TOP + 3, plate_w, 1, PAD_D)                          # bottom shade edge
    c.r(px0, PAD_TOP, 1, 4, PAD_D); c.r(px0 + plate_w - 1, PAD_TOP, 1, 4, PAD_D)  # square side edges
    # small square LED (not circular, avoids reading as a dome bump) on the pad's top surface
    c.r(CX - 2, PAD_TOP + 1, 4, 2, mix(ACCENT, '#ffffff', .15))
    c.r(CX - 1, PAD_TOP + 1, 2, 1, '#ffffff')
    # a coiled charge cable resting at the base for flavour
    c.line(6, 33, 9, 31, CABLE, 1); c.line(9, 31, 6, 29, CABLE, 1); c.p(6, 27, CABLE)
    c.outline_alpha(); return c


def docked(c, rec_on=False, batt=None, zzz=False):
    """Compact folded drone resting ON the landing pad (character only, drawn in the sit
    frame; the pad/stand itself lives in seat()). Body bottom sits flush on PAD_TOP (no
    gap, no overlap into the plate)."""
    bw, bh = 16, 7
    bx0, by0 = CX - bw // 2, PAD_TOP - bh   # body's bottom edge lands exactly on the plate top
    # folded rotor arms lying flat along the top of the body
    c.line(bx0 + 2, by0 + 1, bx0 - 2, by0 - 1, ARM, 1)
    c.line(bx0 + bw - 2, by0 + 1, bx0 + bw + 2, by0 - 1, ARM, 1)
    c.p(bx0 - 2, by0 - 1, ARM_D); c.p(bx0 + bw + 2, by0 - 1, ARM_D)
    c.line(bx0 - 2, by0 - 1, bx0 - 5, by0, PROP_FAINT, 1)             # drooped folded blade
    c.line(bx0 + bw + 2, by0 - 1, bx0 + bw + 5, by0, PROP_FAINT, 1)
    # body shell, sitting on the pad
    c.box(bx0, by0, bw, bh, BODY, out=None, hi=BODY_L, sh=BODY_D)
    c.r(bx0 + 2, by0 + 1, bw - 4, 1, BODY_L)
    # lens, dimmed / resting
    lcx, lcy = bx0 + bw + 2, by0 + bh // 2
    c.circ(lcx, lcy, 4, LENS_RIM)
    c.ring(lcx, lcy, 4, RING, th=1)
    c.circ(lcx, lcy, 3, LENS_GLASS_D)
    c.p(lcx - 1, lcy - 1, LENS_GLASS)
    # tally / charging LED on top
    c.r(bx0 + bw - 5, by0 - 2, 4, 2, REC if rec_on else REC_D)
    if batt is not None:
        c.box(bx0 + 2, by0 + 2, 6, 4, SCREEN, out=None, hi=SCREEN_D, sh=SCREEN_D)
        fw = max(0, min(4, batt))
        if fw: c.r(bx0 + 3, by0 + 3, fw, 2, LED_ON)
    if zzz:
        c.txt(bx0 + bw + 5, by0 + 1, 'Z', mix(ACCENT, '#ffffff', .3), 1)
        c.txt(bx0 + bw + 8, by0 - 2, 'Z', mix(ACCENT, '#ffffff', .3), 1)


def sit():
    out = []
    for k in range(2):
        c = C(W, H)          # character ONLY; engine draws seat() underneath in the same box
        docked(c, rec_on=False, batt=(4 if k == 1 else None), zzz=(k == 0))
        c.outline_alpha(); out.append(c)
    return out
