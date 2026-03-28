# Dungeon Biome Ore Vote Tables

> Source: `__fiddle__.json` key `dungeons/dungeons/biomes/<biome>/<pool>`, FoM 0.14.x (2026-03-28)

FoM dungeons use weighted probabilistic spawning. Each biome has pools (`ore_rock`, `seam_rock`, `small_rock`). On each floor, the game rolls against the pool weights to place nodes in empty cells.

## Biome vote tables

### Upper Mines (floors 1–19)
Primary ore: copper | Gem: ruby

| Pool | Node type | Weight |
|------|-----------|--------|
| ore_rock | node_copper | 45 |
| ore_rock | rock_copper | 9 |
| ore_rock | node_ruby | 3 |
| ore_rock | rock_ruby | 1 |
| seam_rock | seam_rock_copper | 1 |
| small_rock | small_rock_stone_upper | 1 |
| small_rock | small_dirt_rock_one | 1 |

### The Tide Caverns (floors 20–39)
Primary ore: iron | Gem: sapphire

| Pool | Node type | Weight |
|------|-----------|--------|
| ore_rock | node_iron | 45 |
| ore_rock | rock_iron | 9 |
| ore_rock | node_sapphire | 3 |
| ore_rock | rock_sapphire | 1 |
| seam_rock | seam_rock_iron | 1 |
| small_rock | small_rock_stone_two | 1 |
| small_rock | small_dirt_rock_two | 1 |

### Deep Earth (floors 40–59)
Primary ore: silver | Gem: emerald

| Pool | Node type | Weight |
|------|-----------|--------|
| ore_rock | node_silver | 45 |
| ore_rock | rock_silver | 9 |
| ore_rock | node_emerald | 3 |
| ore_rock | rock_emerald | 1 |
| seam_rock | seam_rock_silver | 1 |
| small_rock | small_rock_stone_three | 1 |
| small_rock | small_dirt_rock_three | 1 |

### The Lava Caves (floors 60–79)
Primary ore: gold | Gem: diamond

| Pool | Node type | Weight |
|------|-----------|--------|
| ore_rock | node_gold | 45 |
| ore_rock | rock_gold | 9 |
| ore_rock | node_diamond | 3 |
| ore_rock | rock_diamond | 1 |
| seam_rock | seam_rock_gold | 1 |
| small_rock | small_rock_stone_four | 1 |
| small_rock | small_dirt_rock_four | 1 |

### Ancient Ruins (floors 80+)
Primary ore: mistril | Gem: pink_diamond

| Pool | Node type | Weight |
|------|-----------|--------|
| ore_rock | node_mistril | 45 |
| ore_rock | rock_mistril | 9 |
| ore_rock | node_pink_diamond | 3 |
| ore_rock | rock_pink_diamond | 1 |
| seam_rock | seam_rock_mistril | 1 |
| small_rock | small_rock_stone_five | 1 |
| small_rock | small_dirt_rock_five | 1 |

## Pattern

Every biome follows the same weight distribution:
- Primary ore node: 45
- Primary ore rock (high-yield variant): 9
- Gem node: 3
- Gem rock: 1

This gives a ~78% chance of the base ore node, ~15% large ore rock, ~5% gem node, ~2% gem rock per occupied cell.

## Custom node injection (EFL)

To add a custom EFL ore to a dungeon biome, declare in `spawnRules.dungeonVotes`:

```json
"dungeonVotes": [
  { "biome": "upper_mines", "pool": "ore_rock", "weight": 5 }
]
```

EFL will hook `gml_Script_create_node_prototypes` and call `gml_Script_register_node@Anchor@Anchor` (RUNTIME_VERIFY pending) to inject the entry.
