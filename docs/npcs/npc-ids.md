# NPC IDs

> Source: `__fiddle__.json` key scan under `npcs/`, FoM 0.15.x (2026-03-28)
> **34 NPCs** with fiddle data.

## NPC list with key data

| ID | Dateable | Sprite icon | Music |
|----|----------|-------------|-------|
| adeline | yes | spr_ui_generic_icon_npc_adeline | Music/Npc Tracks/Adeline |
| balor | yes | spr_ui_generic_icon_npc_balor | — |
| caldarus | yes | spr_ui_generic_icon_npc_caldarus | — |
| celine | yes | spr_ui_generic_icon_npc_celine | Music/Npc Tracks/Celine |
| dell | no | spr_ui_generic_icon_npc_dell | — |
| eiland | no | spr_ui_generic_icon_npc_eiland | — |
| elsie | no | spr_ui_generic_icon_npc_elsie | — |
| errol | no | spr_ui_generic_icon_npc_errol | — |
| hayden | yes | spr_ui_generic_icon_npc_hayden | — |
| hemlock | yes | spr_ui_generic_icon_npc_hemlock | — |
| jo | no | spr_ui_generic_icon_npc_jo | — |
| landen | yes | spr_ui_generic_icon_npc_landen | — |
| luc | no | spr_ui_generic_icon_npc_luc | — |
| maple | yes | spr_ui_generic_icon_npc_maple | — |
| nora | no | spr_ui_generic_icon_npc_nora | — |
| reina | yes | spr_ui_generic_icon_npc_reina | — |
| seridia | no | — | Music/Npc Tracks/Seridia |
| terithia | no | spr_ui_generic_icon_npc_terithia | — |
| valen | yes | spr_ui_generic_icon_npc_valen | — |

(Run `tools/discover_npcs.py --game-path <path>` for all 34 with full field data.)

## Gift preferences (selected NPCs)

### adeline
- **loved:** coffee, cup_of_tea, gazpacho, lemon_pie, middlemist, mistril_ingot, peaches_and_cream, perfect_pink_diamond, plum_blossom, pumpkin_pie
- **liked:** candied_lemon_peel, heather, lemon, lemonade, ore_diamond, ore_mistril, ore_pink_diamond, paper, peach, pineshroom_toast, pumpkin_stew, red_wine, snapdragon, sour_lemon_cake, spicy_cheddar_biscuit, tulip, vegetable_soup, white_wine, wildberry_pie, wildberry_scone
- **hated:** morel_mushroom
- **disliked tags:** junk, bugs, mushroomy, weird_gift

### balor
- **loved:** alda_gem_bracelet, apple_honey_curry, chili_coconut_curry, deluxe_curry, family_crest_pendant, perfect_diamond, perfect_emerald, perfect_pink_diamond, perfect_ruby, perfect_sapphire
- **liked:** cauliflower_curry, chickpea_curry, crystal_rose, fog_orchid, frost_lily, gold_ingot, golden_cheesecake, golden_cookies, jasmine, ore_diamond, ore_gold, ore_ruby, ore_sapphire, perfect_gold_ore, rose
- **hated:** ant

### caldarus
- **loved:** apple_honey_curry, fried_rice, harvest_plate, mont_blanc, seafood_boil, seafood_snow_pea_noodles, spring_galette, statuette_of_caldarus, sushi_platter, veggie_sub_sandwich

For full gift data for all NPCs, run:
```bash
python tools/discover_items.py --gifts-only --game-path "C:/path/to/FoM"
```

## Portrait emotions

Query emotions for a specific NPC:
```bash
python tools/query_fiddle.py --npc-emotions celine --game-path "C:/path/to/FoM"
python tools/query_fiddle.py --common-emotions --game-path "C:/path/to/FoM"
```

Common emotions available across most NPCs: `normal`, `happy`, `sad`, `angry`, `surprised`, `embarrassed`, `thinking`, `blushing`.
