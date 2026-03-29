# GML Script Catalog

> Source: `discover_scripts.py` — full data.win STRG scan, FoM 0.15.x (2026-03-28)
> **2340 unique script names** across 18 areas.

This file contains the primary Option B injection target analysis. For the complete raw list, run `tools/discover_scripts.py --game-path <path>`.

## Runtime discovery approach (EFL_Probe methodology)

FoM uses YYC — scripts are native C++ functions, so static STRG scanning gives names but not live call order or argument types. To confirm hook candidates at runtime, EFL_Probe was built as a standalone Aurie module (separate from EFL.dll).

**Phase 1 — Discovery scan**: At `ModuleInitialize`, enumerate `YYTK::GetScriptData(0..N)` stopping after 500 consecutive misses. For each `CScript*`, read `m_Code->GetName()` (works in YYC mode even though `m_Code` is otherwise unused). Filter by keyword. This produces an indexed list of all probe-relevant script names with their array indices.

**Phase 2 — Live hooks**: For each candidate, call `GetNamedRoutinePointer(name, &ptr)`, cast to `CScript*`, extract `m_Functions->m_ScriptFunction`, then `MmCreateHook(module, name, hookFn, &trampoline)`. When the script fires, log all args.

**Key script indices confirmed 2026-03-29**:

| Script | Index | Confirmed |
|:-------|:------|:----------|
| `gml_Script_register_node@Anchor@Anchor` | 242 | Yes — fires with single struct arg on new game |
| `gml_Script_spawn_crafting_menu` | 1635 | Yes — fires on opening any crafting station |
| `gml_Script_write_node@Grid@Grid` | 3181 | Yes — fires during Farm entry |
| `gml_Script_attempt_to_write_object_node` | 3251 | Yes — fires during Farm entry, 9 args |
| `gml_Script_create_node_prototypes` | 3238 | Yes — fires once per room on grid init |

The `discover_scripts.py` static scan and the EFL_Probe runtime approach are complementary: static gives the full name table; live probe gives call order, arg types, and confirms which candidates actually fire for target game actions.

## Option B injection targets

These are the confirmed binding points for Script Injection (EFL Unit 13).

### `on_npc_tick`
- `gml_Script_npc_is_unlocked`
- `gml_Script_npcs_on_step`

### `on_npc_interact`
- `gml_Script_interact_with@StoryExecutor@StoryExecutor`
- `gml_Script_talk_to@StoryExecutor@StoryExecutor`
- `gml_Script_anon@5082@interact_with@StoryExecutor@StoryExecutor`
- `gml_Script_anon@5214@anon@5082@interact_with@StoryExecutor@StoryExecutor`

### `on_area_enter`
- `gml_Script_initialize_on_room_start@Grid@Grid`
- `gml_Script_npcs_on_room_start`
- `gml_Script_on_room_start@Anchor@Anchor`
- `gml_Script_on_room_start@DungeonRunner@DungeonRunner`
- (and 28 more — run `discover_scripts.py --search room_start`)

### `on_area_exit`
- No confirmed candidates yet. Manual investigation needed.
- Candidate: `gml_Script_goto_gm_room` (room transition trigger)

### `on_resource_gather`
- `gml_Script_pick_node`
- `gml_Script_hoe_node`
- `gml_Script_water_node`
- `gml_Script_chop_node`
- `gml_Script_shovel_node`
- `gml_Script_slash_node`
- (plus `can_*` guard variants)

### `on_quest_update`
- `gml_Script_fulfill_quest@StoryExecutor@StoryExecutor`
- `gml_Script_assert_quest_active@StoryExecutor@StoryExecutor`
- `gml_Script_turn_in_quest@StoryExecutor@StoryExecutor`

### `on_trigger_fire`
- `gml_Script_ScheduleExecuteAny@anon@23542@T2OutputFactory@T2r`
- `gml_Script_goto_scene_trigger@StoryExecutor@StoryExecutor`
- (and 24 more — run `discover_scripts.py --search trigger`)

### `on_save`
- `gml_Script____struct___447@serialize@Npc@Npc`
- `gml_Script_serialize@Npc@Npc` (variant)
- (and save-related serialize scripts)

### `on_load`
- `gml_Script_deserialize@Npc@Npc`
- `gml_Script_deserialize_daycare`
- `gml_Script_fiddle_deserialize_season`
- `gml_Script_schedule_deserialize_expirator@T2r@T2r`

## Area breakdown (top-level scripts only)

To view scripts by area:
```bash
python tools/discover_scripts.py --game-path "C:/path/to/FoM" --list-areas
python tools/discover_scripts.py --game-path "C:/path/to/FoM" --area Crafting --top-level-only
```

| Area | Scripts (approx.) |
|------|------------------|
| Crafting | 272 |
| NPC | ~180 |
| Grid/Node | ~315 (other_node) |
| Story/Quest | ~90 |
| UI/Menu | ~400 |
| Miscellaneous | ~700 |
