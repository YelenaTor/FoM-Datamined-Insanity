# Contributing

## What to contribute

- Corrections to existing entries (wrong script name, changed in a patch)
- New hook targets found via YYTK probing
- New fiddle keys discovered in a game update
- Additional NPC/item/area data

## Format rules

- Always note the FoM version you tested against at the top of any significant addition:
  `> Verified: FoM 0.14.x`
- For script names: only mark `[CONFIRMED]` if you have verified the name exists in `data.win` (e.g. via `discover_scripts.py` output or Ghidra).
- For fiddle keys: paste the exact `key = value` output from `query_fiddle.py`.

## Workflow

1. Run the relevant discovery tool against your game install
2. Copy changed sections into the appropriate `docs/` file
3. Add a version note
4. Open a PR with the raw output file in `raw/` (it will be gitignored but reviewers can download from the PR diff)

## Citation format

When adding a finding, include the source:

```
Source: __fiddle__.json key scan, FoM 0.14.x (2026-03-28)
Source: Ghidra decompile of FieldsOfMistria.exe, FoM 0.14.x
Source: YYTK runtime probe via gml_Script_initialize_on_room_start, FoM 0.14.x
```
