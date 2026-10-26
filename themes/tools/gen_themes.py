"""Build the hermes-office v5.2 theme pack: sprites/*.png + themes.json.
Run: cd themes/tools && python3 gen_themes.py"""
import os, re, json, base64, zlib, struct
import wall_wide, props
from px import mix, dk, lt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SP = os.path.join(ROOT, 'sprites')
os.makedirs(SP, exist_ok=True)

def emit(group, k=4):
    out = {}
    for name, fn in group.items():
        c = fn(); W, H = c.png(os.path.join(SP, name + '.png'), k)
        out[name] = (W, H)
    return out

import props2, megatron
for f in os.listdir(SP):
    if f.endswith('.png'): os.remove(os.path.join(SP, f))   # clean rebuild, no stale sprites
WALL = {**wall_wide.ALL, **megatron.ALL3}; WALL.pop('hq_map')
TALL = dict(props2.TALL2)
UNIT = {**{k: v for k, v in props.UNIT.items() if k not in ('radar_console', 'paint_stool')}, **props2.UNIT2}
POT = {**props.POT, **props2.POT2}
DESKS = {**{k: v for k, v in props.DESK.items() if k not in ('d_flag', 'd_medal')}, **props2.DESK2}
sizes = {}
for g in (WALL, TALL, UNIT, POT, props.MISC, props2.RUG2, DESKS): sizes.update(emit(g))

# ---- floor tiles: palette swap of claude-office floor-tile (MIT). Tile is indexed PNG w/ 3-colour PLTE.
src = open(os.path.join(ROOT, '..', 'test', 'sprites.gen.js')).read()
tile = base64.b64decode(re.search(r"floorTile: 'data:image/png;base64,([^']+)'", src).group(1))
def chunks(b):
    i = 8
    while i < len(b):
        n = struct.unpack('>I', b[i:i+4])[0]; t = b[i+4:i+8]; yield t, b[i+8:i+8+n]; i += 12 + n
