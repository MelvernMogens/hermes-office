"""v5.6 build: cleaner sprites + themes.json blocks (cleaner, propFx, top-level cleanerRef).
Idempotent: re-run any time after editing cleaners/cl_*.py.  python3 themes/tools/gen_v56.py
NOTE: gen_themes.py rewrites themes.json from scratch -> re-run this afterwards."""
import os, sys, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)            # themes/
SP = os.path.join(ROOT, 'sprites')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'cleaners'))

K = 4                 # 40x36 cells * 4 = 160x144 png (2x HiDPI of 120x108 css)
CSS = [120, 108]      # 3 css px per cell (SIZE FIX 18:33)
THEMES = ['default', 'coder', 'research', 'designer', 'analyst', 'content', 'video', 'qa', 'ops', 'pm', 'growth']

# fx colour fallback per fx kind (META fxColor wins)
FXC = {'energon': '#b44dff', 'pixels': '#22e3ff', 'dust': '#d8c7a0', 'paint': '#ff5ea8', 'paper': '#f4efe2',
       'sparkle': '#fff3b0', 'bubbles': '#bfe9ff', 'mist': '#c9fbff', 'oil': '#3a3a2a', 'leaves': '#7ddc5a', 'sparks': '#ffb347'}


def _tall_frames(m, k, off):
    """Re-run the theme's frame function on a canvas with `off` extra rows ON TOP (everything drawn `off` rows lower)."""
    import px as _px
    class Tall(_px.C):
        def __init__(s, w, h): super().__init__(w, h + off)
        def p(s, x, y, col): super().p(x, int(y) + off, col)
    orig = m.C; m.C = Tall
    try:
        return getattr(m, k)()
    finally:
        m.C = orig


def headroom(m):
    """v5.7e: rows a theme draws ABOVE row 0 (ops Gus: hard hat at -6). px.C silently drops them -> head cut off in the
    office. Measured once per theme over every walk/clean/sit frame; 0 for themes that already fit."""
    probe = 16
    top = 0
    for k in ('walk', 'clean', 'sit'):
        for t in _tall_frames(m, k, probe):
            rows = [y - probe for y in range(t.h) if any(t.d[y])]
            if rows: top = min(top, rows[0])
    return -top


def export(tid, out_id):
    m = importlib.import_module('cl_' + tid)
    blk = {'name': m.META['name'], 'persona': m.META['persona'], 'size': CSS, 'anchor': 'bottom-center',
           'cell': 3, 'fx': m.META['fx'], 'fxColor': m.META.get('fxColor') or FXC.get(m.META['fx'], '#ffffff')}
    extra = headroom(m)                                  # taller canvas, bottom (feet) rows unchanged
    if extra:
        blk['size'] = [CSS[0], CSS[1] + extra * 3]
    for k in ('walk', 'clean', 'sit'):
        blk[k] = []
        for i, c in enumerate(_tall_frames(m, k, extra) if extra else getattr(m, k)()):
            name = 'cl_%s_%s%d.png' % (out_id, k, i)
            assert (c.w, c.h) == (40, 36 + extra)
            c.png(os.path.join(SP, name), K); blk[k].append('sprites/' + name)
    name = 'cl_%s_seat.png' % out_id
    m.seat().png(os.path.join(SP, name), K)
    blk['seat'] = {'sprite': 'sprites/' + name, 'size': CSS, 'anchor': 'bottom-center'}
    blk['fps'] = {'walk': 8, 'clean': 6, 'sit': 1.5}
    # locomotion hint for the engine (bob/glide); purely cosmetic
    blk['move'] = getattr(m, 'MOVE', None) or LOCO.get(tid, 'walk')
    return blk


LOCO = {'default': 'walk', 'coder': 'roll', 'research': 'shuffle', 'designer': 'waddle', 'analyst': 'roll',
        'content': 'walk', 'video': 'hover', 'qa': 'hover', 'ops': 'roll', 'pm': 'glide', 'growth': 'hop', 'ref': 'walk'}

