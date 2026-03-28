"""
discover_areas.py — Fields of Mistria area/room discovery tool

Enumerates all room/area IDs from __fiddle__.json and cross-references
GML room transition scripts.

Output: raw/areas.txt

Usage:
    python discover_areas.py --game-path "C:/path/to/FoM"
    python discover_areas.py --game-path "C:/path/to/FoM" --search waterfall
"""

import json
import re
import os
import argparse

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "areas.txt")


def find_fiddle(game_path):
    candidates = [
        os.path.join(game_path, "runtime", "Fields of Mistria", "__fiddle__.json"),
        os.path.join(game_path, "__fiddle__.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"__fiddle__.json not found under {game_path!r}")


def find_gml_discovery(game_path):
    candidates = [
        os.path.join(game_path, ".temp", "gml_discovery.txt"),
        os.path.join(game_path, "gml_discovery.txt"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"gml_discovery.txt not found under {game_path!r}")


def load_fiddle(game_path):
    with open(find_fiddle(game_path), encoding="utf-8") as f:
        return json.load(f)


def load_gml_scripts(game_path):
    scripts = []
    with open(find_gml_discovery(game_path), encoding="utf-8") as f:
        for line in f:
            m = re.search(r"gml_Script_\S+", line)
            if m:
                scripts.append(m.group(0))
    return sorted(set(scripts))


def discover_locations(data):
    locations = {}
    for k, v in data.items():
        if not k.startswith("locations/"):
            continue
        parts = k.split("/")
        if len(parts) < 2:
            continue
        loc_id = parts[1]
        if loc_id not in locations:
            locations[loc_id] = {}
        if len(parts) >= 3:
            locations[loc_id]["/".join(parts[2:])] = v
    return locations


def discover_room_scripts(all_scripts):
    patterns = ["room", "transition", "room_start", "initialize_on_room"]
    return [s for s in all_scripts if any(p in s.lower() for p in patterns)]


def run(game_path, search_filter=None):
    data = load_fiddle(game_path)
    all_scripts = load_gml_scripts(game_path)

    locations = discover_locations(data)
    room_scripts = discover_room_scripts(all_scripts)

    if search_filter:
        locations = {k: v for k, v in locations.items() if search_filter.lower() in k.lower()}
        room_scripts = [s for s in room_scripts if search_filter.lower() in s.lower()]

    lines = ["=" * 72, "FIELDS OF MISTRIA — AREAS / LOCATIONS", "=" * 72,
             f"Total locations: {len(locations)}\n"]

    for loc_id in sorted(locations):
        info = locations[loc_id]
        name = info.get("name", "")
        music = info.get("music", "")
        row = f"  {loc_id}"
        extras = [x for x in [f'name="{name}"', f'music="{music}"'] if '=""' not in x]
        if extras:
            row += "  ->  " + "  ".join(extras)
        lines.append(row)

    lines += ["", "=" * 72, f"ROOM TRANSITION / ROOM_START GML SCRIPTS ({len(room_scripts)} total)",
              "=" * 72]
    lines.extend(f"  {s}" for s in room_scripts)

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover FoM areas and room scripts")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--search", help="Filter results by substring")
    args = parser.parse_args()
    run(args.game_path, search_filter=args.search)
