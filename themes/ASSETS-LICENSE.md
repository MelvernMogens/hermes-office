# Theme assets: origin and license

**No third-party art was downloaded for the floor themes.** Every theme sprite was drawn in code using Python stdlib pixel grids exported to indexed PNG. The generators are `themes/tools/*.py` and `themes/tools/cleaners/*.py`. All of it is covered by this repo's MIT license.

| Output (`themes/sprites/`) | Generator |
|---|---|
| Wall panels: `hq_map`, `coder_terminal`, `designer_swatches`, `content_storyboard`, `video_timeline`, `analyst_dashboard`, `research_library`, `qa_bugboard`, `ops_noc`, `pm_kanban`, `growth_chart` | `tools/wall_wide.py` |
| Tall props, unit props, pot/misc props, desk accessories (`d_*`) | `tools/props.py`, `tools/props2.py` |
| Per-theme furniture: `desk_*`, `chair_*`, `monitor_*`, `keyboard_*`, `elevatorFrame_*`, `elevatorDoor_*`, `wallTexture_*`, `wallTrimTexture_*`, `acc_*`, `accboss_*`, `floor_*` | `tools/furniture.py` |
| Employee-of-the-Month portraits | `tools/portraits.py`, `tools/megatron.py` |
| Cleaner NPCs: `cl_<theme>_{walk0-3,clean0-3,sit0-1,seat}` | `tools/cleaners/cl_<theme>.py` (on top of `tools/px.py`) |
| 3×5 pixel font | `tools/px.py` |

**Megatron theme.** It is Decepticon-flavoured, but its emblem is an original angular mask (`tools/props2.py`, `EMBLEM`). It is not the official Hasbro / Transformers insignia. No logos, trademarks or licensed characters are reproduced.

**Exception: the claude-office reference sprites.** The base office sprites from [claude-office](https://github.com/paulrobello/claude-office) are not part of this theme pack. Those are the default desk, chair, monitor, elevator, boss rug and the original floor tile. They live in `test/sprites.gen.js` and are embedded in `plugin.js`, under the MIT license © 2026 Paul Robello (see `THIRD_PARTY_NOTICES.md`). `preview.html` loads them only for comparison.

**Regenerate:**

```bash
cd themes/tools && python3 gen_themes.py && python3 gen_v56.py
```

Both are deterministic. `gen_themes.py` clears `sprites/` first. `gen_v56.py` writes the cleaner/propFx blocks into `themes.json`, so run it after `gen_themes.py`.
