# GMS2 YYC Binary Format (data.win)

> Verified: FoM 0.14.x — Ghidra + Python binary parser (2026-03-28)

Fields of Mistria ships as a GameMaker Studio 2 YYC (YoYo Compiler) Windows build. The game data is stored in `data.win` in the FORM chunk container format.

## FORM chunk layout

`data.win` is a single FORM chunk containing sequential named sub-chunks:

```
FORM
├── GEN8   — general metadata (game name, GUID, build info)
├── OPTN   — options
├── LANG   — language configuration
├── EXTN   — extensions
├── SOND   — sounds
├── AGRP   — audio groups
├── SPRT   — sprites
├── BGND   — backgrounds
├── PATH   — paths
├── SCPT   — script entries (name → code index mapping)
├── GLOB   — globals
├── SHDR   — shaders
├── FONT   — fonts
├── TMLN   — timelines
├── OBJT   — object definitions (254 total in FoM 0.14.x)
├── ACRV   — animation curves
├── SEQN   — sequences
├── TAGS   — tags
├── ROOM   — room definitions (214 rooms in FoM 0.14.x)
├── DAFL   — data files
├── EMBI   — embedded images
├── TPAG   — texture page entries
├── CODE   — compiled GML bytecode
├── VARI   — variable definitions
├── FUNC   — function definitions
├── STRG   — string table
├── TXTR   — texture data
└── AUDO   — audio data
```

Each chunk header: 4-byte ASCII name + 4-byte `uint32` size.

## STRG chunk

The string table stores all string literals. Layout:

```
STRG header (8 bytes: "STRG" + chunk size)
  uint32 count
  uint32 offsets[count]   <- each offset points to the 4-byte length prefix of a string
  ...
  for each string:
    uint32 length         <- byte length (NOT including null terminator)
    char   data[length]
    byte   0x00           <- null terminator
```

**Critical offset quirk:** Each entry in the offset table points to the **4-byte length prefix**. The actual string data starts 4 bytes after the offset. OBJT `name_ptr` values point **directly to the string data** (i.e. `strg_base + offset + 4`).

When building a string lookup dict, key both `off` (→ length) and `off + 4` (→ string data), otherwise OBJT name lookups will return `<idx>` for every object.

## OBJT chunk

Object definitions. 254 objects total in FoM 0.14.x.

```
OBJT header
  uint32 count
  uint32 offsets[count]
  for each object:
    uint32 name_ptr       <- points into STRG data (NOT length prefix — see above)
    uint32 sprite_index
    ...
```

**Key finding:** There is no `obj_iron_rock`, `obj_copper_ore`, or any ore-type object in OBJT. Resource nodes are **not** GameMaker object instances. The only visual host is `obj_node_renderer`.

## ROOM chunk

Room definitions. 214 rooms in FoM 0.14.x.

```
ROOM header
  uint32 count
  for each room:
    uint32 name_ptr
    uint32 caption_ptr
    uint32 width, height
    uint32 speed
    ...
    uint32 instance_count
    for each instance:
      float x, y
      uint32 object_index
      uint32 instance_id
      ...
```

**Key finding:** No pre-placed resource node instances exist in any ROOM chunk. Scanning all 214 rooms for object names matching ore/node patterns returns 0 results. FoM places resource nodes entirely at runtime via the Grid/Anchor/Node system.

## GML script names

All script names (2340 total in FoM 0.14.x) follow the pattern:
```
gml_Script_<name>
gml_Script_<name>@<ClassName>@<ClassName>    # method on a struct/class
gml_Script_anon@<offset>@<enclosing>         # anonymous function
```

The `@` separator encodes the method chain. For hooks, target the short form where possible (e.g. `gml_Script_pick_node`, not the `anon@` variants).

See [script-catalog.md](../scripts/script-catalog.md) for the full list.
