# Area / Location IDs

> Source: `__fiddle__.json` key scan under `locations/`, FoM 0.14.x (2026-03-28)
> **79 locations** total.

Format: `location_id  →  name_key  music_path`

## All locations

```
abandoned_mines
abandoned_pit
adelines_bedroom
adelines_office
aldaria
balors_room
bathhouse               name="locations/bathhouse/name"         music="Music/Location Tracks/Bathhouse"
bathhouse_bath                                                  music="Music/Location Tracks/Bathhouse"
bathhouse_bedroom                                               music="Music/Location Tracks/Bathhouse"
bathhouse_change_room                                           music="Music/Location Tracks/Bathhouse"
beach                   name="locations/beach/name"
beach_secret            name="locations/beach_secret/name"
blacksmith_room_left                                            music="Music/Location Tracks/Blacksmith"
blacksmith_room_right                                           music="Music/Location Tracks/Blacksmith"
blacksmith_store        name="locations/blacksmith_store/name"  music="Music/Location Tracks/Blacksmith"
caldarus_house          name="locations/caldarus_house/name"    music="Music/Location Tracks/Deep Woods"
celines_room            name="locations/celines_room/name"
clinic_b1
clinic_f1               name="locations/clinic_f1/name"         music="Music/Location Tracks/Clinic"
clinic_f2                                                       music="Music/Location Tracks/Clinic"
deep_woods              name="locations/deep_woods/name"        music="Music/Location Tracks/Deep Woods"
default                 name="locations/default/name"           music="<n/a>"
dells_bedroom                                                   music="Music/Location Tracks/General Store"
dragonsworn_glade       name="locations/dragonsworn_glade/name" music="Music/Location Tracks/Deep Woods"
dungeon                                                         music="Music/Location Tracks/MinesEntry"
earth_seal              name="locations/earth_seal/name"        music="{'day': 'Music/Events/TheSeal', ...}"
eastern_road            name="locations/eastern_road/name"
eilands_bedroom
eilands_office
elsies_bedroom
errols_bedroom          name="locations/errols_bedroom/name"
farm
fire_seal               name="locations/fire_seal/name"         music="{'day': 'Music/Events/TheSeal', ...}"
general_store_home                                              music="Music/Location Tracks/General Store"
general_store_store     name="locations/general_store_store/name" music="Music/Location Tracks/General Store"
haydens_bedroom
haydens_farm            name="locations/haydens_farm/name"
haydens_house           name="locations/haydens_house/name"
holt_and_noras_bedroom                                          music="Music/Location Tracks/General Store"
inn                     name="locations/inn/name"               music="Music/Location Tracks/InnLessBusy"
jo_and_hemlocks_room
landens_house_f1        name="locations/landens_house_f1/name"  music="Music/Location Tracks/Carpenter"
landens_house_f2                                                music="Music/Location Tracks/Carpenter"
large_barn
large_coop
large_greenhouse
lucs_room
manor_house_dining_room
manor_house_entry       name="locations/manor_house_entry/name"
maples_room
medium_barn
medium_coop
mill                    name="locations/mill/name"
mines_entry             name="locations/mines_entry/name"       music="{'day': 'Music/Location Tracks/MinesEntry', ...}"
museum_entry            name="locations/museum_entry/name"
narrows                 name="locations/narrows/name"
narrows_secret          name="locations/narrows_secret/name"
player_home             name="locations/player_home/name"       music="{'day': 'Music/Location Tracks/Player Home/Day', ...}"
player_home_east        name="locations/player_home_east/name"
player_home_north       name="locations/player_home_north/name"
player_home_upper_central
player_home_upper_east
player_home_upper_west
player_home_west
priestess_quarters      name="locations/priestess_quarters/name"
reinas_room
ruins_seal              name="locations/ruins_seal/name"        music="{'day': 'Music/Events/TheSeal', ...}"
seridias_chamber                                                music="{'day': 'Music/Location Tracks/TheFinalSeal', ...}"
seridias_house          name="locations/seridias_house/name"    music="Music/Npc Tracks/Seridia"
seridias_house_back                                             music="Music/Location Tracks/SeridiaVoidRoom"
small_barn
small_coop
small_greenhouse
summit                  name="locations/summit/name"
terithias_house         name="locations/terithias_house/name"
town                    name="locations/town/name"
void_seal               name="locations/void_seal/name"         music="Music/Location Tracks/VoidSeal"
water_seal              name="locations/water_seal/name"        music="{'day': 'Music/Events/TheSeal', ...}"
western_ruins           name="locations/western_ruins/name"
```

## Room transition scripts

Key room-start GML scripts (37 total):

```
gml_Script_initialize_on_room_start@Grid@Grid
gml_Script_npcs_on_room_start
gml_Script_on_room_start@Anchor@Anchor
gml_Script_on_room_start@DungeonRunner@DungeonRunner
gml_Script_festival_room_start
gml_Script_spawn_bugs_on_room_start
gml_Script_npas_room_start
gml_Script_goto_gm_room
gml_Script_pet_on_room_start
```

Run `tools/discover_areas.py --game-path <path>` for the full list.
