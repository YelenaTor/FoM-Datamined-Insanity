"""
discover_scripts.py — Fields of Mistria full GML script target enumeration

Extracts ALL named gml_Script_* entries from gml_discovery.txt and
categorizes them by area. Primary prerequisite for Script Injection (Option B).

Output: raw/scripts.txt

Usage:
    python discover_scripts.py --game-path "C:/path/to/FoM"
    python discover_scripts.py --game-path "C:/path/to/FoM" --area crafting
    python discover_scripts.py --game-path "C:/path/to/FoM" --search story_start
    python discover_scripts.py --game-path "C:/path/to/FoM" --top-level-only
    python discover_scripts.py --game-path "C:/path/to/FoM" --list-areas
"""

import re
import os
import argparse
from collections import defaultdict

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "scripts.txt")


def find_gml_discovery(game_path):
    candidates = [
        os.path.join(game_path, ".temp", "gml_discovery.txt"),
        os.path.join(game_path, "gml_discovery.txt"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"gml_discovery.txt not found under {game_path!r}")


def parse_gml_discovery(game_path):
    scripts = []
    current = None
    with open(find_gml_discovery(game_path), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            m = re.match(r"^SCRIPT:\s+(\S+)", line)
            if m:
                if current:
                    scripts.append(current)
                current = {"name": m.group(1), "type": "", "area": "", "related": []}
                continue
            if current is None:
                continue
            m = re.match(r"^\s+Type:\s+(.+)", line)
            if m:
                current["type"] = m.group(1).strip()
                continue
            m = re.match(r"^\s+Area:\s+(.+)", line)
            if m:
                current["area"] = m.group(1).strip()
                continue
            m = re.match(r"^\s+-\s+(gml_Script_\S+)", line)
            if m:
                current["related"].append(m.group(1))
    if current:
        scripts.append(current)

    name_to_area = {}
    for s in scripts:
        parent_name = f"gml_Script_{s['name']}" if not s["name"].startswith("gml_Script_") else s["name"]
        name_to_area[parent_name] = s["area"]
        for r in s["related"]:
            if r not in name_to_area:
                name_to_area[r] = s["area"]
    return scripts, name_to_area


def is_top_level(script_name):
    return "@" not in script_name


def run(game_path, area_filter=None, search_filter=None, top_level_only=False, list_areas=False):
    scripts, name_to_area = parse_gml_discovery(game_path)
    areas = defaultdict(list)
    for name, area in sorted(name_to_area.items()):
        areas[area or "Uncategorized"].append(name)

    if list_areas:
        print("All areas in gml_discovery.txt:\n")
        for area in sorted(areas):
            print(f"  {area} ({len(areas[area])} scripts)")
        return

    expected_hooks = [
        ("on_npc_tick",        ["npcs_on_step", "npc_is_unlocked"]),
        ("on_npc_interact",    ["talk_to", "interact_with"]),
        ("on_player_update",   ["AriFsm", "ari"]),
        ("on_area_enter",      ["room_start", "initialize_on_room_start", "npcs_on_room_start"]),
        ("on_area_exit",       ["roomtransition", "obj_roomtransition"]),
        ("on_resource_gather", ["hoe_node", "pick_node", "water_node", "chop_node"]),
        ("on_quest_update",    ["fulfill_quest", "assert_quest_active", "turn_in_quest"]),
        ("on_trigger_fire",    ["story_start", "goto_scene_trigger", "execute"]),
        ("on_save",            ["serialize"]),
        ("on_load",            ["deserialize"]),
    ]

    all_script_names = set(name_to_area.keys())
    lines = ["=" * 72, "FIELDS OF MISTRIA — FULL GML SCRIPT CATALOG", "=" * 72,
             f"Total unique script names: {len(name_to_area)}", f"Areas: {len(areas)}\n",
             "  PRIMARY OPTION B INJECTION TARGETS:", ""]
    for binding, candidates in expected_hooks:
        matches = [s for s in all_script_names if any(c in s.lower() for c in candidates)]
        lines.append(f"  {binding}:")
        if matches:
            for m in sorted(matches)[:5]:
                lines.append(f"    -> {m}")
            if len(matches) > 5:
                lines.append(f"    -> ...and {len(matches)-5} more")
        else:
            lines.append("    -> [no candidates found]")
        lines.append("")

    lines += ["=" * 72, "FULL SCRIPT LIST BY AREA", "=" * 72]
    for area in sorted(areas):
        if area_filter and area_filter.lower() not in area.lower():
            continue
        scripts_in_area = sorted(areas[area])
        if top_level_only:
            scripts_in_area = [s for s in scripts_in_area if is_top_level(s)]
        if search_filter:
            scripts_in_area = [s for s in scripts_in_area if search_filter.lower() in s.lower()]
        if not scripts_in_area:
            continue
        lines.append(f"\n  --- {area} ({len(scripts_in_area)}) ---")
        lines.extend(f"  {s}" for s in scripts_in_area)

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enumerate all GML script targets")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--area", help="Filter by area name substring")
    parser.add_argument("--search", help="Filter by script name substring")
    parser.add_argument("--top-level-only", action="store_true",
                        help="Show only simple (non-nested) script names")
    parser.add_argument("--list-areas", action="store_true", help="List all areas with counts")
    args = parser.parse_args()
    run(args.game_path, area_filter=args.area, search_filter=args.search,
        top_level_only=args.top_level_only, list_areas=args.list_areas)
