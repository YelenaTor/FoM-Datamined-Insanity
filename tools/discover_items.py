"""
discover_items.py — Fields of Mistria item discovery tool

Collects item IDs from NPC gift preferences, store stock, and forageable
lists in __fiddle__.json.

Output: raw/items.txt

Usage:
    python discover_items.py --game-path "C:/path/to/FoM"
    python discover_items.py --game-path "C:/path/to/FoM" --search gem
    python discover_items.py --game-path "C:/path/to/FoM" --gifts-only
    python discover_items.py --game-path "C:/path/to/FoM" --npc celine
"""

import json
import os
import argparse
from collections import defaultdict

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "items.txt")


def find_fiddle(game_path):
    candidates = [
        os.path.join(game_path, "runtime", "Fields of Mistria", "__fiddle__.json"),
        os.path.join(game_path, "__fiddle__.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"__fiddle__.json not found under {game_path!r}")


def load_fiddle(game_path):
    with open(find_fiddle(game_path), encoding="utf-8") as f:
        return json.load(f)


def discover_gift_data(data):
    npc_gifts = defaultdict(dict)
    for k, v in data.items():
        if not k.startswith("npcs/"):
            continue
        parts = k.split("/")
        if len(parts) != 3:
            continue
        npc_id, field = parts[1], parts[2]
        if field in ("liked_gifts", "loved_gifts", "disliked_gift_tags", "hated_gift"):
            npc_gifts[npc_id][field] = v
    return npc_gifts


def discover_forageable_items(data):
    forageables = defaultdict(lambda: defaultdict(list))
    for k, v in data.items():
        if not k.startswith("forageables/"):
            continue
        parts = k.split("/")
        if len(parts) >= 4 and isinstance(v, str):
            season, rarity = parts[1], parts[2]
            forageables[season][rarity].append(v)
    return forageables


def discover_store_items(data):
    store_items = defaultdict(set)
    for k, v in data.items():
        if not k.startswith("stores/"):
            continue
        parts = k.split("/")
        if len(parts) < 2:
            continue
        store_id = parts[1]
        if parts[-1] == "item" and isinstance(v, str):
            store_items[store_id].add(v)
        elif isinstance(v, dict) and "item" in v:
            store_items[store_id].add(v["item"])
    return store_items


def all_gift_items(npc_gifts):
    items = set()
    for gifts in npc_gifts.values():
        for field in ("liked_gifts", "loved_gifts"):
            val = gifts.get(field, [])
            if isinstance(val, list):
                items.update(val)
        hated = gifts.get("hated_gift")
        if isinstance(hated, str):
            items.add(hated)
    return sorted(items)


def run(game_path, search_filter=None, gifts_only=False, npc_filter=None):
    data = load_fiddle(game_path)
    npc_gifts = discover_gift_data(data)
    forageables = discover_forageable_items(data)
    store_items = discover_store_items(data)

    lines = ["=" * 72, "FIELDS OF MISTRIA -- ITEMS (from gift lists, stores, forageables)",
             "=" * 72, "",
             "  NOTE: FoM stores items by string ID throughout the data.",
             "  Use these IDs as 'giftableItems' in world-npc content packs.", "",
             "=" * 72, "NPC GIFT PREFERENCES", "=" * 72]

    filtered_npcs = {k: v for k, v in npc_gifts.items()
                     if not npc_filter or npc_filter.lower() in k.lower()}
    for npc_id in sorted(filtered_npcs):
        gifts = filtered_npcs[npc_id]
        loved = gifts.get("loved_gifts", [])
        liked = gifts.get("liked_gifts", [])
        hated = gifts.get("hated_gift", "")
        disliked_tags = gifts.get("disliked_gift_tags", [])
        if search_filter:
            loved = [i for i in loved if search_filter.lower() in i.lower()]
            liked = [i for i in liked if search_filter.lower() in i.lower()]
        if not loved and not liked and not hated:
            continue
        lines.append(f"\n  {npc_id}:")
        if loved:
            lines.append(f"    loved:    {', '.join(sorted(loved))}")
        if liked:
            lines.append(f"    liked:    {', '.join(sorted(liked))}")
        if hated:
            lines.append(f"    hated:    {hated}")
        if disliked_tags:
            lines.append(f"    disliked_tags: {', '.join(disliked_tags)}")

    if not gifts_only:
        all_items = all_gift_items(npc_gifts)
        if search_filter:
            all_items = [i for i in all_items if search_filter.lower() in i.lower()]
        lines += ["", "=" * 72, f"ALL UNIQUE GIFT ITEMS ({len(all_items)} total)",
                  "=" * 72, "  (union of loved/liked/hated across all NPCs)", ""]
        lines.extend(f"  {item}" for item in all_items)

        lines += ["", "=" * 72, "FORAGEABLE ITEMS BY SEASON", "=" * 72]
        for season in sorted(forageables):
            lines.append(f"\n  {season.upper()}:")
            for rarity in sorted(forageables[season]):
                items_list = sorted(set(forageables[season][rarity]))
                if search_filter:
                    items_list = [i for i in items_list if search_filter.lower() in i.lower()]
                if items_list:
                    lines.append(f"    {rarity}: {', '.join(items_list)}")

        lines += ["", "=" * 72, "STORE STOCK (item IDs per shop)", "=" * 72]
        for store_id in sorted(store_items):
            items_list = sorted(store_items[store_id])
            if search_filter:
                items_list = [i for i in items_list if search_filter.lower() in i.lower()]
            if not items_list:
                continue
            lines.append(f"\n  {store_id} ({len(items_list)} items):")
            lines.append(f"    {', '.join(items_list[:30])}")
            if len(items_list) > 30:
                lines.append(f"    ...and {len(items_list)-30} more")

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover FoM items and gift preferences")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--search", help="Filter item IDs by substring")
    parser.add_argument("--gifts-only", action="store_true",
                        help="Show only NPC gift data (skip forageables/stores)")
    parser.add_argument("--npc", help="Filter by NPC name substring")
    args = parser.parse_args()
    run(args.game_path, search_filter=args.search, gifts_only=args.gifts_only, npc_filter=args.npc)
