"""
query_fiddle.py — Query the Fields of Mistria __fiddle__.json game data file.

Usage examples:
    python query_fiddle.py --game-path "C:/path/to/FoM" --prefix "npcs/celine/portraits"
    python query_fiddle.py --game-path "C:/path/to/FoM" --prefix "locations" --depth 1
    python query_fiddle.py --game-path "C:/path/to/FoM" --search "portrait" --limit 20
    python query_fiddle.py --game-path "C:/path/to/FoM" --npc-emotions celine
    python query_fiddle.py --game-path "C:/path/to/FoM" --all-locations
    python query_fiddle.py --game-path "C:/path/to/FoM" --common-emotions

The fiddle file is expected at:
    <game-path>/runtime/Fields of Mistria/__fiddle__.json
"""

import json
import argparse
import os
from collections import Counter


def find_fiddle(game_path):
    candidates = [
        os.path.join(game_path, "runtime", "Fields of Mistria", "__fiddle__.json"),
        os.path.join(game_path, "__fiddle__.json"),
        os.path.join(game_path, "data", "__fiddle__.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        f"__fiddle__.json not found under {game_path!r}.\n"
        "Try pointing --game-path directly at the folder containing __fiddle__.json."
    )


def load_fiddle(game_path):
    path = find_fiddle(game_path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cmd_prefix(data, prefix, depth=None, limit=50):
    matches = sorted(k for k in data.keys() if k.startswith(prefix))
    if depth is not None:
        seen = set()
        filtered = []
        for k in matches:
            parts = k.split("/")
            truncated = "/".join(parts[: depth + 1])
            if truncated not in seen:
                seen.add(truncated)
                filtered.append(truncated)
        matches = filtered
    for k in matches[:limit]:
        if depth is None:
            print(f"  {k} = {data.get(k, '(branch)')}")
        else:
            print(f"  {k}")
    if len(matches) > limit:
        print(f"  ... and {len(matches) - limit} more")
    print(f"\nTotal: {len(matches)} entries")


def cmd_search(data, pattern, limit=30):
    matches = sorted(k for k in data.keys() if pattern.lower() in k.lower())
    for k in matches[:limit]:
        print(f"  {k} = {data[k]}")
    if len(matches) > limit:
        print(f"  ... and {len(matches) - limit} more")
    print(f"\nTotal: {len(matches)} matches")


def cmd_npc_emotions(data, npc_name):
    prefix = f"npcs/{npc_name}/portraits/"
    emotions = sorted(set(
        k[len(prefix):].split("/")[0]
        for k in data.keys()
        if k.startswith(prefix)
    ))
    if not emotions:
        print(f"No portraits found for NPC '{npc_name}'")
        return
    print(f"Portrait emotions for {npc_name} ({len(emotions)} total):")
    for e in emotions:
        print(f"  {e}")


def cmd_common_emotions(data):
    emotion_counts = Counter()
    npc_names = sorted(set(
        k.split("/")[1]
        for k in data.keys()
        if k.startswith("npcs/") and "/portraits/" in k
    ))
    for npc in npc_names:
        emotions = set(
            k.split("/")[3]
            for k in data.keys()
            if k.startswith(f"npcs/{npc}/portraits/")
        )
        for e in emotions:
            emotion_counts[e] += 1

    total = len(npc_names)
    print(f"Emotion availability across {total} NPCs:\n")
    for e, count in sorted(emotion_counts.items(), key=lambda x: (-x[1], x[0])):
        bar = "#" * (count * 30 // total)
        print(f"  {e:30s} {count:2d}/{total}  {bar}")


def cmd_all_locations(data):
    loc_names = sorted(set(
        k.split("/")[1]
        for k in data.keys()
        if k.startswith("locations/")
    ))
    print(f"All locations ({len(loc_names)}):\n")
    for loc in loc_names:
        name = data.get(f"locations/{loc}/name", "")
        music = data.get(f"locations/{loc}/music", "")
        extra = []
        if name:
            extra.append(f'name="{name}"')
        if music:
            extra.append(f'music="{music}"')
        suffix = f"  ({', '.join(extra)})" if extra else ""
        print(f"  {loc}{suffix}")


def main():
    parser = argparse.ArgumentParser(description="Query FoM __fiddle__.json")
    parser.add_argument("--game-path", required=True,
                        help="Path to FoM game folder (containing __fiddle__.json)")
    parser.add_argument("--prefix", help="Show keys with this prefix")
    parser.add_argument("--depth", type=int, help="Truncate prefix results at depth")
    parser.add_argument("--search", help="Search all keys for substring")
    parser.add_argument("--npc-emotions", metavar="NPC", help="List portrait emotions for NPC")
    parser.add_argument("--common-emotions", action="store_true",
                        help="Show emotion availability across all NPCs")
    parser.add_argument("--all-locations", action="store_true", help="List all locations")
    parser.add_argument("--limit", type=int, default=50, help="Max results (default 50)")
    args = parser.parse_args()

    data = load_fiddle(args.game_path)

    if args.prefix:
        cmd_prefix(data, args.prefix, args.depth, args.limit)
    elif args.search:
        cmd_search(data, args.search, args.limit)
    elif args.npc_emotions:
        cmd_npc_emotions(data, args.npc_emotions)
    elif args.common_emotions:
        cmd_common_emotions(data)
    elif args.all_locations:
        cmd_all_locations(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
