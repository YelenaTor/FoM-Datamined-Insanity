"""
discover_resources.py — Fields of Mistria resource node discovery tool

Enumerates tool node script targets (hoe_node, pick_node, water_node, etc.)
and resource-related GML hooks needed for EFL resource spawning.

Output: raw/resources.txt

Usage:
    python discover_resources.py --game-path "C:/path/to/FoM"
    python discover_resources.py --game-path "C:/path/to/FoM" --search chop
"""

import re
import os
import argparse

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "resources.txt")


def find_gml_discovery(game_path):
    candidates = [
        os.path.join(game_path, ".temp", "gml_discovery.txt"),
        os.path.join(game_path, "gml_discovery.txt"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        f"gml_discovery.txt not found under {game_path!r}.\n"
        "Generate it by running a YYTK script dump against FieldsOfMistria.exe."
    )


def load_gml_scripts(game_path):
    scripts = []
    with open(find_gml_discovery(game_path), encoding="utf-8") as f:
        for line in f:
            m = re.search(r"gml_Script_\S+", line)
            if m:
                scripts.append(m.group(0))
    return sorted(set(scripts))


TOOL_PATTERNS = {
    "hoe":    ["hoe_node", "can_hoe_node"],
    "pick":   ["pick_node", "can_pick_node", "pick_axe"],
    "water":  ["water_node", "can_water_node", "water_all", "water_chunk"],
    "chop":   ["chop_node", "can_chop_node"],
    "shovel": ["shovel_node", "can_shovel_node"],
    "slash":  ["slash_node"],
    "plant":  ["plant_seed", "plant_grass", "plant_sapling", "can_plant"],
    "spawn":  ["spawn_resource", "spawn_node", "register_node", "item_node",
               "create_node_prototypes", "find_node"],
    "respawn": ["bush_node_new_day", "crop_node_new_day", "tree_node_new_day", "new_day"],
}


def categorize_scripts(all_scripts):
    categorized = {cat: [] for cat in TOOL_PATTERNS}
    categorized["other_node"] = []
    seen = set()
    for cat, patterns in TOOL_PATTERNS.items():
        for s in all_scripts:
            if any(p in s.lower() for p in patterns) and s not in seen:
                categorized[cat].append(s)
                seen.add(s)
    for s in all_scripts:
        if "node" in s.lower() and s not in seen:
            categorized["other_node"].append(s)
    return categorized


def run(game_path, search_filter=None):
    all_scripts = load_gml_scripts(game_path)
    categorized = categorize_scripts(all_scripts)

    confirmed = [
        "gml_Script_hoe_node", "gml_Script_pick_node", "gml_Script_water_node",
        "gml_Script_chop_node", "gml_Script_shovel_node",
    ]

    lines = ["=" * 72, "FIELDS OF MISTRIA — RESOURCE NODE SCRIPTS", "=" * 72, "",
             "  KEY HOOK TARGETS FOR EFL RESOURCE SPAWNING:", ""]
    for s in confirmed:
        status = "CONFIRMED IN DATA.WIN" if s in all_scripts else "NOT FOUND — verify name"
        lines.append(f"  {s:55s}  [{status}]")
    lines.append("")

    for cat in TOOL_PATTERNS:
        scripts = categorized[cat]
        if search_filter:
            scripts = [s for s in scripts if search_filter.lower() in s.lower()]
        if not scripts:
            continue
        lines.append(f"  --- {cat.upper()} ({len(scripts)}) ---")
        lines.extend(f"  {s}" for s in scripts)
        lines.append("")

    other = categorized["other_node"]
    if search_filter:
        other = [s for s in other if search_filter.lower() in s.lower()]
    if other:
        lines.append(f"  --- OTHER NODE SCRIPTS ({len(other)}) ---")
        lines.extend(f"  {s}" for s in other)

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover FoM resource node scripts")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--search", help="Filter by substring")
    args = parser.parse_args()
    run(args.game_path, search_filter=args.search)
