"""python3 silhouettes.py [ids...] -> _sheets/_silhouettes.png
Row 1: walk0 of every cleaner as flat black silhouette on white (shape check).
Row 2: walk0 in colour on dark floor. Row 3: clean1. Row 4: seat+sit composite.
Labels are drawn as tiny index ticks; order printed to stdout."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from px import C, hx
import zlib, struct


def png_rgb(s, path, k=4):
    raw = bytearray()
    for row in s.d:
        line = b''.join(bytes(hx(c)) if c else b'\x00\x00\x00' for c in row for _ in range(k))
        for _ in range(k): raw += b'\x00' + line
    def ch(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', s.w * k, s.h * k, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(bytes(raw), 9)) + ch(b'IEND', b'')
    open(path, 'wb').write(data)

IDS = ['default', 'coder', 'research', 'designer', 'analyst', 'content', 'video', 'qa', 'ops', 'pm', 'growth', 'ref']


def blit(dst, src, ox, oy, col=None):
    for y in range(src.h):
        for x in range(src.w):
            v = src.d[y][x]
            if v: dst.p(ox + x, oy + y, col or v)


def main(ids):
    mods = []
    for t in ids:
        try:
            mods.append((t, importlib.import_module('cl_' + t)))
        except Exception as e:
            print('FAIL', t, e); mods.append((t, None))
    n = len(mods)
    S = C(n * 44 + 4, 4 * 40 + 4)
    S.r(0, 0, S.w, 42, '#f2f2f2')
    S.r(0, 42, S.w, S.h - 42, '#22252b')
    for i, (t, m) in enumerate(mods):
        if not m: continue
        ox = 4 + i * 44
        w = m.walk(); cl = m.clean(); st = m.sit(); se = m.seat()
        blit(S, w[0], ox, 2, '#000000')
        blit(S, w[0], ox, 44)
        blit(S, cl[min(1, len(cl) - 1)], ox, 84)
        comp = C(40, 36); blit(comp, se, 0, 0); blit(comp, st[0], 0, 0)
        blit(S, comp, ox, 124)
        print(i, t, m.META.get('name'))
    p = os.path.join(HERE, '_sheets', '_silhouettes.png'); png_rgb(S, p, 4); print('->', p)


if __name__ == '__main__':
    main(sys.argv[1:] or IDS)