def ch(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t+d) & 0xffffffff)
ref_pal = [c for t, c in chunks(tile) if t == b'PLTE'][0]
assert len(ref_pal) == 9, 'expected 3-colour ref tile palette'
def tile_png(cols):
    pal = b''.join(bytes(int(c.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for c in cols)
    return b'\x89PNG\r\n\x1a\n' + b''.join(ch(t, pal if t == b'PLTE' else d) for t, d in chunks(tile))

# ---- slot geometry (world px, from claude-office positions.ts / plugin v5 sizes). Props keep the ref slot centre.
SLOTS = {
    'CityWindow':    {'x': 319, 'y': 30, 'w': 200, 'h': 160, 'anchor': 'topleft'},
    'WaterCooler':   {'cx': 1010, 'cy': 200, 'w': 40, 'h': 124, 'note': 'bottom aligned to ref cooler bottom (y=260)'},
    'CoffeeMachine': {'cx': 1081, 'cy': 191, 'w': 60, 'h': 66},
    'Plant':         {'cx': 118, 'cy': 970, 'w': 48, 'h': 62},
    'BossRug':       {'cx': 640, 'cy': 940, 'w': 372, 'h': 180, 'note': 'replaces ref boss rug (373x179) under boss desk'},
    'Printer':       {'cx': 50, 'cy': 960 - 47.8 + 30, 'w': 64, 'h': 60, 'note': 'replaces printer only; mini desk stays'},
}
KIND = {**{k: 'CityWindow' for k in WALL}, **{k: 'WaterCooler' for k in TALL},
        **{k: 'CoffeeMachine' for k in UNIT}, **{k: 'Plant' for k in POT}, 'printer_3d': 'Printer', 'hex_platform': 'BossRug'}

# desk accessory placement = same anchor the ref uses for desk items (x+50, y+40 from desk origin), 24x24 css
DESK_ITEM = {'dx': 50, 'dy': 38, 'w': 24, 'h': 24}

T = {}
def theme(id_, label, wall, trim, floor, _tile_unused, accent, props_, desk, slots_desk, chrome, rug):
    # floor tile = ref greys (#252525/#343434/#3e3e3e, same contrast as the accepted v5 floor) tinted 10% toward the accent
    tile_cols = [mix(g, accent, .10) for g in ('#252525', '#343434', '#3e3e3e')]
    tile_cols = [mix(c, floor, .25) for c in tile_cols]
    T[id_] = {
        'label': label, 'wall': wall, 'wallTrim': trim, 'floor': floor, 'floorTile': 'sprites/floor_%s.png' % id_,
        'floorTint': tile_cols, 'accent': accent,
        'props': {k: ('sprites/%s.png' % v if v else None) for k, v in props_.items()},
        'deskItems': [{'file': 'sprites/%s.png' % f, 'desks': d} for f, d in zip(desk, slots_desk)],
        'chrome': chrome, 'rugFilter': rug,
    }
    open(os.path.join(SP, 'floor_%s.png' % id_), 'wb').write(tile_png(tile_cols))

def P(city, tall, unit, plant=None, printer=None, eom=None, clock=None, wb=None, safety=None, rug=None):
    return {'CityWindow': city, 'WaterCooler': tall, 'CoffeeMachine': unit, 'Plant': plant, 'Printer': printer, 'BossRug': rug,
            'EmployeeOfMonth': eom, 'WallClock': clock, 'Whiteboard': wb, 'SafetySign': safety}

def chrome(frame, board_head, sign_bg, sign_border, sign_head, sign_text, clock_rim, trim_glow):
    return {'eomFrame': frame, 'whiteboardHeader': board_head, 'safetySign': {'bg': sign_bg, 'border': sign_border, 'header': sign_head, 'text': sign_text},
            'clockRim': clock_rim, 'trimGlow': trim_glow}

theme('default', 'WARLORD / MECH BASE', '#1f1f27', '#2c2340', '#1a1a20', None, '#a855f7',
      P('cyber_holo', 'energon_pylon', 'energon_cubes', 'mech_plant', rug='hex_platform'), ['d_energon', 'd_emblem'], [[0, 5], [2, 7]],
      chrome('#5a5d6c', '#2a1f40', '#1e1a2c', '#a855f7', '#ff2d3d', '#22e3ff', '#2a2c35', '#a855f7'), 'none')
theme('coder', 'CODER LAB', '#1d2527', '#16312c', '#191f21', ['#151b1d', '#1e2729', '#253033'], '#39ff9c',
      P('coder_terminal', 'server_rack', 'neon_fridge', 'cactus_led', 'printer_3d'), ['d_can', 'd_rgbfan'], [[1, 4], [3, 6]],
      chrome('#2a8a6a', '#0f2a24', '#0b1a17', '#051210', '#11705a', '#39ff9c', '#17332d', '#2ee6e6'), 'hue-rotate(150deg) saturate(.7) brightness(.8)')
theme('designer', 'DESIGN STUDIO', '#2a2530', '#3a2c3c', '#222027', ['#1e1c22', '#29262e', '#312d37'], '#f5a8c8',
      P('designer_swatches', 'easel', 'paint_cart', 'flower_pastel'), ['d_palette', 'd_tablet'], [[0, 6], [2, 5]],
      chrome('#d9a3c3', '#3a2c48', '#2e2438', '#1e1726', '#b07ab0', '#ffd6f0', '#3a2c48', '#bdb2ff'), 'hue-rotate(290deg) saturate(.6)')
theme('content', 'WRITER ROOM', '#2e2721', '#4a3522', '#241f1b', ['#1f1a16', '#2a231d', '#332a22'], '#e0a060',
      P('content_storyboard', 'tall_bookcase', 'typewriter_table', 'paper_bin'), ['d_notebook', 'd_bookstack'], [[1, 7], [3, 4]],
      chrome('#8b5a2b', '#4a3522', '#3a2a1a', '#22180e', '#a8452f', '#f4d8a8', '#4a3522', '#e0a060'), 'hue-rotate(20deg) saturate(.8)')
theme('video', 'PRODUCTION STUDIO', '#251f30', '#3a2452', '#1f1b27', ['#1a1722', '#24202e', '#2c2738'], '#b36bff',
      P('video_timeline', 'softbox', 'camera_tripod', 'film_reels'), ['d_clapper', 'd_minicam'], [[0, 5], [2, 7]],
      chrome('#7a4ab0', '#2a1a40', '#22163a', '#140c24', '#8f4de0', '#e0c8ff', '#2a1a40', '#c77dff'), 'hue-rotate(250deg) saturate(.8)')
theme('analyst', 'DATA ROOM', '#1f2634', '#1c3150', '#1b2029', ['#171b23', '#20262f', '#272e39'], '#4da3ff',
      P('analyst_dashboard', 'data_totem', 'report_cabinet'), ['d_calc', 'd_minipie'], [[1, 6], [3, 4]],
      chrome('#3a6aa8', '#12243c', '#10203a', '#081224', '#2e6fd8', '#9fd0ff', '#12243c', '#4da3ff'), 'hue-rotate(210deg) saturate(.7)')
theme('research', 'LIBRARY', '#1f2a22', '#3a2c1c', '#1c211d', ['#171c18', '#202721', '#272f28'], '#c9a55a',
      P('research_library', 'floor_globe', 'microscope_table', 'fern_big'), ['d_openbook', 'd_magnifier'], [[0, 6], [2, 5]],
      chrome('#6b4a30', '#1f3a28', '#1a3322', '#0c1f12', '#2f5d3a', '#e8d9a8', '#3a2c1c', '#c9a55a'), 'hue-rotate(110deg) saturate(.55) brightness(.85)')
theme('qa', 'QA LAB', '#26262a', '#2e2a2a', '#1f1f22', ['#1a1a1d', '#232326', '#2b2b2f'], '#e5484d',
      P('qa_bugboard', 'test_rig', 'test_bench', 'bonsai_check'), ['d_bugjar', 'd_clipboard'], [[1, 4], [3, 6]],
      chrome('#6a6f76', '#2a1c1c', '#1a3a22', '#0d2414', '#e5484d', '#3ecf6e', '#2a2a2e', '#e5484d'), 'hue-rotate(0deg) saturate(.7)')
theme('ops', 'NOC', '#28231f', '#4a2e14', '#211e1b', ['#1c1916', '#26221e', '#2e2924'], '#ff8a1f',
      P('ops_noc', 'noc_rack', 'alarm_console', 'extinguisher'), ['d_walkie', 'd_beacon'], [[0, 7], [2, 5]],
      chrome('#8a5a2a', '#3a2410', '#2a1c10', '#1a1008', '#ff8a1f', '#ffd0a0', '#3a2410', '#ff8a1f'), 'hue-rotate(30deg) saturate(.9)')
theme('pm', 'WAR ROOM', '#1c2929', '#163a37', '#1a2222', ['#161d1d', '#1f2828', '#263030'], '#2ec4b6',
      P('pm_kanban', 'flip_chart', 'wall_calendar'), ['d_sticky', 'd_hourglass'], [[1, 6], [3, 4]],
      chrome('#2a8a82', '#10302e', '#0f2a28', '#061a18', '#1a8a80', '#bff5ef', '#10302e', '#2ec4b6'), 'hue-rotate(170deg) saturate(.6)')
theme('growth', 'GROWTH DESK', '#232820', '#34401c', '#1e221b', ['#191d16', '#22271e', '#2a3025'], '#a3e635',
      P('growth_chart', 'growth_kiosk', 'trophy_shelf', 'money_sprout'), ['d_megaphone', 'd_rocket'], [[0, 5], [2, 7]],
      chrome('#6a8a2a', '#243016', '#1f2a14', '#10180a', '#5f8a1c', '#e9ffb8', '#243016', '#a3e635'), 'hue-rotate(90deg) saturate(.7) brightness(.9)')

for t in T.values():
    for slot, f in t['props'].items():
        if f:
            n = os.path.basename(f)[:-4]; assert KIND[n] == slot, (n, slot)

# ---------------- rev3: furniture / architecture / capsules per theme ----------------
import furniture as F
WB = {  # dark whiteboard panels (was bright white) : bg, border, text, dim text, header
 'default': ('#15161c', '#3b3e4a', '#e9d5ff', '#8a8fa6'), 'coder': ('#0a1210', '#1f3a30', '#b8ffd8', '#5b8a74'),
 'designer': ('#1f1a26', '#5a4a68', '#fbe3f0', '#9a8aa8'), 'content': ('#1f1812', '#6b4423', '#f4e3c3', '#9a8466'),
 'video': ('#141019', '#3a2452', '#ead8ff', '#8a78a0'), 'analyst': ('#0b1220', '#1c3150', '#d6e8ff', '#6f8fb8'),
 'research': ('#141c15', '#3a2c1c', '#ecdfb8', '#8a8a6a'), 'qa': ('#161617', '#3a3f45', '#f2f2f2', '#8a9098'),
 'ops': ('#161310', '#4a2e14', '#ffe3c8', '#9a8470'), 'pm': ('#0e1818', '#1f4a47', '#d6fffa', '#6a9a96'),
 'growth': ('#12160e', '#34401c', '#efffd0', '#8a9a6a'),
}
CLOCK = {'default': ('#2a2c35', '#d8b4fe', '#ff2d3d')}
for tid, t in T.items():
    ms = {'desk': F.desk, 'chair': F.chair, 'monitor': F.monitor, 'keyboard': F.keyboard,
          'elevatorFrame': F.elevator_frame, 'elevatorDoor': F.elevator_door, 'wallTexture': F.wall_tile, 'wallTrimTexture': F.trim_tile}
    for key, fn in ms.items():
        name = '%s_%s' % (key, tid); fn(tid).png(os.path.join(SP, name + '.png')); t[key] = 'sprites/%s.png' % name
    # textured floor tile replaces the palette-swap (50 cells x 2 css px = 100px tile, like ref)
    F.floor_tile(tid).png(os.path.join(SP, 'floor_%s.png' % tid), 2); t['floorTile'] = 'sprites/floor_%s.png' % tid
    t.pop('floorTint', None)
    F.acc(tid).png(os.path.join(SP, 'acc_%s.png' % tid)); F.acc(tid, True).png(os.path.join(SP, 'accboss_%s.png' % tid))
    pal, stroke, boss, keep_ref = F.CAPS[tid]
    t['agentPalette'] = pal; t['agentStroke'] = stroke; t['bossBody'] = boss
    t['agentAccessory'] = {'file': 'sprites/acc_%s.png' % tid, 'w': 56, 'h': 48, **F.ACC_OFF, 'replacesRefShades': True}
    t['bossAccessory'] = {'file': 'sprites/accboss_%s.png' % tid, 'w': 56, 'h': 48, **F.ACC_OFF, 'replacesRefShades': True}
    bg, border, txt, dim = WB[tid]
    face, hand, sec = CLOCK.get(tid, (dk(t['wall'], .2), lt(t['accent'], .45), t['accent']))
    t['chrome'].update({'whiteboardBg': bg, 'whiteboardBorder': border, 'whiteboardText': txt, 'whiteboardDim': dim,
                        'clockFace': face, 'clockHand': hand, 'clockSecond': sec, 'eomCard': dk(t['wall'], .15)})
F.robot_portrait().png(os.path.join(SP, 'eom_megatron.png')); T['default']['chrome']['eomPortrait'] = 'sprites/eom_megatron.png'
import portraits
for _tid, _fn in portraits.ALL.items():
    _fn().png(os.path.join(SP, 'eom_%s.png' % _tid)); T[_tid]['chrome']['eomPortrait'] = 'sprites/eom_%s.png' % _tid
F.pcb_mat().png(os.path.join(SP, 'pcb_mat.png')); T['coder']['props']['BossRug'] = 'sprites/pcb_mat.png'
F.fabricator().png(os.path.join(SP, 'fabricator.png')); T['default']['props']['Printer'] = 'sprites/fabricator.png'

out = {
    'version': '5.2', 'world': {'w': 1280, 'h': 1024, 'wallH': 250, 'trim': {'y': 240, 'h': 10}},
    'notes': [
        'props[slot] = file -> draw this sprite in the ref slot INSTEAD of the ref prop; null = keep ref prop.',
        'EmployeeOfMonth / WallClock / Whiteboard / SafetySign stay functional (live data) - only recoloured via chrome.*',
        'deskItems[i].desks = desk indices (0..7, row-major) whose ref DESK_ITEM is replaced by this accessory (drawn at desk.x+dx, desk.y+dy).',
        'floorTile = themed 100x100 tile (textured, own art), use exactly like SPRITES.floorTile in FLOOR_PATTERN (keep the rotate/odd-tile darkening).',
        'rugFilter = CSS filter applied to the ref boss rug when props.BossRug is null.',
        'trimGlow = 2px line on top of the wall trim (y=240) to carry the accent; everything else stays dark.',
        'All PNGs are pixel art at 2x; render with image-rendering: pixelated at the css sizes below.',
        'REV3 architecture: wallTexture = 128x240 tile repeated along x over y 0..240; wallTrimTexture = 64x10 tile repeated along x at y 240..250.',
        'REV3 sprite swaps (SAME css size + anchor as plugin v5 ref): desk 140.5x73.9, chair 63.3x100.8, monitor 63x51.7, keyboard 52.6x14, elevatorFrame 154.4x144.3, elevatorDoor 50.8x123.5 (both doors, scaleX anim). Boss desk/monitor/keyboard/chair use the same theme sprites. Elevator indicator light stays plugin-drawn.',
        'REV3 capsule: body fill = agentPalette[i % n] (boss = bossBody), stroke = agentStroke (width 4, radius 22, 48x80 unchanged). agentAccessory/bossAccessory REPLACE the ref sunglasses: draw 56x48 at capsule-centre + (x,y). Agent capsule centre = pos + (0,-16); boss capsule centre = (640, 906). The accessory replaces the ref sunglasses always and the ref headset while seated.',
        'REV3 chrome: whiteboardBg/Border/Text/Dim (dark board, light text), clockFace/clockHand/clockSecond, eomCard (card bg), eomPortrait (optional image replacing the EoM photo).',
    ],
    'sizes': {'desk': [140.5, 73.9], 'chair': [63.3, 100.8], 'monitor': [63, 51.7], 'keyboard': [52.6, 14], 'elevatorFrame': [154.4, 144.3],
              'elevatorDoor': [50.8, 123.5], 'floorTile': [100, 100], 'wallTexture': [128, 240], 'wallTrimTexture': [64, 10], 'accessory': [56, 48]},
    'slots': SLOTS, 'deskItem': DESK_ITEM, 'themes': T,
}
json.dump(out, open(os.path.join(ROOT, 'themes.json'), 'w'), indent=1)
print('sprites', len(sizes) + len(T), 'themes', len(T))
