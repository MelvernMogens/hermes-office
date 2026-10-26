"""Tiny pixel-art canvas + indexed PNG writer (stdlib only). Designer-drawn assets for hermes-office themes.
1 cell = 2 CSS px on screen; PNG exported at 4 px/cell (2x HiDPI) with nearest-neighbour scaling."""
import zlib, struct, math

OUT = '#0c0e12'

FONT = {
 'A':['.#.','#.#','###','#.#','#.#'],'B':['##.','#.#','##.','#.#','##.'],'C':['.##','#..','#..','#..','.##'],
 'D':['##.','#.#','#.#','#.#','##.'],'E':['###','#..','##.','#..','###'],'F':['###','#..','##.','#..','#..'],
 'G':['.##','#..','#.#','#.#','.##'],'H':['#.#','#.#','###','#.#','#.#'],'I':['###','.#.','.#.','.#.','###'],
 'J':['..#','..#','..#','#.#','.#.'],'K':['#.#','#.#','##.','#.#','#.#'],'L':['#..','#..','#..','#..','###'],
 'M':['#.#','###','###','#.#','#.#'],'N':['##.','#.#','#.#','#.#','#.#'],'O':['.#.','#.#','#.#','#.#','.#.'],
 'P':['##.','#.#','##.','#..','#..'],'Q':['.#.','#.#','#.#','##.','.##'],'R':['##.','#.#','##.','#.#','#.#'],
 'S':['.##','#..','.#.','..#','##.'],'T':['###','.#.','.#.','.#.','.#.'],'U':['#.#','#.#','#.#','#.#','###'],
 'V':['#.#','#.#','#.#','#.#','.#.'],'W':['#.#','#.#','###','###','#.#'],'X':['#.#','#.#','.#.','#.#','#.#'],
 'Y':['#.#','#.#','.#.','.#.','.#.'],'Z':['###','..#','.#.','#..','###'],
 '0':['###','#.#','#.#','#.#','###'],'1':['.#.','##.','.#.','.#.','###'],'2':['##.','..#','.#.','#..','###'],
 '3':['##.','..#','.#.','..#','##.'],'4':['#.#','#.#','###','..#','..#'],'5':['###','#..','##.','..#','##.'],
 '6':['.##','#..','###','#.#','###'],'7':['###','..#','.#.','.#.','.#.'],'8':['###','#.#','###','#.#','###'],
 '9':['###','#.#','###','..#','##.'],'%':['#.#','..#','.#.','#..','#.#'],'+':['...','.#.','###','.#.','...'],
 '.':['...','...','...','...','.#.'],'$':['.##','##.','.#.','.##','##.'],'>':['#..','.#.','..#','.#.','#..'],
 '<':['..#','.#.','#..','.#.','..#'],'/':['..#','..#','.#.','#..','#..'],'_':['...','...','...','...','###'],
 '!':['.#.','.#.','.#.','...','.#.'],':':['...','.#.','...','.#.','...'],'-':['...','...','###','...','...'],
 ' ':['...','...','...','...','...'],
}

def hx(c):
    c = c.lstrip('#')[:8]
    if len(c) == 3: c = ''.join(ch*2 for ch in c)
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def tohex(t): return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in t)
def mix(a, b, t): A, B = hx(a), hx(b); return tohex(tuple(A[i] + (B[i]-A[i])*t for i in range(3)))
def dk(c, t=.3): return mix(c, '#000000', t)
def lt(c, t=.3): return mix(c, '#ffffff', t)

