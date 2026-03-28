# Surface Node Placement

> Source: data.win ROOM chunk scan + __fiddle__.json, FoM 0.15.x (2026-03-28)

Surface-world resource nodes (farm, narrows, deep_woods, abandoned_mines) are placed by room-start GML scripts. Positions are NOT stored in `__fiddle__.json` or in the ROOM chunk — they are hardcoded in the compiled bytecode.

## How to discover occupied cells

Use a YYTK hook on `gml_Script_write_node@Grid@Grid`:

```cpp
hooks_->registerScriptHook("probe_write_node", "gml_Script_write_node@Grid@Grid",
    [](YYTK::CInstance* self, YYTK::CInstance* other, YYTK::CCode* code,
       int argc, YYTK::RValue* args) {
        // args[0] = node_type_id (string), args[1] = cell_x, args[2] = cell_y
        log_.info("PROBE", "Node placed: " + args[0].asString()
                  + " at (" + std::to_string(args[1].asInt())
                  + "," + std::to_string(args[2].asInt()) + ")");
    });
```

Enter the target area. Every cell FoM occupies will be logged. Non-occupied cells are safe for `spawnRules.anchors`.

## `grow_back` system (surface regrowth)

Surface forageables (branches, weeds, flowers, small stones) regrow on each new day via `gml_Script_grow_back_new_day`.

Eligible spawn object types (from `__fiddle__.json` `grow_back/` keys):

```
small_rock_stone_one
branch
weed
tree_pine
tree_oak
```

Cell size for the regrowth grid: **16px** (vs 32px for the main ore-placement Grid).

## `locations/<area>/forageables`

`__fiddle__.json` stores a forageable **count** per area (integer only, not positions):

```
locations/deep_woods/forageables = 12
locations/narrows/forageables = 8
```

These counts drive the regrowth system — FoM places that many forageable nodes randomly in valid cells on each day transition. Positions are chosen at runtime, not stored.

## Season-based forageables

Forageable items vary by season. Full seasonal tables in [../items/item-ids.md](../items/item-ids.md).
