# StoryExecutor / Cutscene Scripts

> Source: `discover_scripts.py`, FoM 0.14.x (2026-03-28)

FoM's cutscene system is driven by `StoryExecutor`. All quest dialogue, NPC talk trees, and story triggers route through it.

## Key scripts

| Script | Purpose |
|--------|---------|
| `gml_Script_interact_with@StoryExecutor@StoryExecutor` | Player interacts with NPC — entry point for dialogue |
| `gml_Script_talk_to@StoryExecutor@StoryExecutor` | Starts a conversation |
| `gml_Script_anon@5082@interact_with@StoryExecutor@StoryExecutor` | Anonymous inner function of `interact_with` |
| `gml_Script_fulfill_quest@StoryExecutor@StoryExecutor` | Mark quest objective complete |
| `gml_Script_assert_quest_active@StoryExecutor@StoryExecutor` | Check if a quest is active |
| `gml_Script_turn_in_quest@StoryExecutor@StoryExecutor` | Complete quest and trigger reward |
| `gml_Script_goto_scene_trigger@StoryExecutor@StoryExecutor` | Jump to a named scene/cutscene |
| `gml_Script_anon@1293@goto_scene_trigger@StoryExecutor@StoryExecutor` | Inner goto_scene implementation |

## Story firing (EFL)

EFL's `StoryBridge::fireEvent(eventId)` calls:
```
gml_Script_story_start (RUNTIME_VERIFY — look up in __fiddle__.json)
```

Until confirmed, the EFL hook emits `STORY-H001` stub diagnostic.

## Quest scripts

| Script | Binding point |
|--------|--------------|
| `gml_Script_fulfill_quest@StoryExecutor@StoryExecutor` | `on_quest_update` |
| `gml_Script_assert_quest_active@StoryExecutor@StoryExecutor` | `on_quest_update` |
| `gml_Script_turn_in_quest@StoryExecutor@StoryExecutor` | `on_quest_update` |

## Trigger system

| Script | Purpose |
|--------|---------|
| `gml_Script_ScheduleExecuteAny@anon@23542@T2OutputFactory@T2r` | Execute a scheduled trigger |
| `gml_Script_execute_suite@TestSuite` (via anon wrappers) | Run a trigger test suite |

Triggers are declared under `cutscenes/` and `triggers/` in `__fiddle__.json`.
