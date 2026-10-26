"""Self-check sheet for one cleaner: python3 sheet.py <id>  -> _sheets/<id>.png (+ asserts contract).
Layout (1 row): walk frames | clean frames | sit frames | seat alone | seat+sit composite | ghost agent capsule."""
import os, sys, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from px import C

FX = {'sparkle', 'dust', 'bubbles', 'sparks', 'energon', 'paint', 'paper', 'leaves', 'mist', 'pixels', 'oil'}


def load(tid):
    m = importlib.import_module('cl_' + tid)
    W, H = 40, 36
    fr = {'walk': m.walk(), 'clean': m.clean(), 'sit': m.sit()}
    seat = m.seat()
    lim = {'walk': (2, 4), 'clean': (2, 4), 'sit': (1, 2)}
    for k, v in fr.items():
        assert lim[k][0] <= len(v) <= lim[k][1], (tid, k, len(v))
        for c in v: assert (c.w, c.h) == (W, H), (tid, k, c.w, c.h)
    assert (seat.w, seat.h) == (W, H), (tid, 'seat')
    meta = m.META
    for k in ('name', 'persona', 'fx'): assert meta.get(k), (tid, k)
    assert meta['fx'] in FX, (tid, meta['fx'])
    for k in ('walk', 'clean'):
        for i, c in enumerate(fr[k]):
            assert any(c.d[35][x] for x in range(W)) or any(c.d[34][x] for x in range(W)), (tid, k, i, 'feet not on bottom row')
    return m, fr, seat


def floor_of(tid):
    try:
        th = json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), 'themes.json')))['themes']
        return th[tid]['floor'] if tid in th else '#2a2a2a'
    except Exception:
        return '#2a2a2a'


def blit(dst, src, ox, oy):
    for y in range(src.h):
        for x in range(src.w):
            v = src.d[y][x]
            if v: dst.p(ox + x, oy + y, v)


def sheet(tid):
    m, fr, seat = load(tid)
    cells = fr['walk'] + fr['clean'] + fr['sit'] + [seat]
    n = len(cells) + 2
    S = C(n * 42 + 2, 40)
    S.r(0, 0, S.w, S.h, floor_of(tid))
    for i, c in enumerate(cells):
        S.ol(1 + i * 42, 1, 42, 38, '#3a3f4a'); blit(S, c, 2 + i * 42, 2)
    comp = C(40, 36); blit(comp, seat, 0, 0); blit(comp, fr['sit'][0], 0, 0)
    i = len(cells); S.ol(1 + i * 42, 1, 42, 38, '#ffd000'); blit(S, comp, 2 + i * 42, 2)
    # ghost agent capsule 24x40 cells scaled to our 2css/cell = 48x80 css => 24x40 cells (does not fit 36 rows: clip top)
    # SIZE FIX 18:33: 3 css/cell. Agent capsule 48x80 css = 16x27 cells + legs => ~33 cells tall total.
    i += 1; x0 = 2 + i * 42 + 12
    CW, CH, top = 16, 27, 2 + 36 - 33
    for y in range(CH):
        for x in range(CW):
            dx = min(x, CW - 1 - x); dy = min(y, CH - 1 - y)
            r = 7
            if dx < r and dy < r and (r - dx) ** 2 + (r - dy) ** 2 > r * r: continue
            edge = x in (0, CW - 1) or y in (0, CH - 1) or (dx < r and dy < r and (r - dx + 1) ** 2 + (r - dy + 1) ** 2 > r * r)
            S.p(x0 + x, top + y, '#e5e7eb' if edge else '#3b82f6')
    for y in range(top + CH, 2 + 36):
        for x in (4, 5, 10, 11): S.p(x0 + x, y, '#e5e7eb')
    os.makedirs(os.path.join(HERE, '_sheets'), exist_ok=True)
    p = os.path.join(HERE, '_sheets', tid + '.png'); S.png(p, 5)
    print('ok', tid, {k: len(v) for k, v in fr.items()}, m.META['fx'], '->', p)


if __name__ == '__main__':
    for t in sys.argv[1:]: sheet(t)
