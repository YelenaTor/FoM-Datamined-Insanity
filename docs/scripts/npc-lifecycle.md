# NPC Lifecycle GML Scripts

> Source: `discover_npcs.py` + `discover_scripts.py`, FoM 0.14.x (2026-03-28)

## Key hook targets

| Script | Binding point | Notes |
|--------|--------------|-------|
| `gml_Script_npc_is_unlocked` | `on_npc_tick` | Fires every tick per NPC; guards visibility |
| `gml_Script_npcs_on_step` | `on_npc_tick` | Main NPC update loop |
| `gml_Script_npcs_on_room_start` | `on_area_enter` | Spawns NPCs in the current area |
| `gml_Script_interact_with@StoryExecutor@StoryExecutor` | `on_npc_interact` | Player initiates NPC talk |
| `gml_Script_talk_to@StoryExecutor@StoryExecutor` | `on_npc_interact` | Starts dialogue via StoryExecutor |
| `gml_Script_receive_gift@gml_Object_par_NPC_Create_0` | Gift giving | Called when player gifts an item |
| `gml_Script_initialize@gml_Object_par_NPC_Create_0` | NPC creation | Per-NPC init |

## NPC identification scripts

| Script | Purpose |
|--------|---------|
| `gml_Script_npc_id_to_string` | Convert NPC index → string ID |
| `gml_Script_string_to_npc_id` | Convert string ID → NPC index |
| `gml_Script_npc_is_unlocked` | Check if NPC is unlocked in current save |

## Heart / gift scripts

| Script | Purpose |
|--------|---------|
| `gml_Script_receive_gift@gml_Object_par_NPC_Create_0` | Handle gift receipt |

Heart point storage: `EFL/<modId>/npc/<npcId>/hearts` (int) via SaveService.

## NPC serialization

| Script | Purpose |
|--------|---------|
| `gml_Script____struct___447@serialize@Npc@Npc` | Serialize NPC state |
| `gml_Script_deserialize@Npc@Npc` | Deserialize NPC state |

## FSM scripts (NPC behavior)

FoM NPCs use a state machine (`AriFsm`). Key scripts:

```
gml_Script_create_default_fsm@gml_Object_par_NPC_Create_0
gml_Script_bop_along_path@anon@4629@create_default_fsm@gml_Object_par_NPC_Create_0
gml_Script_begin_pathfinding@anon@4629@create_default_fsm@gml_Object_par_NPC_Create_0
```

The FSM handles NPC movement, idle behavior, eating/drinking routines, and schedule-driven actions.

## Portrait system

Portraits are stored under `npcs/<npc_id>/portraits/<emotion>` in `__fiddle__.json`.
See [../npcs/npc-ids.md](../npcs/npc-ids.md) for per-NPC emotion lists.

Common emotions available across most NPCs: `normal`, `happy`, `sad`, `angry`, `surprised`, `embarrassed`.

Query emotions for a specific NPC:
```bash
python tools/query_fiddle.py --npc-emotions celine --game-path "C:/path/to/FoM"
```