class C:
    def __init__(s, w, h): s.w, s.h = w, h; s.d = [[None]*w for _ in range(h)]
    def p(s, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < s.w and 0 <= y < s.h: s.d[y][x] = c
    def r(s, x, y, w, h, c):
        for yy in range(int(y), int(y+h)):
            for xx in range(int(x), int(x+w)): s.p(xx, yy, c)
    def ol(s, x, y, w, h, c):
        s.r(x, y, w, 1, c); s.r(x, y+h-1, w, 1, c); s.r(x, y, 1, h, c); s.r(x+w-1, y, 1, h, c)
    def box(s, x, y, w, h, f, out=OUT, hi=None, sh=None):
        """outlined, bevelled block (16-bit look): light top/left, dark bottom/right"""
        s.r(x, y, w, h, f)
        s.r(x+1, y+1, w-2, 1, hi or lt(f, .22)); s.r(x+1, y+1, 1, h-2, hi or lt(f, .22))
        s.r(x+1, y+h-2, w-2, 1, sh or dk(f, .3)); s.r(x+w-2, y+1, 1, h-2, sh or dk(f, .3))
        if out: s.ol(x, y, w, h, out)
    def frame(s, x, y, w, h, fc, bw=3, out=OUT):
        """bevelled picture frame band of width bw around (x,y,w,h) outer box"""
        s.r(x, y, w, bw, lt(fc, .15)); s.r(x, y, bw, h, lt(fc, .15))
        s.r(x, y+h-bw, w, bw, dk(fc, .25)); s.r(x+w-bw, y, bw, h, dk(fc, .25))
        s.r(x+1, y+1, w-2, 1, lt(fc, .35))
        s.ol(x, y, w, h, out); s.ol(x+bw-1, y+bw-1, w-2*bw+2, h-2*bw+2, dk(fc, .55))
    def circ(s, cx, cy, rad, c):
        for y in range(int(cy-rad-1), int(cy+rad+2)):
            for x in range(int(cx-rad-1), int(cx+rad+2)):
                if (x-cx)**2 + (y-cy)**2 <= rad*rad + rad*.8: s.p(x, y, c)
    def ell(s, cx, cy, rx, ry, c):
        for y in range(int(cy-ry-1), int(cy+ry+2)):
            for x in range(int(cx-rx-1), int(cx+rx+2)):
                if ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1.0: s.p(x, y, c)
    def ring(s, cx, cy, rad, c, th=1):
        for y in range(int(cy-rad-1), int(cy+rad+2)):
            for x in range(int(cx-rad-1), int(cx+rad+2)):
                d = math.hypot(x-cx, y-cy)
                if rad-th < d <= rad+.35: s.p(x, y, c)
    def line(s, x0, y0, x1, y1, c, th=1):
        n = int(max(abs(x1-x0), abs(y1-y0))) or 1
        for i in range(n+1):
            x = x0 + (x1-x0)*i/n; y = y0 + (y1-y0)*i/n
            s.r(round(x), round(y), th, th, c)
    def txt(s, x, y, t, c, sc=1):
        for ch in t.upper():
            g = FONT.get(ch, FONT[' '])
            for gy, row in enumerate(g):
                for gx, v in enumerate(row):
                    if v == '#': s.r(x+gx*sc, y+gy*sc, sc, sc, c)
            x += 4*sc
    def tw(s, t, sc=1): return len(t)*4*sc - sc
    def ctxt(s, cx, y, t, c, sc=1): s.txt(cx - s.tw(t, sc)//2, y, t, c, sc)
    def outline_alpha(s, c=OUT):
        """add 1-cell outline around every opaque region (sprite silhouette)"""
        src = [row[:] for row in s.d]
        for y in range(s.h):
            for x in range(s.w):
                if src[y][x] is None:
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        xx, yy = x+dx, y+dy
                        if 0 <= xx < s.w and 0 <= yy < s.h and src[yy][xx] is not None and src[yy][xx] != c:
                            s.d[y][x] = c; break
    def png(s, path, k=4):
        cols = sorted({c for row in s.d for c in row if c})
        assert len(cols) < 256, (path, len(cols))
        idx = {c: i+1 for i, c in enumerate(cols)}
        pal = b'\x00\x00\x00' + b''.join(bytes(hx(c)) for c in cols)
        trns = b'\x00' + bytes(int(c[7:9], 16) if len(c) == 9 else 255 for c in cols)
        raw = bytearray()
        for row in s.d:
            line = bytes(idx.get(c, 0) for c in row for _ in range(k))
            for _ in range(k): raw += b'\x00' + line
        def ch(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t+d) & 0xffffffff)
        W, H = s.w*k, s.h*k
        data = b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 3, 0, 0, 0)) \
            + ch(b'PLTE', pal) + ch(b'tRNS', trns) + ch(b'IDAT', zlib.compress(bytes(raw), 9)) + ch(b'IEND', b'')
        open(path, 'wb').write(data)
        return W, H
