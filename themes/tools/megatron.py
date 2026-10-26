"""MEGATRON (Decepticon-style) wall panel: metal-planet hologram. Original art, no Hasbro insignia."""
import math
from px import C, OUT, dk, lt, mix
from props2 import GM, GM2, PUR, RED, ENG, emblem

def cyber_holo():
    W, H = 100, 80; c = C(W, H)
    c.box(0, 0, W, H, GM2); c.r(1, 1, W-2, 1, PUR); c.r(1, H-2, W-2, 1, dk(PUR, .3))
    for x in (2, 96): c.r(x, 4, 2, 72, GM)
    c.r(4, 4, 92, 72, '#07060c')
    for gy in range(6, 76, 6): c.r(4, gy, 92, 1, '#0e0c18')                # scanlines
    cx, cy, R = 50, 42, 24
    for y in range(cy-R, cy+R+1):                                           # metal planet
        for x in range(cx-R, cx+R+1):
            d = math.hypot(x-cx, y-cy)
            if d <= R:
                shade = 1 - (x-cx+y-cy+R)/(3*R)
                base = mix('#2e3040', '#8a8fa6', max(0, min(1, shade)))
                if ((x//4) + (y//3)) % 5 == 0: base = dk(base, .35)          # plating grid
                if (x*3 + y*7) % 29 == 0: base = ENG                          # city lights
                c.p(x, y, base)
    c.ring(cx, cy, R, PUR, 1)
    for a in range(0, 360, 2):                                              # orbital ring
        r = math.radians(a); x = cx + math.cos(r)*36; y = cy + math.sin(r)*8 - math.cos(r)*3
        if not (math.sin(r) < 0 and math.hypot(x-cx, y-cy) < R): c.p(x, y, lt(PUR, .3) if a % 20 else '#ffffff')
    for (x, y) in [(18, 20), (82, 64), (86, 18), (14, 62)]: c.r(x-1, y-1, 3, 3, RED); c.p(x, y, '#ffc0c8')
    c.r(4, 4, 92, 7, '#120f1c'); emblem(c, 5, 4, PUR, RED) if False else None
    c.txt(6, 5, 'CYBER OPS', lt(PUR, .35)); c.txt(70, 5, 'LIVE', RED); c.r(87, 6, 3, 3, RED)
    c.r(4, 70, 92, 6, '#120f1c')
    for i, wv in enumerate([12, 20, 8, 26, 10]): c.r(6+i*18, 72, wv, 2, ENG if i % 2 else PUR)
    emblem(c, 83, 57, '#4a4d5c', RED)
    return c

ALL3 = {'cyber_holo': cyber_holo}
