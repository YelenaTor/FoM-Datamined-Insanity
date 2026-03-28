# Grid / Anchor / Node Runtime System

> Verified: FoM 0.14.x — YYTK runtime probing + __fiddle__.json scan (2026-03-28)

FoM's resource node system is entirely runtime-managed. There are no pre-placed node instances in the ROOM chunk (confirmed by scanning all 214 rooms in data.win — see [yyc-runtime.md](yyc-runtime.md)).

## Core concepts

| Concept | Role |
|---------|------|
| **Grid** | Spatial data structure that tracks which cells are occupied. Each area has one Grid. Cell size = 32px (confirmed from `initialize_on_room_start@Grid@Grid` `cell_size` variable). |
| **Anchor** | A named group within a Grid. Manages node lifetime, enable/disable, and spatial queries. Examples: `ore_rock`, `small_rock`, `seam_rock`. |
| **Node** | A single data entry in an Anchor: type ID + position. Not a GM object. Rendered on-screen by `obj_node_renderer` (a single shared visual host). |
| **NodePrototype** | Struct that defines how a node type behaves: HP, drop table, respawn policy. Created once per room by `gml_Script_create_node_prototypes`. |

## Key scripts

| Script | Purpose |
|--------|---------|
| `gml_Script_initialize_on_room_start@Grid@Grid` | Sets up grid for current room, fires prototype creation |
| `gml_Script_create_node_prototypes` | Registers all node type definitions for this room (fires once per room entry) |
| `gml_Script_register_node@Anchor@Anchor` | Adds a single node entry to an Anchor — **candidate for EFL injection** (RUNTIME_VERIFY) |
| `gml_Script_write_node@Grid@Grid` | Marks a cell as occupied by a node |
| `gml_Script_attempt_to_write_object_node` | Safe wrapper for `write_node` with validation — used for player-placed objects |
| `gml_Script_find_node` | Query a node by cell position |
| `gml_Script_free_node@Anchor@Anchor` | Remove a node (triggered on harvest/destroy) |
| `gml_Script_new_day@Grid@Grid` | Respawn handler — called on day transition |
| `gml_Script_create_node_renderer` | Spawn the shared visual host `obj_node_renderer` |
| `gml_Script_item_node` | May be for item drops on ground (not persistent resource nodes) |

## How dungeon ore works

Dungeon ore is placed probabilistically, not at fixed coordinates. On room entry:

1. `initialize_on_room_start@Grid@Grid` fires
2. `create_node_prototypes` builds the prototype table for this biome
3. The biome's vote pool is consulted: each node type has a weight. A random selection places nodes in empty cells.
4. `register_node@Anchor@Anchor` is called per selected node (RUNTIME_VERIFY — this is the injection candidate)

Vote tables are in `__fiddle__.json` under `dungeons/dungeons/biomes/<biome>/<pool>`. See [dungeon-ore-votes.md](../spawn/dungeon-ore-votes.md).

## How surface nodes work

Surface world nodes (farm, narrows, deep_woods, abandoned_mines) are placed by room-start GML. The positions are hardcoded in the room-start script, not in fiddle. To discover empty cells:

- Hook `gml_Script_write_node@Grid@Grid` at runtime via YYTK
- Log every cell FoM occupies when entering that area
- Any non-occupied cell is safe for EFL `spawnRules.anchors` placement

The `grow_back` system respawns surface forageables on a new-day tick (`gml_Script_grow_back_new_day`). Cell size is 16px for the regrowth grid (vs 32px for the main Grid).

## obj_node_renderer

The sole visible host for all resource nodes. A single pooled GM object:

- `gml_Script_init@gml_Object_obj_node_renderer_Create_0` — initialise renderer for a node type
- `gml_Script_set_sprite@gml_Object_obj_node_renderer_Create_0` — set display sprite
- `gml_Script_collide@gml_Object_obj_node_renderer_Create_0` — collision callback
- `gml_Script_interact@gml_Object_obj_node_renderer_Create_0` — player interaction callback

When a node is harvested/destroyed, the renderer is freed; the node data is removed from the Anchor.
