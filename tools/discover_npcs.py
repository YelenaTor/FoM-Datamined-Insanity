"""
discover_npcs.py — Fields of Mistria NPC discovery tool

Enumerates all NPC names, portrait emotions, and GML script targets
for NPC tick/interact hooks.

Output: raw/npcs.txt

Usage:
    python discover_npcs.py --game-path "C:/path/to/FoM"
    python discover_npcs.py --game-path "C:/path/to/FoM" --npc celine
    python discover_npcs.py --game-path "C:/path/to/FoM" --portraits-only
"""

import json
import re
import os
import argparse
from collections import defaultdict

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "raw", "npcs.txt")


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


def discover_npcs(data):
    npcs = defaultdict(lambda: {"portraits": set(), "fields": {}})
    for k, v in data.items():
        if not k.startswith("npcs/"):
            continue
        parts = k.split("/")
        if len(parts) < 2:
            continue
        npc_id = parts[1]
        if len(parts) >= 4 and parts[2] == "portraits":
            npcs[npc_id]["portraits"].add(parts[3])
        elif len(parts) == 3:
            npcs[npc_id]["fields"][parts[2]] = v
    return npcs


def discover_npc_scripts(all_scripts):
    patterns = ["npc", "spawn_npc", "give_gift", "heart", "talk_to", "interact"]
    return [s for s in all_scripts if any(p in s.lower() for p in patterns)]


def run(game_path, npc_filter=None, portraits_only=False):
    data = load_fiddle(game_path)
    all_scripts = load_gml_scripts(game_path)

    npcs = discover_npcs(data)
    npc_scripts = discover_npc_scripts(all_scripts)

    if npc_filter:
        npcs = {k: v for k, v in npcs.items() if npc_filter.lower() in k.lower()}
        npc_scripts = [s for s in npc_scripts if npc_filter.lower() in s.lower()]

    lines = ["=" * 72, "FIELDS OF MISTRIA — NPCs", "=" * 72,
             f"Total NPCs with fiddle data: {len(npcs)}\n"]

    for npc_id in sorted(npcs):
        info = npcs[npc_id]
        portraits = sorted(info["portraits"])
        fields = info["fields"]
        lines.append(f"  {npc_id}")
        for fk, fv in sorted(fields.items()):
            if isinstance(fv, (str, int, float, bool)):
                lines.append(f"    {fk}: {fv}")
            elif isinstance(fv, list) and all(isinstance(x, str) for x in fv):
                lines.append(f"    {fk}: {', '.join(fv)}")
            else:
                lines.append(f"    {fk}: [complex — use query_fiddle.py --prefix npcs/{npc_id}/{fk}]")
        if portraits:
            lines.append(f"    portraits ({len(portraits)}): {', '.join(portraits)}")
        lines.append("")

    if not portraits_only:
        lines += ["=" * 72, f"NPC LIFECYCLE GML SCRIPTS ({len(npc_scripts)} total)", "=" * 72,
                  "  Key hook targets for on_npc_tick / on_npc_interact:\n"]
        priority = ["spawn_npc", "give_gift", "add_heart_points", "npc_id_to_string",
                    "string_to_npc_id", "npc_is_unlocked", "npcs_on_step", "npcs_on_room_start",
                    "talk_to", "interact_with"]
        seen = set()
        for p in priority:
            for s in npc_scripts:
                if p in s.lower() and s not in seen:
                    lines.append(f"  *** {s}")
                    seen.add(s)
        lines += ["", "  All NPC scripts:"]
        lines.extend(f"  {s}" for s in npc_scripts)

    output = "\n".join(lines)
    print(output)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover FoM NPC data and hook targets")
    parser.add_argument("--game-path", required=True, help="Path to FoM game folder")
    parser.add_argument("--npc", help="Filter by NPC name substring")
    parser.add_argument("--portraits-only", action="store_true", help="Skip GML scripts section")
    args = parser.parse_args()
    run(args.game_path, npc_filter=args.npc, portraits_only=args.portraits_only)
