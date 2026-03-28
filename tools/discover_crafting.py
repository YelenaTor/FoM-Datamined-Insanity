"""
discover_crafting.py — Fields of Mistria crafting station discovery tool

Enumerates crafting station objects, script targets for recipe injection,
and the spawn_crafting_menu hook.

Output: raw/crafting.txt

Usage:
    python discover_crafting.py --game-path "C:/path/to/FoM"
    python discover_crafting.py --game-path "C:/path/to/FoM" --search recipe
"""

import json
import re
import os
import argparse

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "crafting.txt")


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


def discover_crafting_scripts(all_scripts):
    categories = {
        "menu":    ["crafting_menu", "spawn_crafting_menu", "load_crafting_ui",
                    "load_cooking_ui", "check_item_craftable"],
        "recipe":  ["recipe", "unlock_recipe", "has_recipe", "inject_recipe",
                    "inventory_satisfies_recipe", "ari_has_recipe"],
        "station": ["crafting_table", "stable_crafting", "farm_expansion"],
        "context": ["recipe_context", "string_to_recipe", "recipe_component"],
    }
    result = {cat: [] for cat in categories}
    result["other"] = []
    seen = set()
    for cat, patterns in categories.items():
        for s in all_scripts:
            if any(p in s.lower() for p in patterns) and s not in seen:
                result[cat].append(s)
                seen.add(s)
    for s in all_scripts:
        if ("craft" in s.lower() or "recipe" in s.lower()) and s not in seen:
            result["other"].append(s)
    return result


def run(game_path, search_filter=None):
    data = load_fiddle(game_path)
    all_scripts = load_gml_scripts(game_path)
    crafting_scripts = discover_crafting_scripts(all_scripts)

    priority = [
        "gml_Script_spawn_crafting_menu",
        "gml_Script_CraftingMenu",
        "gml_Script_load_crafting_ui_data",
        "gml_Script_check_item_craftable@CraftingMenu@CraftingMenu",
        "gml_Script_unlock_recipe@Ari@Ari",
        "gml_Script_ari_has_recipe_anywhere",
    ]

    lines = ["=" * 72, "FIELDS OF MISTRIA — CRAFTING STATIONS & RECIPE SCRIPTS", "=" * 72, "",
             "  KEY TARGETS FOR EFL CRAFTING STATION HOOK:", ""]
    for s in priority:
        status = "IN DATA.WIN" if s in all_scripts else "not found"
        lines.append(f"  {s:60s} [{status}]")
    lines.append("")

    for cat, scripts in crafting_scripts.items():
        if search_filter:
            scripts = [s for s in scripts if search_filter.lower() in s.lower()]
        if not scripts:
            continue
        lines.append(f"  --- {cat.upper()} SCRIPTS ({len(scripts)}) ---")
        lines.extend(f"  {s}" for s in scripts)
        lines.append("")

    crafting_fiddle = {k: v for k, v in data.items()
                       if any(seg in k for seg in ["recipe", "craft", "station"])}
    if search_filter:
        crafting_fiddle = {k: v for k, v in crafting_fiddle.items()
                           if search_filter.lower() in k.lower()}
    lines += ["=" * 72, f"CRAFTING FIDDLE ENTRIES ({len(crafting_fiddle)} total)", "=" * 72]
    for k in sorted(crafting_fiddle)[:100]:
        lines.append(f"  {k} = {crafting_fiddle[k]}")
    if len(crafting_fiddle) > 100:
        lines.append(f"  ... and {len(crafting_fiddle) - 100} more (use --search to narrow)")

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover FoM crafting scripts and stations")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--search", help="Filter by substring")
    args = parser.parse_args()
    run(args.game_path, search_filter=args.search)
