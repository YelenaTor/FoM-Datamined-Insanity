# FoM Datamined Insanity

[![Fields of Mistria on Steam](https://img.shields.io/badge/Steam-Fields_of_Mistria-1b2838?logo=steam&logoColor=white)](https://store.steampowered.com/app/2142790/Fields_of_Mistria/)
[![MOMI Mod Loader](https://img.shields.io/badge/Mod_Loader-MOMI-blueviolet)](https://github.com/mods-of-mistria/mods-of-mistria-installer)
[![Related: mistria-notes](https://img.shields.io/badge/Related-mistria--notes-orange)](https://github.com/AnnaNomoly/mistria-notes)
[![License: CC0](https://img.shields.io/badge/License-CC0-lightgrey)](https://creativecommons.org/publicdomain/zero/1.0/)

Community-maintained reference for Fields of Mistria internals, reverse-engineered via Ghidra, `__fiddle__.json`, and YYTK runtime probing.

**Game version pinned: 0.15.x** — verify with `tools/query_fiddle.py --prefix version` before using for a newer patch.

> **See also:** [mistria-notes](https://github.com/AnnaNomoly/mistria-notes) — version-organized game data snapshots (v0.11–v0.15.1) and YYTK script call documentation (e.g. `gml_Script_modify_health@Ari@Ari`). Complementary to this repo's focus on spawn systems and hook catalogs.

## What's here

| Folder | Contents |
|--------|----------|
| `docs/architecture/` | GMS2 YYC binary format, data.win chunk layout, Grid/Anchor/Node runtime system |
| `docs/spawn/` | Ore vote tables, dungeon biome spawn config, surface node placement |
| `docs/scripts/` | Confirmed GML hook targets, NPC lifecycle, StoryExecutor, full 2340-script catalog |
| `docs/areas/` | All 79 location IDs with music and name keys |
| `docs/npcs/` | NPC IDs, gift preferences, portrait emotions |
| `docs/items/` | Item IDs from gift lists, forageables, store stock |
| `tools/` | Python scripts that regenerate all docs from a live game install |
| `raw/` | Gitignored — drop raw tool output here locally |

## Quick lookups

- **Is `gml_Script_pick_node` in data.win?** → [confirmed-hooks.md](docs/scripts/confirmed-hooks.md)
- **What weight does copper have in Upper Mines?** → [dungeon-ore-votes.md](docs/spawn/dungeon-ore-votes.md)
- **What's celine's sprite ID?** → [npc-ids.md](docs/npcs/npc-ids.md)
- **What room is `narrows` hosted in?** → [room-ids.md](docs/areas/room-ids.md)

## Regenerating docs

You need a Fields of Mistria game install and Python 3.9+.

```bash
cd tools
python discover_resources.py --game-path "C:/path/to/FoM"
python discover_areas.py     --game-path "C:/path/to/FoM"
python discover_npcs.py      --game-path "C:/path/to/FoM"
python discover_items.py     --game-path "C:/path/to/FoM"
python discover_crafting.py  --game-path "C:/path/to/FoM"
python discover_scripts.py   --game-path "C:/path/to/FoM"
```

Output lands in `raw/`. Copy the rendered sections into the relevant `docs/` file and open a PR.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Public domain / CC0. This is reference documentation only; no game assets are included.
