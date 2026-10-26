"""War-room cleaner: 'Tempo' — a TALL SKINNY ROLLER-SKATER gliding on quad skates, not a
standard 2-leg walk. Very thin long limbs, tall head (top near y=2), strong forward lean with
one leg extended back pushing and the other tucked under — silhouette reads as a diagonal
lean, not an upright pill. Skates show a visible boot + 4 round wheels in a row (quad-skate
read, not sneakers). Carries a big light clipboard clamped in the front hand and a short-pole
flat squeegee/wiper pad (NOT a stringy mop) for cleaning, swept side to side while gliding.
Canvas 40x36 cells, anchor bottom-centre (skate wheels on row 35, body centred on x=20),
faces right."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from px import C, mix, dk, lt

META = {'name': 'Tempo', 'persona': 'Roller-skating PM who glides the floor clean between stand-ups.',
        'fx': 'sparkle', 'fxColor': '#2ec4b6'}

W, H = 40, 36
SKIN, SKIN_D = '#e0a878', '#b87c52'
JACKET, JACKET_D, JACKET_L = '#2ec4b6', '#1a8f85', '#5fe0d3'
LEG, LEG_D = '#33393c', '#1e2224'
HAIR, HAIR_D = '#2b1f18', '#170f0a'
HEADSET = '#c9ccd1'
CYAN = '#06b6d4'
BOOT, BOOT_D, BOOT_L = '#20242a', '#101216', '#3a4048'
SKATE_W, SKATE_W_D, SKATE_HUB = '#c7ccd3', '#7c828b', '#eef1f4'   # bright light-grey wheels + white hub
SKATE_FRAME = '#9aa0a8'
CLIP, CLIP_D = '#eef0f2', '#c3c8cf'
STICKY, STICKY_D = '#eab308', '#a6790a'
BOARD, BOARD_D, BOARD_L = '#163a37', '#0c211f', '#245e58'
STOOL, STOOL_D, STOOL_L = '#3a4b4d', '#26302f', '#557171'
PAD, PAD_D, PAD_L = '#dfe4e8', '#9aa3ab', '#f4f7f9'   # squeegee/wiper pad, distinct from mop
POLE, POLE_D = '#8f939a', '#5b5f66'
SILVER = '#c9ccd1'


def skate(c, x, y, tilt=0):
    """Quad roller skate: dark boot + frame + 4 bright round wheels in a row (reads as SKATE,
    not a shoe). Drawn at foot position (x,y = bottom-front of the boot)."""
    c.box(x - 2, y - 5, 6, 5, BOOT, out=None, hi=BOOT_L, sh=BOOT_D)          # ankle boot
    c.r(x - 2, y - 5, 6, 1, lt(BOOT, .35))
    c.r(x + 2, y - 3, 2, 2, HEADSET)                                        # buckle strap glint
    c.r(x - 4, y - 1, 10, 2, SKATE_FRAME); c.r(x - 4, y - 1, 10, 1, lt(SKATE_FRAME, .2))  # wheel frame/plate
    # 4 wheels in a row (quad skate), bright so they read against the dark floor
    xs = (x - 3, x - 1 + tilt, x + 2 - tilt, x + 4)
    for i, wx in enumerate(xs):
        wy = y + 1 + (tilt if i in (1,) else (-tilt if i == 2 else 0))
        c.circ(wx, wy, 1, SKATE_W); c.circ(wx, wy, 1, SKATE_W_D if i % 2 else SKATE_W)
        c.p(round(wx), round(wy), SKATE_HUB)


def glide_legs(c, phase, y0):
    """phase 0..3: one long thin leg extended back pushing, other bent under the leaning torso.
    Whole leg pair sits under a forward-leaning hip so the silhouette is diagonal."""
    hip_x, hip_y = 17, y0 + 20
    if phase == 0:      # push leg fully extended back-left & low
        c.line(hip_x, hip_y, 6, 33, LEG, 3); c.line(hip_x + 1, hip_y, 7, 33, LEG_D, 1)
        skate(c, 6, 33)
        c.line(hip_x + 3, hip_y, 23, 30, LEG, 3)
        skate(c, 23, 30, tilt=1)
    elif phase == 1:    # gathering: both legs closer under body, lowest crouch
        c.line(hip_x, hip_y, 12, 34, LEG, 3)
        skate(c, 12, 34)
        c.line(hip_x + 2, hip_y, 22, 33, LEG, 3)
        skate(c, 22, 33)
    elif phase == 2:    # push leg extended back-right, opposite of phase 0
        c.line(hip_x, hip_y, 9, 30, LEG, 3)
        skate(c, 9, 30, tilt=1)
        c.line(hip_x + 3, hip_y, 27, 33, LEG, 3); c.line(hip_x + 4, hip_y, 28, 33, LEG_D, 1)
        skate(c, 27, 33)
    else:                # tall glide: both legs long and close, highest stance
        c.line(hip_x, hip_y, 13, 32, LEG, 3)
        skate(c, 13, 32)
        c.line(hip_x + 2, hip_y, 21, 31, LEG, 3)
        skate(c, 21, 31)


def torso(c, y0, lean):
    """Long thin torso leaning forward by `lean` cells at the shoulders."""
    hip_x = 17
    c.line(hip_x, y0 + 20, hip_x + lean, y0 + 4, JACKET, 7)
    c.line(hip_x + 1, y0 + 20, hip_x + 1 + lean, y0 + 4, JACKET_D, 2)
    c.line(hip_x - 2, y0 + 20, hip_x - 2 + lean, y0 + 4, JACKET_L, 1)
    c.r(hip_x - 1 + lean, y0 + 9, 2, 5, SILVER)                                  # lanyard/stopwatch strap
    c.circ(hip_x + lean, y0 + 14, 2, dk(SILVER, .1)); c.circ(hip_x + lean, y0 + 14, 1, CYAN)


def head(c, y0, lean, blink=False):
    """Tall thin head, top near y=2, riding atop the leaning torso."""
    hx = 12 + lean
    c.box(hx, y0 - 5, 9, 9, SKIN, out=None, hi=lt(SKIN, .2), sh=SKIN_D)
    c.r(hx + 7, y0 - 2, 1, 1, SKIN_D if blink else '#1a1a1a')
    c.r(hx + 6, y0 + 1, 2, 1, dk(SKIN, .25))
    c.r(hx - 1, y0 - 6, 10, 3, HAIR)                                             # hairline/crown
    ty = hx - 3
    c.ell(ty, y0 - 8, 2, 2, HAIR)                                                # ponytail bun (up, tall)
    c.line(ty, y0 - 7, ty - 3, y0 + 3, HAIR_D, 3)                                # thick swinging ponytail
    c.line(ty - 1, y0 - 6, ty - 4, y0 + 2, HAIR, 1)
    c.r(hx - 1, y0 - 5, 10, 2, lt(HEADSET, .1))                                  # headset band, bright
    c.circ(hx + 8, y0 - 1, 2, HEADSET); c.circ(hx + 8, y0 - 1, 1, CYAN)
    c.line(hx + 8, y0 + 1, hx + 6, y0 + 3, HEADSET, 1)                           # mic boom
    return hx, y0 - 5


def clipboard_front(c, y0, lean):
    """Big, unmistakable clipboard clamped in the FRONT hand, held out ahead of the body where
    it reads clearly in silhouette (not tucked behind the torso)."""
    sx, sy = 19 + lean, y0 + 7
    bx, by = 24 + lean, y0 + 5
    c.line(sx, sy, bx - 2, by + 6, JACKET, 3)                                     # forearm to board
    c.box(bx, by, 8, 11, CLIP, out=None, hi=lt(CLIP, .25), sh=CLIP_D)             # board
    c.r(bx + 2, by - 2, 4, 2, CLIP_D)                                             # clip clasp top
    c.r(bx + 1, by + 3, 6, 1, dk(CLIP, .3)); c.r(bx + 1, by + 6, 6, 1, dk(CLIP, .3))  # ruled lines
    c.r(bx + 1, by + 8, 5, 2, STICKY)                                            # sticky note corner
    c.r(bx - 1, by - 1, 2, 2, SKIN)                                              # fingers over the edge
    return bx, by


def arm_back(c, y0, lean):
    """Trailing arm swings back, thin and long, empty (balances the glide)."""
    sx, sy = 15 + lean, y0 + 7
    c.line(sx, sy, sx - 7, y0 + 17, JACKET_D, 2)
    c.r(sx - 8, y0 + 16, 2, 2, SKIN)


def tempo(c, y0=4, phase=3, lean=5, blink=False):
    glide_legs(c, phase, y0)
    torso(c, y0, lean)
    arm_back(c, y0, lean)
    head(c, y0, lean, blink)
    clipboard_front(c, y0, lean)


def walk():
    out = []
    leans = (7, 5, 7, 5)
    for i, (phase, lean) in enumerate(zip((0, 1, 2, 1), leans)):
        c = C(W, H)
        tempo(c, 4, phase, lean, blink=False)
        c.outline_alpha(); out.append(c)
    return out


def clean():
    """Gliding in a wide figure-8 lean, sweeping a flat squeegee/wiper pad on a SHORT pole
    (not a stringy mop) from low-left to high-right and back — pad clearly changes position
    and angle between frames."""
    out = []
    # (pad centre x, pad centre y, pad tilt 0=flat/-1=angled) across the 4-frame sweep
    sweeps = ((30, 33, 0), (35, 27, 1), (37, 20, 0), (35, 27, -1))
    for i, (px, py, tilt) in enumerate(sweeps):
        c = C(W, H)
        y0 = 5
        lean = (2, 4, 6, 4)[i]
        glide_legs(c, (1, 0, 3, 2)[i], y0)
        torso(c, y0, lean)
        hx, hy = head(c, y0, lean, blink=(i == 2))
        bx, by = clipboard_front(c, y0, lean)
        # short pole from the back hand down to the pad (pole length stays short: ~6-8 cells)
        sx, sy = 15 + lean, y0 + 8
        px0, py0 = sx - 3, sy + 5
        c.line(sx, sy, px0, py0, POLE, 2); c.line(sx + 1, sy, px0 + 1, py0, POLE_D, 1)
        # flat pad: a short wide bar, angle via tilt, clearly not string/strand mop
        dx, dy = 4, 1 + tilt
        c.line(px - dx, py - dy, px + dx, py + dy, PAD, 3)
        c.line(px - dx, py - dy - 1, px + dx, py + dy - 1, PAD_L, 1)
        c.line(px - dx, py - dy + 2, px + dx, py + dy + 2, PAD_D, 1)
        c.line(px0, py0, px - dx, py - dy, POLE, 1)
        c.outline_alpha(); out.append(c)
    return out


def seat():
    c = C(W, H)
    x0 = 16
    c.r(x0, 33, 8, 2, STOOL_D)                                                   # base feet
    c.r(x0 + 3, 20, 2, 14, STOOL)                                                # tall pole
    c.r(x0 - 3, 24, 14, 2, STOOL_D)                                              # footrest ring
    c.box(x0 - 4, 14, 16, 6, STOOL, out=None, hi=STOOL_L, sh=STOOL_D)            # seat top
    c.r(x0 - 4, 14, 16, 1, STOOL_L)
    c.box(4, 8, 14, 12, BOARD, out=None, hi=BOARD_L, sh=BOARD_D)                 # small kanban board
    for i, (sx, sy, col) in enumerate(((6, 10, STICKY), (11, 10, CYAN), (6, 15, STICKY_D), (11, 15, CYAN))):
        c.r(sx, sy, 3, 3, col); c.r(sx, sy, 3, 1, lt(col, .25))
    c.outline_alpha(); return c


def sit():
    out = []
    for k in range(2):
        c = C(W, H)
        y0 = 8
        # perched hips-on-stool-top, skates dangling loose (not on floor)
        c.line(19, y0 + 12, 14, y0 + 22, LEG, 3); skate(c, 14, y0 + 22)
        c.line(21, y0 + 12, 25, y0 + 20, LEG, 3); skate(c, 25, y0 + 20, tilt=1)
        torso(c, y0, lean=2)
        if k == 0:
            arm_back(c, y0, 2)
            hx, hy = head(c, y0, 2, blink=False)
            bx, by = clipboard_front(c, y0, 2)
            c.line(19, y0 + 7, 24, y0 + 2, JACKET, 2)                            # arm up checking stopwatch
            c.r(23, y0, 4, 4, dk(SILVER, .1)); c.r(24, y0 + 1, 2, 2, CYAN)
        else:
            hx, hy = head(c, y0 + 1, 2, blink=True)
            bx, by = clipboard_front(c, y0 + 1, 2)
            c.r(bx + 6, by + 3, 2, 4, dk(SILVER, .2))                           # pen tapping on board
            c.r(bx + 6, by + 2, 2, 1, lt(SILVER, .3))
        c.outline_alpha(); out.append(c)
    return out
