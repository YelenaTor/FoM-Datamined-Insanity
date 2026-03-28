# Item IDs

> Source: `__fiddle__.json` — NPC gift lists, store stock, forageables, FoM 0.14.x (2026-03-28)

FoM stores items by string ID throughout `__fiddle__.json`. There is no single `items/` key — IDs appear in gift preferences, store stock, and recipe data.

## Using item IDs

Use these IDs in EFL world-npc content packs as `giftableItems`:
```json
{
  "id": "my_npc",
  "giftableItems": ["coffee", "wildberry_pie", "ore_mistril"],
  "heartsPerGift": 2
}
```

## Searching for item IDs

```bash
# Find all items containing "diamond"
python tools/discover_items.py --search diamond --game-path "C:/path/to/FoM"

# All gift data for a specific NPC
python tools/discover_items.py --gifts-only --npc celine --game-path "C:/path/to/FoM"
```

## Ore IDs (from spawn system)

```
ore_copper, ore_iron, ore_silver, ore_gold, ore_mistril
ore_ruby, ore_sapphire, ore_emerald, ore_diamond, ore_pink_diamond
perfect_ruby, perfect_sapphire, perfect_emerald, perfect_diamond,
perfect_gold_ore, perfect_pink_diamond
```

## Selected item IDs by category

### Ores and gems
`ore_copper`, `ore_iron`, `ore_silver`, `ore_gold`, `ore_mistril`,
`ore_ruby`, `ore_sapphire`, `ore_emerald`, `ore_diamond`, `ore_pink_diamond`

### Ingots
`copper_ingot`, `iron_ingot`, `silver_ingot`, `gold_ingot`, `mistril_ingot`

### Crops (seasonal)
`potato`, `beet`, `cabbage`, `pumpkin`, `apple`, `lemon`, `peach`, `bell_berry`

### Flowers
`middlemist`, `plum_blossom`, `jasmine`, `heather`, `snapdragon`,
`crystal_rose`, `fog_orchid`, `frost_lily`, `tulip`, `rose`, `wildberry`

### Cooked food / gifts
`coffee`, `cup_of_tea`, `gazpacho`, `lemon_pie`, `pumpkin_pie`,
`wildberry_pie`, `wildberry_scone`, `apple_juice`, `red_wine`, `white_wine`

## Seasonal forageables

Run `tools/discover_items.py --game-path <path>` for the full seasonal table. Items vary by season and rarity (common/uncommon/rare).

## Store stock

FoM has multiple shops. Run:
```bash
python tools/discover_items.py --game-path "C:/path/to/FoM"
```
to see per-store item IDs (general_store, blacksmith, etc.).
