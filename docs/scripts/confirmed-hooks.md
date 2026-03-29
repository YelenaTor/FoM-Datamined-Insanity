# Confirmed GML Hook Targets

> Source: data.win STRG scan via `discover_scripts.py`, FoM 0.15.x (2026-03-28)
> `[CONFIRMED]` = verified present in data.win string table.
> `[CONFIRMED via EFL_Probe, 2026-03-29]` = live runtime hook fired in EFL_Probe session.

## YYC Mode Note

Fields of Mistria uses the **YoYo Compiler (YYC)**. All GML scripts are compiled to native C++. This has a critical implication for hooking:

- `EVENT_OBJECT_CALL` / `Code_Execute` does **NOT** fire for any of these scripts.
- `YYTK::FWCodeEvent` callbacks are useless for FoM scripts.
- **Correct approach**: `GetNamedRoutinePointer(name, &ptr)` → cast to `CScript*` → read `m_Functions->m_ScriptFunction` → `MmCreateHook(module, name, fn, shim, &trampoline)`.

EFL implements this via a 32-slot compile-time shim table in `engine/src/bridge/hooks.cpp`. See `HookRegistry::registerScriptHook` for the full YYC path.

## Resource node tool scripts

These fire when the player uses a tool on a node. Suitable for `on_resource_gather` hooks.

| Script | Tool | Status |
|--------|------|--------|
| `gml_Script_hoe_node` | Hoe | [CONFIRMED] |
| `gml_Script_pick_node` | Pickaxe / mining | [CONFIRMED] |
| `gml_Script_water_node` | Watering can | [CONFIRMED] |
| `gml_Script_chop_node` | Axe | [CONFIRMED] |
| `gml_Script_shovel_node` | Shovel | [CONFIRMED] |
| `gml_Script_slash_node` | Combat slash | [CONFIRMED] |
| `gml_Script_can_hoe_node` | Hoe guard | [CONFIRMED] |
| `gml_Script_can_pick_node` | Pick guard | [CONFIRMED] |
| `gml_Script_can_water_node` | Water guard | [CONFIRMED] |
| `gml_Script_can_chop_node` | Chop guard | [CONFIRMED] |
| `gml_Script_can_shovel_node` | Shovel guard | [CONFIRMED] |

## Node spawn / registration scripts

Used by EFL for custom area node injection.

| Script | Index | Purpose | Notes |
|--------|-------|---------|-------|
| `gml_Script_create_node_prototypes` | 3238 | Registers all node type definitions for current room | [CONFIRMED via EFL_Probe, 2026-03-29] Hook target for dungeon vote injection |
| `gml_Script_register_node@Anchor@Anchor` | 242 | Adds a node entry to an Anchor | [CONFIRMED via EFL_Probe, 2026-03-29] Takes single GML struct arg; struct field layout TBD |
| `gml_Script_write_node@Grid@Grid` | 3181 | Marks a cell occupied | [CONFIRMED via EFL_Probe, 2026-03-29] Args: `(struct, grid_x, grid_y, struct, struct, bool, ...)` |
| `gml_Script_attempt_to_write_object_node` | 3251 | Validated node placement (checks can_write first) | [CONFIRMED via EFL_Probe, 2026-03-29] Args: `(struct, grid_x, grid_y, struct, struct, bool, ...)` Preferred for EFL surface area spawning |
| `gml_Script_find_node` | — | Query node at cell | Utility |
| `gml_Script_item_node` | — | Ground item drops (not persistent resource nodes) | Not for ore |

## Room start / area hooks

| Script | Purpose |
|--------|---------|
| `gml_Script_initialize_on_room_start@Grid@Grid` | Grid setup on area entry |
| `gml_Script_npcs_on_room_start` | NPC spawn on area entry |
| `gml_Script_on_room_start@Anchor@Anchor` | Anchor initialization |
| `gml_Script_festival_room_start` | Festival area setup |
| `gml_Script_goto_gm_room` | Room transition trigger |

## Crafting station hooks

| Script | Index | Purpose | Status |
|--------|-------|---------|--------|
| `gml_Script_spawn_crafting_menu` | 1635 | Opens the crafting UI | [CONFIRMED via EFL_Probe, 2026-03-29] Args: `(menu_struct, x: real, y: real, station_id: real)` |
| `gml_Script_CraftingMenu` | Crafting menu constructor | [CONFIRMED] |
| `gml_Script_load_crafting_ui_data` | Loads recipe list into UI | [CONFIRMED] |
| `gml_Script_check_item_craftable@CraftingMenu@CraftingMenu` | Per-recipe craftability check | [CONFIRMED] |
| `gml_Script_unlock_recipe@Ari@Ari` | Unlock a recipe for the player | [CONFIRMED] |
| `gml_Script_ari_has_recipe_anywhere` | Check if player has recipe | [CONFIRMED] |

## Respawn (new day) scripts

| Script | Purpose |
|--------|---------|
| `gml_Script_new_day@Grid@Grid` | Grid-level new-day handler |
| `gml_Script_grow_back_new_day` | Surface forageable regrowth |
| `gml_Script_bush_node_new_day` | Bush respawn |
| `gml_Script_crop_node_new_day` | Crop growth tick |
| `gml_Script_tree_node_new_day` | Tree regrowth |
| `gml_Script_npas_new_day` | Animal respawn |