# ---- prop animations per slot (coords relative to the slot box, css px). CityWindow = anim.json (panel frames).
# slot boxes: WaterCooler 40x124, CoffeeMachine 60x66, Plant 48x62, Printer 64x60. null slot -> engine ref anim.
PROPFX = {
 'default': {'WaterCooler': {'type': 'glow', 'color': '#b44dff', 'area': [6, 10, 28, 96], 'period': 3.2},
             'CoffeeMachine': {'type': 'float', 'area': [8, 4, 44, 30], 'amp': 2, 'period': 2.6},
             'Plant': {'type': 'sway', 'origin': [24, 62], 'deg': 2.5},
             'Printer': {'type': 'leds', 'color': '#b44dff', 'area': [8, 6, 48, 10], 'n': 3}},
 'coder': {'WaterCooler': {'type': 'leds', 'color': '#22e3ff', 'area': [6, 10, 28, 100], 'n': 8},
           'CoffeeMachine': {'type': 'flicker', 'color': '#ff4fd8', 'area': [4, 4, 52, 58]},
           'Plant': {'type': 'pulse', 'color': '#39ff88', 'area': [10, 4, 28, 40], 'period': 2.4},
           'Printer': {'type': 'leds', 'color': '#22e3ff', 'area': [10, 8, 44, 8], 'n': 2}},
 'research': {'WaterCooler': {'type': 'spin', 'area': [4, 8, 32, 40], 'period': 12},
              'CoffeeMachine': {'type': 'glint', 'color': '#fff3b0', 'at': [30, 14], 'period': 5},
              'Plant': {'type': 'sway', 'origin': [24, 62], 'deg': 3}, 'Printer': None},
 'designer': {'WaterCooler': {'type': 'sway', 'origin': [20, 124], 'deg': 1, 'area': [6, 10, 28, 60]},
              'CoffeeMachine': {'type': 'pulse', 'color': '#ff5ea8', 'area': [6, 6, 48, 22], 'period': 3},
              'Plant': {'type': 'sway', 'origin': [24, 62], 'deg': 3}, 'Printer': None},
 'content': {'WaterCooler': {'type': 'glint', 'color': '#f4efe2', 'at': [20, 30], 'period': 6},
             'CoffeeMachine': {'type': 'type', 'color': '#f4efe2', 'area': [14, 14, 32, 12], 'period': 0.18},
             'Plant': {'type': 'paper', 'area': [8, 0, 32, 20], 'period': 7}, 'Printer': None},
 'video': {'WaterCooler': {'type': 'pulse', 'color': '#fff6d6', 'area': [2, 4, 36, 60], 'period': 3.5},
           'CoffeeMachine': {'type': 'leds', 'color': '#ff3344', 'at': [40, 12], 'n': 1, 'period': 1.2},
           'Plant': {'type': 'spin', 'area': [6, 6, 36, 36], 'period': 9}, 'Printer': None},
 'analyst': {'WaterCooler': {'type': 'scan', 'color': '#4fd1ff', 'area': [6, 10, 28, 100], 'period': 3},
             'CoffeeMachine': {'type': 'leds', 'color': '#ffb020', 'area': [8, 8, 44, 40], 'n': 3},
             'Plant': None, 'Printer': None},
 'qa': {'WaterCooler': {'type': 'flicker', 'color': '#39ff88', 'alt': '#ff4d4d', 'area': [6, 14, 28, 24], 'period': 2.5},
        'CoffeeMachine': {'type': 'leds', 'color': '#39ff88', 'area': [6, 6, 48, 10], 'n': 3},
        'Plant': {'type': 'sway', 'origin': [24, 62], 'deg': 2}, 'Printer': None},
 'ops': {'WaterCooler': {'type': 'leds', 'color': '#39ff88', 'alt': '#ffb020', 'area': [6, 10, 28, 100], 'n': 10},
         'CoffeeMachine': {'type': 'spin', 'color': '#ff3344', 'at': [30, 6], 'period': 1.4, 'beam': True},
         'Plant': None, 'Printer': None},
 'pm': {'WaterCooler': {'type': 'flip', 'area': [2, 6, 36, 50], 'period': 11},
        'CoffeeMachine': {'type': 'flip', 'area': [6, 10, 48, 40], 'period': 17},
        'Plant': None, 'Printer': None},
 'growth': {'WaterCooler': {'type': 'count', 'color': '#39ff88', 'area': [6, 14, 28, 20], 'period': 1.5},
            'CoffeeMachine': {'type': 'glint', 'color': '#ffd84d', 'area': [4, 4, 52, 58], 'period': 4.5},
            'Plant': {'type': 'leds', 'color': '#ffd84d', 'area': [8, 6, 32, 30], 'n': 3, 'period': 2}, 'Printer': None},
}


def main():
    p = os.path.join(ROOT, 'themes.json')
    d = json.load(open(p))
    tot = 0
    for tid in THEMES:
        blk = export(tid, tid)
        d['themes'][tid]['cleaner'] = blk
        fx = dict(PROPFX[tid])
        props = d['themes'][tid]['props']
        for slot in list(fx):              # animate only slots that actually have a themed sprite
            if not props.get(slot): fx[slot] = None
        fx['CityWindow'] = {'type': 'anim', 'src': 'anim/anim.json'}
        d['themes'][tid]['propFx'] = fx
    d['cleanerRef'] = export('ref', 'ref')
    d['propFxRef'] = {'WaterCooler': {'type': 'bubbles'}, 'CoffeeMachine': {'type': 'steam'},
                      'Printer': {'type': 'paper'}, 'Plant': {'type': 'sway', 'deg': 2}}
    json.dump(d, open(p, 'w'), indent=1)
    for f in os.listdir(SP):
        if f.startswith('cl_'): tot += os.path.getsize(os.path.join(SP, f))
    print('cleaner pngs: %d KB' % (tot // 1024))


if __name__ == '__main__':
    main()
