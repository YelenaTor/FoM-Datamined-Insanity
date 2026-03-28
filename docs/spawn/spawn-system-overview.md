# Spawn System Overview

> Source: data.win ROOM chunk scan + __fiddle__.json, FoM 0.15.x (2026-03-28)

## Key Finding

**FoM does NOT pre-place resource nodes in rooms. All node placement is runtime-only.**

Scanning all 214 rooms in `data.win` for object instances matching any ore/rock/node pattern returns 0 results. There are no `obj_iron_rock`, `obj_copper_ore`, or similar objects in the OBJT chunk at all.

## Three spawn contexts

### 1. EFL custom areas — use `spawnRules.anchors`

EFL custom areas (backed by `HijackedRoomBackend`) have no pre-existing nodes. Any valid grid cell can be used. Specify `"area_id": "x,y"` in `spawnRules.anchors`. EFL calls `attempt_to_write_object_node` (validated path) at room activation.

### 2. FoM dungeon floors — use `spawnRules.dungeonVotes`

Dungeon floors use a **probabilistic vote-based spawn system**. Each biome defines weighted pools for ore types. Fixed coordinates do not exist and `spawnRules.anchors` cannot be used here.

EFL hooks `gml_Script_create_node_prototypes` and injects entries into the biome vote table. The runtime mutation API (`gml_Script_register_node@Anchor@Anchor`) requires RUNTIME_VERIFY before the real call can be wired.

See [dungeon-ore-votes.md](dungeon-ore-votes.md) for the full vote tables.

### 3. FoM surface areas — coordinate discovery required

Surface world areas (farm, narrows, deep_woods, abandoned_mines) have nodes placed by room-start GML. Positions are hardcoded, not in fiddle. To find free cells:

1. Hook `gml_Script_write_node@Grid@Grid` via YYTK at runtime
2. Enter the target area — FoM will log every cell it occupies
3. Pick a non-occupied cell for `spawnRules.anchors`

## Node type IDs (from `object_prototypes/rock` in fiddle)

All confirmed ore node type strings:

```
node_copper, rock_copper, seam_rock_copper
node_iron,   rock_iron,   seam_rock_iron
node_silver, rock_silver, seam_rock_silver
node_gold,   rock_gold,   seam_rock_gold
node_ruby,   rock_ruby
node_sapphire, rock_sapphire
node_emerald, rock_emerald
node_diamond, rock_diamond
node_mistril, rock_mistril, seam_rock_mistril
node_pink_diamond, rock_pink_diamond
rock_void
```

**Variants:**
- `node_*` — lower drop count (common ore rocks)
- `rock_*` — higher drop count (rare large rocks)
- `seam_*` — low HP, drops from ore seams/veins
