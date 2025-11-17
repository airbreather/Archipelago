from BaseClasses import Item, Region, Location, ItemClassification
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from .options import WorldOfWarcraftOptions
from .ExportLua import export_lua_mappings
from .ExportLuaConfig import export_lua_config
import os
import json
import random
from pathlib import Path
import importlib.resources as pkg_resources

# Constants
CLASS_VALUE_TO_NAME = {
    0: "Warrior",
    1: "Death Knight",
    2: "Paladin",
    3: "Hunter",
    4: "Shaman",
    5: "Rogue",
    6: "Druid",
    7: "Priest",
    8: "Warlock",
    9: "Mage",
    # 10: "Random"  # optional
}

RACE_VALUE_TO_NAME = {
    0: "Human",
    1: "Dwarf",
    2: "Gnome",
    3: "Night Elf",
    4: "Draenei",
    5: "Orc",
    6: "Troll",
    7: "Tauren",
    8: "Forsaken",
    9: "Blood Elf",
    # 10: "Random"  # optional
}

RACE_TO_STARTING_ZONE = {
    "Human": "Elwynn Forest",
    "Dwarf": "Dun Morogh",
    "Gnome": "Dun Morogh",
    "Night Elf": "Teldrassil",
    "Draenei": "Azuremyst Isle",
    "Orc": "Durotar",
    "Troll": "Durotar",
    "Tauren": "Mulgore",
    "Undead": "Tirisfal Glades",
    "Blood Elf": "Eversong Woods",
}

GOAL_VALUE_TO_LEVEL = {
    0: 10,
    1: 20,
    2: 30,
    3: 40,
    4: 50,
    5: 60,
    6: 70,
    7: 80
}

FACTION_GROUP_TO_RACES = {
    1: ["Human", "Dwarf", "Gnome", "Night Elf", "Draenei"],
    2: ["Human", "Dwarf", "Gnome", "Night Elf", "Draenei"],
    3: ["Human", "Dwarf", "Gnome", "Night Elf", "Draenei"],
    4: ["Orc", "Troll", "Tauren", "Forsaken", "Blood Elf"],
    5: ["Orc", "Troll", "Tauren", "Forsaken", "Blood Elf"],
    8: ["Human", "Dwarf", "Gnome", "Night Elf", "Draenei"],
}

PREPENDS = {
    # Shared ids
    "Base": 10,
    "Items": 11,
    "Quests": 12,
    "Zones": 13,
    "Levels": 14,
    "Spells": 15,
    # Class specific spells:
    "Warrior": 20,
    "DeathKnight": 21,
    "Paladin": 22,
    "Hunter": 23,
    "Shaman": 24,
    "Rogue": 25,
    "Druid": 26, 
    "Priest": 27,
    "Warlock": 28,
    "Mage": 29
}

FREE_LEVELS = 5

def preload_wow_metadata():
    quests_pkg = f"{__package__}.quests"
    spells_pkg = f"{__package__}.spells"
    wowap_file = pkg_resources.files(__package__).joinpath("wowap.json")
    skills_file = pkg_resources.files(__package__).joinpath("Skills.json")
    locs = {}
    items = {
        "Victory": 101,
        "Gold": 102,
        "Progressive Level": 103,
        "Progressive Riding": 104,
        "Random Buff": 105,
        "Random Debuff": 106,
        "Random Bag": 107,
    }
    loc_id = 1
    item_id = 8
    quests = {}
    spells = {}
    all_zones = {}
    spells_by_class = {}

    with wowap_file.open("r", encoding="utf-8") as f:
        zones = json.load(f)
        for zone_name, zdata in zones.items():
            if zdata.get("min_level", 0) < 80:
                items[f"Unlock {zone_name}"] = int(f"{PREPENDS['Zones']}{zdata.get('id', 0)}")
            if zone_name not in all_zones:
                all_zones[zone_name] = zones[zone_name]


    for level in range(2, 81):
        locs[f"Level {level}"] = int(f"{PREPENDS['Levels']}{level}")

    for entry in pkg_resources.files(__package__).joinpath("quests").iterdir():
        if not entry.name.endswith(".json"):
            continue
        with entry.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for name in data.keys():
            if name not in locs:
                locs[name] = int(f"{PREPENDS['Quests']}{data[name]['ID']}")
            if name not in quests:
                quests[name] = data[name]


    for entry in pkg_resources.files(__package__).joinpath("spells").iterdir():
        if not entry.name.endswith(".json"):
            continue
        className = entry.name.replace(".json", "").replace(" ", "")
        with entry.open("r", encoding="utf-8") as f:
            data = json.load(f)

        spells_by_class[className] = dict(data)

        for name in data.keys():
            if name not in locs:
                locs[name] = int(f"{PREPENDS[className]}{data[name]['id']}")
            if name not in items:
                items[name] = int(f"{PREPENDS[className]}{data[name]['id']}")
            if name not in spells:
                spells[name] = data[name]


    with skills_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
        for className in data:
            for skill in data[className].keys():
                prefix = PREPENDS.get(className, PREPENDS["Spells"])
                if skill not in locs:
                    locs[name] = int(f"{prefix}{data[className][skill]['id']}")
                if skill not in items:
                    items[name] = int(f"{prefix}{data[className][skill]['id']}")
                if name not in spells:
                    spells[name] = data[name]
                if className != "Riding" and skill not in spells_by_class[className]:
                    spells_by_class[className][skill] = data[className][skill]

    print(f"[WOW] Preloaded {len(locs)} locations and {len(items)} items.")
    return locs, items, quests, spells, all_zones, spells_by_class

# Static preload before class
PRELOADED_LOCS, PRELOADED_ITEMS, ALL_QUESTS, ALL_SPELLS, ALL_ZONES, SPELLS_MAPPING = preload_wow_metadata()

class WowWorld(World):
    """World of Warcraft progressive-level world with zones, quests, and spells."""

    game = "World of Warcraft"
    topology_present = False
    options_dataclass = WorldOfWarcraftOptions

    item_name_to_id = PRELOADED_ITEMS
    location_name_to_id = PRELOADED_LOCS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make sure each player has isolated copies of world data
        self.ZONES = {}
        self.QUESTS = {}
        self.SPELLS = {}
        self.ALL_QUESTS = dict(ALL_QUESTS)
        self.ALL_SPELLS = dict(ALL_SPELLS)
        self.ALL_ZONES = dict(ALL_ZONES)
        self.SPELLS_MAPPING = dict(SPELLS_MAPPING)
        self.zone_quest_map = {}
    # --------------------------------------------------------------------------
    # Item Definitions and Location Map
    # --------------------------------------------------------------------------
        self.location_name_to_id = dict(PRELOADED_LOCS)
        self.item_name_to_id = dict(PRELOADED_ITEMS)

    # --------------------------------------------------------------------------
    # Utilities
    # --------------------------------------------------------------------------
    def create_race_and_class(self, playerString):
        combo = playerString.split("/")
        return combo[0], combo[1]

    def prune_inaccessible_quests(self):
        """
        Remove quests that are not part of any feasible prerequisite chain.
        A quest is kept only if:
          - its min_level <= self.player_max_level, and
          - all quests in its 'requires' list can also be kept.
        This performs an iterative fixed-point computation; cyclic or missing prereqs get pruned.
        """
        # Working copies
        all_quests = dict(self.QUESTS)          # quest_name -> { 'zone':..., 'min_level':..., ... }
        zones = dict(self.ZONES)                # zone_name -> { 'min_level':..., 'quests': { ... } }

        # Pre-filter: drop quests with min_level > player_max_level
        filtered = {q: data for q, data in all_quests.items() if data.get("min_level", 1) <= self.player_max_level}

        # Build requires map (normalize missing 'requires' -> empty list)
        requires_map = {}
        for q, d in filtered.items():
            requires_map[q] = list(d.get("requires", [])) if d.get("requires") else []

        # Iterative inclusion: start with quests that have no requirements
        included = set(q for q, reqs in requires_map.items() if not reqs)

        changed = True
        while changed:
            changed = False
            for q, reqs in requires_map.items():
                if q in included:
                    continue
                # All requirements must exist in filtered (else this quest cannot be satisfied)
                if any(r not in requires_map for r in reqs):
                    # requirement missing (filtered out by level or never present) -> cannot include q
                    continue
                # If all requirements are already included, include this quest
                if all(r in included for r in reqs):
                    included.add(q)
                    changed = True

        # Now included contains the closure of reachable quests
        removed_quests = set(all_quests.keys()) - included

        # Remove them from self.QUESTS and zones mapping
        for q in removed_quests:
            if q in self.QUESTS:
                del self.QUESTS[q]

        # Also clean per-zone quest lists and drop empty zones
        removed_zones = []
        for zone_name, zone_data in list(self.ZONES.items()):
            # zone_data["quests"] is dict(quest_name -> quest_data)
            zone_quests = zone_data.get("quests", {})
            # Keep only quests in `included`
            new_zone_quests = {qn: qd for qn, qd in zone_quests.items() if qn in included}
            if not new_zone_quests:
                # drop zone entirely
                del self.ZONES[zone_name]
                removed_zones.append(zone_name)
            else:
                self.ZONES[zone_name]["quests"] = new_zone_quests

        # Logging
        kept = len(included)
        removed_q_count = len(removed_quests)
        removed_z_count = len(removed_zones)
        print(f"[WOW] Pruned quests: kept={kept}, removed_quests={removed_q_count}, removed_zones={removed_z_count}")

        # Return stats if you want to inspect
        return {"kept": kept, "removed_quests": removed_quests, "removed_zones": removed_zones}


    def load_quests_from_json(self):
        """Load all quests from zones defined in wowap.json where min_level < max."""


        try:
            with pkg_resources.files(__package__).joinpath("wowap.json").open("r", encoding="utf-8") as f:
                wowap_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("wowap.json not found inside wow.apworld (make sure it’s in the wow/ folder)")

        all_quests = {}
        zones = {}

        for character in self.allChars:
            seen_zones = []
            connecting_level_appropriate_zones = []

            def map_connections(zone_name):
                zone = wowap_data[zone_name]
                if zone_name in seen_zones:
                    return
                if zone.get("min_level", 0) < self.player_max_level:
                    seen_zones.append(zone_name)
                    connecting_level_appropriate_zones.append(zone_name) 
                    for subzone in zone.get("connections", []):
                        map_connections(subzone)

            map_connections(character["starting_zone"])
            for zone_name, zone_data in wowap_data.items():
                if zone_name not in connecting_level_appropriate_zones:
                    continue

                min_level = zone_data.get("min_level", 0)
                if min_level >= self.player_max_level:
                    continue  # skip higher-level zones

                try:
                    with pkg_resources.files(__package__).joinpath("quests", f"{zone_name}.json").open("r", encoding="utf-8") as zf:
                        zone_quests = json.load(zf)
                except json.JSONDecodeError as e:
                    print(f"[WOW] Failed to parse quests/{zone_name}.json: {e}")
                    continue

                # Filter and add quests
                quest_dict = {}
                for quest_name, quest_data in zone_quests.items():
                    min_quest_level = quest_data.get("MinLevel", 1)
                    seasonalEvent = quest_data.get("seasonalEvent", 0)
                    races = quest_data.get("AllowableRaces", [])
                    classes = quest_data.get("AllowableClasses", [])
                    quest_id = quest_data.get("ID", 0)
                    reward_spell = quest_data.get("RewardSpell", 0) # Tame Beast, for example
                    faction_group = quest_data.get("FactionGroup", 0)
                    profession = quest_data.get("Profession", 0)
                    rep1 = quest_data.get("RequiredFactionValue1", 0)
                    rep2 = quest_data.get("RequiredFactionValue2", 0)
                    quest_zones = quest_data.get("zone", 0)
                    requires = quest_data.get("requires", 0)

                    if min_quest_level > self.player_max_level:
                        continue
                    if seasonalEvent:
                        continue
                    if races != [] and character["race"] not in races:
                        continue
                    if faction_group and character["race"] not in FACTION_GROUP_TO_RACES[faction_group]:
                        continue
                    if classes != [] and character["class"] not in classes:
                        continue
                    if quest_id == 3861: # CLUCK! is behaving oddly
                        continue
                    if  profession and profession not in self.professions:
                        continue
                    if rep1 or rep2:
                        continue
                    # if all zones not in connecting level appropriate zones - this excludes many seasonal event quests
                    all_zones_allowed = True
                    for zone in quest_zones:
                        if zone not in connecting_level_appropriate_zones:
                            all_zones_allowed = False
                    if not all_zones_allowed:
                        continue

                    quest_dict[quest_name] = {
                        "zones": quest_zones,
                        "requires": requires,
                        "min_level": min_quest_level
                        }
                    all_quests[quest_name] = {
                        "min_level": min_quest_level,
                        "zone": zone_name,
                        "quest_id": quest_id,
                        "reward_spell": reward_spell,
                        "classes": classes,
                        }

                zones[zone_name] = {
                    "min_level": min_level,
                    "max_level": zone_data.get("max_level", min_level + 10),
                    "id": zone_data.get("id", 0),
                    "connections": zone_data.get("connections", []),
                    "quests": (zones.get(zone_name, {}).get("quests", {}) | quest_dict)
                }

        print(f"[WOW] Loaded {len(all_quests)} quests from {len(zones)} zones (min_level < {self.player_max_level}).")
        return all_quests, zones

    def load_spells_from_json(self):
        """Load spells and skills from packaged JSON files (zip-safe)."""

        spells_pkg = f"{__package__}.spells"
        spells = {}

        # --- Load skills and merge for this class ---
        try:
            with pkg_resources.files(__package__).joinpath("Skills.json").open("r", encoding="utf-8") as f:
                skills_data = json.load(f)

            # Class-specific skills

            for character in self.allChars:

                class_skills = skills_data.get(character["class"], {})
                for skill_name, skill_data in class_skills.items():
                    level = skill_data.get("Level", 1)
                    skill_id = skill_data.get("id", 0)
                    cost = skill_data.get("money_cost", 0)

                    if level > self.player_max_level:
                        continue

                    spells[skill_name] = {
                        "level": level,
                        "spell_id": skill_id,
                        "important": False,
                        "cost": cost,
                    }

                # Riding skills (shared)
                riding_skills = skills_data.get("Riding", {})
                for skill_name, skill_data in riding_skills.items():
                    level = skill_data.get("Level", 1)
                    skill_id = skill_data.get("id", 0)
                    cost = skill_data.get("money_cost", 0)

                    if level > self.player_max_level:
                        continue

                    spells[skill_name] = {
                        "level": level,
                        "spell_id": skill_id,
                        "important": False,
                        "cost": cost,
                    }

        except FileNotFoundError:
            print("[WOW] Warning: Skills.json not found in package.")
        except Exception as e:
            print(f"[WOW] Failed to load Skills.json: {e}")

        print(f"[WOW] Loaded {len(spells)} total spells/skills for {character["class"]} class.")
        # --- Load spells for this class ---
        for character in self.allChars:
            try:
                with pkg_resources.files(__package__).joinpath("spells", f"{character["class"]}.json").open("r", encoding="utf-8") as zf:
                    data = json.load(zf)


                    for spell_name, spell_data in data.items():
                        level = spell_data.get("Level", 1)
                        spell_id = spell_data.get("id", 1)
                        races = spell_data.get("AllowableRaces", [])  # portals
                        important = spell_data.get("important", False)
                        cost = spell_data.get("money_cost", 0)

                        if level > self.player_max_level:
                            continue
                        if races and character["race"] not in races:
                            continue

                        spells[spell_name] = {
                            "level": level,
                            "spell_id": spell_id,
                            "important": important,
                            "cost": cost,
                        }


            except FileNotFoundError:
                print(f"[WOW] Warning: {character["class"]}.json not found in spells/ directory.")
            except Exception as e:
                print(f"[WOW] Failed to load {character["class"]}.json: {e}")

            print(f"[WOW] Loaded {len(spells)} spells for {character["class"]} class.")
        return spells

    # --------------------------------------------------------------------------
    # Generation
    # --------------------------------------------------------------------------
    def generate_output(self, output_directory: str) -> None:
        print(self.location_name_to_id)
        export_lua_mappings(output_directory, self.ALL_QUESTS, self.ALL_ZONES, self.ALL_SPELLS, self.item_name_to_id, self.location_name_to_id, self.SPELLS_MAPPING)
        export_lua_config(output_directory, self.options)
        return

    def generate_early(self):
        # --- Load all quests and zones dynamically ---
        print(self.options)
        self.allChars = []
        for combo in self.options.wow_race_and_class_combo:
            playerRace, playerClass = self.create_race_and_class(combo)
            character= {
                "race": playerRace,
                "class": playerClass,
                "starting_zone": RACE_TO_STARTING_ZONE.get(playerRace, "Unknown")
            }
            self.allChars.append(character)

        print(self.allChars)
        #self.player_class_name = CLASS_VALUE_TO_NAME.get(self.options.player_class.value, "Unknown")
        #self.player_race_name = RACE_VALUE_TO_NAME.get(self.options.wow_race.value, "Unknown")
        self.player_max_level = GOAL_VALUE_TO_LEVEL.get(self.options.goal)

        
        #self.starting_zone_name = RACE_TO_STARTING_ZONE.get(self.options.wow_race.value, "Unknown")
        self.professions = self.options.primary_professions.value or []
        if self.options.cooking:
            self.professions.append("Cooking")
        if self.options.first_aid:
            self.professions.append("First Aid")
        if self.options.fishing:
            self.professions.append("Fishing")
        print(self.professions)
        #print(self.player_race_name)
        #print(self.starting_zone_name)
        #print(self.player_class_name)
        print(self.player_max_level)
        print(self.options.traps.value)
        
        self.QUESTS, self.ZONES = self.load_quests_from_json()
        self.SPELLS = self.load_spells_from_json()
        self.prune_inaccessible_quests()

    def generate_basic(self):
        """Called before item/region generation to define base player state."""
        multiworld = self.multiworld
        player = self.player

        # Determine the starting zone (lowest min_level)
        for character in self.allChars:
            starting_zone = character["starting_zone"]
            starting_item = f"Unlock {starting_zone}"

            # Grant the starting zone unlock
            multiworld.push_precollected(Item(starting_item, ItemClassification.progression,
                                            self.item_name_to_id[starting_item], player))

            print(f"[WOW] Starting zone: {starting_zone} (player begins with '{starting_item}')")


    # --------------------------------------------------------------------------
    # Region Creation
    # --------------------------------------------------------------------------
    def create_regions(self):
        self.create_locations()

        multiworld = self.multiworld
        player = self.player

        # Optional: track which zones contain which quests (for reporting/debug)
        self.zone_quest_map = {}

        # --- Menu region (start) ---
        if not any(r.name == "Menu" and r.player == player for r in multiworld.regions):
            menu = Region("Menu", player, multiworld)
            multiworld.regions.append(menu)
        else:
            menu = multiworld.get_region("Menu", player)

        # --- Leveling region (for level locations) ---
        leveling_region = Region("Leveling", player, multiworld)
        multiworld.regions.append(leveling_region)
        menu.connect(leveling_region)

        for level in range(2, self.player_max_level + 1):
            loc_name = f"Level {level}"
            loc = Location(player, loc_name, self.location_name_to_id[loc_name], leveling_region)
            leveling_region.locations.append(loc)
            # Require both zone unlock item AND sufficient level tokens
            if level > FREE_LEVELS + 1:
                req_tokens = level - FREE_LEVELS
                set_rule(loc, lambda state, req=req_tokens: state.count("Progressive Level", player) >= req)

        # --- Sort zones by minimum level ---
        sorted_zones = sorted(self.ZONES.items(), key=lambda kv: kv[1]["min_level"])

        # --- Create all zone regions first ---
        zone_regions = {}
        for zone_name, zone_data in sorted_zones:
            region = Region(zone_name, player, multiworld)
            # --- Zone rule: require both the unlock item and sufficient level ---
            unlock_item = f"Unlock {zone_name}"
            min_level = zone_data["min_level"]
            req_tokens = min_level - FREE_LEVELS

            multiworld.regions.append(region)
            zone_regions[zone_name] = region

        # --- Connect Menu to the starting zone
            for character in self.allChars:
                if zone_name == character["starting_zone"]:
                    menu.connect(zone_regions[zone_name])

        # --- Now add zone-to-zone connections using wowap.json data ---
        created_connections = set()

        for zone_name, zone_data in sorted_zones:
            region = zone_regions[zone_name]
            min_level = zone_data.get("min_level", 1)
            unlock_item_name = f"Unlock {zone_name}"

            for connected_zone_name in zone_data.get("connections", []):
                if connected_zone_name not in zone_regions:
                    continue

                connection_key = tuple(sorted([zone_name, connected_zone_name]))
                if connection_key in created_connections:
                    continue
                created_connections.add(connection_key)

                target_region = zone_regions[connected_zone_name]
                target_min_level = self.ZONES[connected_zone_name]["min_level"]
                target_unlock_item = f"Unlock {connected_zone_name}"

                # Create the bidirectional connection
                region.connect(target_region)
                target_region.connect(region)

                # Fetch the exits we just made
                out_entrance = region.exits[-1]
                back_entrance = target_region.exits[-1]

                # --- Apply rules only in one direction ---
                # From lower-level zone -> higher-level zone
                if min_level <= target_min_level:
                    set_rule(
                        out_entrance,
                        lambda state, unlock_item=target_unlock_item, req_tokens=max(0, target_min_level - FREE_LEVELS):
                            state.has(unlock_item, player)
                            and state.count("Progressive Level", player) >= req_tokens
                    )
                else:
                    # Opposite direction (return path) is free
                    set_rule(out_entrance, lambda state: True)

                # Always make the reverse path free as well (safe fallback)
                set_rule(back_entrance, lambda state: True)



            # Zone-level requirement based on its min level
            min_level = zone_data["min_level"]
            if min_level > FREE_LEVELS + 1:
                req_tokens = min_level - FREE_LEVELS
                #set_rule(region, lambda state, req=req_tokens: state.count("Progressive Level", player) >= req)

            # --- Quest locations for this zone ---
            for quest_name, quest_data in zone_data["quests"].items():
                min_quest_level = quest_data.get("min_level", 1)
                if min_quest_level > self.player_max_level:
                    continue

                # Track which zones have this quest
                self.zone_quest_map.setdefault(quest_name, set()).add(zone_name)

                # Reuse or create quest location
                existing_loc = next(
                    (loc for loc in multiworld.get_locations()
                     if loc.name == quest_name and loc.player == player),
                    None
                )

                if existing_loc:
                    continue
                else:
                    loc_id = self.location_name_to_id[quest_name]
                    loc = Location(player, quest_name, loc_id, region)
                    region.locations.append(loc)
                    # ---------------------------------------------------------
                    # Level + Quest Requirement Rules
                    # ---------------------------------------------------------
                    # Quests that must be completed before this one becomes available
                    required_quests = quest_data.get("requires", [])
                    required_zones = quest_data.get("zones", [])
                    unlock_items = []
                    starting_zones = []
                    for character in self.allChars:
                        if character["starting_zone"] not in starting_zones:
                            starting_zones.append(character["starting_zone"])

                    for zone in required_zones:
                        if zone not in starting_zones:
                            unlock_items.append(f"Unlock {zone}")
                    # Only require tokens if above free level threshold
                    if min_quest_level > FREE_LEVELS + 1:
                        req_tokens = min_quest_level - FREE_LEVELS
                        def quest_rule(state, req=req_tokens, reqs=required_quests, items=unlock_items, loc=loc):
                            zone_ok = all(
                                (r in self.item_name_to_id and state.has(r, player))
                                for r in items
                            )

                            # Check for enough level tokens
                            level_ok = state.count("Progressive Level", player) >= req
                            # Check that all prerequisite quests are completed
                            prereq_ok = True
                            for r in reqs:
                                if r not in self.location_name_to_id:
                                    #print(f"[DEBUG] Missing prerequisite mapping for {r} (skipped)")
                                    continue  # skip it, don’t fail the rule
                                try:
                                    reachable = state.can_reach(r, "Location", player)
                                    #print(f"[DEBUG] Prerequisite '{r}' reachable: {reachable}")
                                    if not reachable:
                                        prereq_ok = False
                                except KeyError:
                                    #print(f"[DEBUG] Prerequisite '{r}' not present in region cache (skipped)")
                                    continue



                            return level_ok and prereq_ok and zone_ok

                        set_rule(loc, quest_rule)

                    elif required_quests != []:

                        # If the quest has prerequisites but no token requirement
                        def quest_rule(state, reqs=required_quests, items=unlock_items):
                            zone_ok = all(
                                (r in self.item_name_to_id and state.has(r, player))
                                for r in items
                            )
                            prereq_ok = True
                            for r in reqs:
                                if r not in self.location_name_to_id:
                                    #print(f"[DEBUG] Missing prerequisite mapping for {r} (skipped)")
                                    continue  # skip it, don’t fail the rule
                                try:
                                    reachable = state.can_reach(r, "Location", player)
                                    #print(f"[DEBUG] Prerequisite '{r}' reachable: {reachable}")
                                    if not reachable:
                                        prereq_ok = False
                                except KeyError:
                                    #print(f"[DEBUG] Prerequisite '{r}' not present in region cache (skipped)")
                                    continue


                            return prereq_ok and zone_ok

                        set_rule(loc, quest_rule)
                    else:
                        def quest_rule(state, reqs=required_quests, items=unlock_items):
                            return all(
                                (r in self.item_name_to_id and state.has(r, player))
                                for r in items
                            )

                        set_rule(loc, quest_rule)

        # --------------------------------------------------------------------------
        # Special-case: Winterspring connectivity via Timbermaw Hold
        # --------------------------------------------------------------------------

        if "Winterspring" in self.ZONES:
            print("[WOW] Adding special connection logic for Winterspring.")

            # Create Timbermaw Hold region if not already added
            timbermaw_name = "Timbermaw Hold"
            if not any(r.name == timbermaw_name and r.player == player for r in multiworld.regions):
                timbermaw_region = Region(timbermaw_name, player, multiworld)
                multiworld.regions.append(timbermaw_region)
                print(f"[WOW] Created special region: {timbermaw_name}")
            else:
                timbermaw_region = multiworld.get_region(timbermaw_name, player)

            # Connect Winterspring to Timbermaw Hold
            winterspring_region = multiworld.get_region("Winterspring", player)
            winterspring_region.connect(timbermaw_region)
            timbermaw_region.connect(winterspring_region)
            print("[WOW] Connected Winterspring → Timbermaw Hold")

            # Connect Timbermaw Hold to Felwood (if exists)
            if "Felwood" in self.ZONES:
                felwood_region = multiworld.get_region("Felwood", player)
                timbermaw_region.connect(felwood_region)
                felwood_region.connect(timbermaw_region)
                print("[WOW] Connected Timbermaw Hold → Felwood")

            # Connect Timbermaw Hold to Moonglade (if exists)
            if "Moonglade" in self.ZONES:
                moonglade_region = multiworld.get_region("Moonglade", player)
                timbermaw_region.connect(moonglade_region)
                moonglade_region.connect(timbermaw_region)
                print("[WOW] Connected Timbermaw Hold → Moonglade")

        # --- Special Case: Deadwind Pass (always added if it connects zones) ---
        deadwind_name = "Deadwind Pass"
        if deadwind_name not in self.ZONES:
            # Only add if at least one of its neighbor zones is present
            has_duskwood = "Duskwood" in self.ZONES
            has_sorrow = "Swamp of Sorrows" in self.ZONES

            if has_duskwood or has_sorrow:
                region = Region(deadwind_name, player, multiworld)
                multiworld.regions.append(region)

                # Connect it to Duskwood and/or Swamp of Sorrows if they exist
                if has_duskwood:
                    region.connect(multiworld.get_region("Duskwood", player))
                    multiworld.get_region("Duskwood", player).connect(region)
                if has_sorrow:
                    region.connect(multiworld.get_region("Swamp of Sorrows", player))
                    multiworld.get_region("Swamp of Sorrows", player).connect(region)

                # Mark as traversal only: no unlock token or level requirement
                print(f"[WOW] Added traversal region: {deadwind_name}")



        # --- Global Spell region ---
        spell_region = Region("Spellbook", player, multiworld)
        multiworld.regions.append(spell_region)
        menu.connect(spell_region)

        for spell_name, spell_data in self.SPELLS.items():
            if not spell_data["level"] and not spell_data["cost"]: # no locations for quest spells
                continue
            loc = Location(player, spell_name, self.location_name_to_id[spell_name], spell_region)
            spell_region.locations.append(loc)
            required_level = spell_data["level"]
            if required_level > FREE_LEVELS + 1:
                set_rule(loc, lambda state, req=required_level - FREE_LEVELS: state.count("Progressive Level", player) >= req)

        # --- Completion condition ---
        multiworld.completion_condition[player] = (
            lambda state: state.has("Victory", player)
        )

        print(f"[WOW] Created {len(sorted_zones)} zone regions with {len(self.QUESTS)} quests and {len(self.SPELLS)} spells.")
        print(f"[WOW] Shared quests across zones: {sum(len(v) > 1 for v in self.zone_quest_map.values())}")

    # --------------------------------------------------------------------------
    # Item Creation
    # --------------------------------------------------------------------------
    def create_items(self):
        multiworld = self.multiworld
        player = self.player
        early_items = {"Progressive Level": FREE_LEVELS}

        # --- Progressive Level Tokens ---
        for _ in range(self.player_max_level - FREE_LEVELS):
            item = Item("Progressive Level", ItemClassification.progression,
                        self.item_name_to_id["Progressive Level"], player)
            multiworld.itempool.append(item)

        starting_zones = []
        for character in self.allChars:
            if character["starting_zone"] not in starting_zones:
                starting_zones.append(character["starting_zone"])

        # --- Zone Unlock Tokens ---
        for zone_name, zone_data in self.ZONES.items():
            unlock_item_name = f"Unlock {zone_name}"
            if unlock_item_name not in self.item_name_to_id:
                self.item_name_to_id[unlock_item_name] = len(self.item_name_to_id) + 1

            item = Item(unlock_item_name, ItemClassification.progression,
                        self.item_name_to_id[unlock_item_name], player)
            if zone_data["min_level"] < self.player_max_level and zone_name not in starting_zones and zone_name != "Timbermaw Hold":
                multiworld.itempool.append(item)

        # --- Spell Tokens ---
        for spell_name in self.SPELLS.keys():
            if spell_name not in self.item_name_to_id:
                self.item_name_to_id[spell_name] = len(self.item_name_to_id) + 1

            item = Item(spell_name, ItemClassification.useful,
                        self.item_name_to_id[spell_name], player)
            multiworld.itempool.append(item)

            if (self.SPELLS[spell_name]["important"]):
                early_items[spell_name] = 1



        # --- Riding Tokens ---
        if self.player_max_level > 70: # Cold Weather
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
        if self.player_max_level > 66: # Artisan
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
        if self.player_max_level > 60: # Expert
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
        if self.player_max_level >= 40: # Journeyman and Mammoths
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
        if self.player_max_level >= 20: # Apprentice
            item = Item("Progressive Riding", ItemClassification.progression,
                self.item_name_to_id["Progressive Riding"], player)
            multiworld.itempool.append(item)
            early_items["Progressive Riding"] = 1



        # At least 5 levels, important spells, and riding if the max level is higher than 19
        multiworld.early_items[player] = early_items

        # --- Lock Victory to Final Level ---
        final_loc = next(
            (loc for loc in multiworld.get_locations(player) if loc.name == f"Level {self.player_max_level}"),
            None
        )
        if final_loc:
            final_loc.place_locked_item(
                Item("Victory", ItemClassification.progression, self.item_name_to_id["Victory"], player)
            )

        print(f"[WOW] Added {len(self.ZONES)} zone unlocks and {self.player_max_level - 1} level tokens.")


        # --- After adding all progression items (level tokens, unlocks, victory, etc.) ---
        player_locations = [loc for loc in multiworld.get_locations() if loc.player == player]
        total_locations = len(player_locations)
        total_items = len([i for i in multiworld.itempool if i.player == player])

        missing = total_locations - total_items - 1
        if missing > 0:
            for _ in range(missing):
                rand = random.random()
                if rand > 0.15 and not self.options.traps.value:
                    item = Item("Gold", ItemClassification.filler,
                                self.item_name_to_id["Gold"], player)
                elif rand > 0.17 and self.options.traps.value:
                    item = Item("Gold", ItemClassification.filler,
                                self.item_name_to_id["Gold"], player)
                elif rand > 0.05 and not self.options.traps.value:
                    item = Item("Random Buff", ItemClassification.filler,
                                self.item_name_to_id["Random Buff"], player)
                elif rand > 0.10 and self.options.traps.value:
                    item = Item("Random Buff", ItemClassification.filler,
                                self.item_name_to_id["Random Buff"], player)
                elif rand > 0.05 and self.options.traps.value:
                    item = Item("Random Debuff", ItemClassification.trap,
                                self.item_name_to_id["Random Debuff"], player)
                else:
                    item = Item("Random Bag", ItemClassification.filler,
                                self.item_name_to_id["Random Bag"], player)

                multiworld.itempool.append(item)

        print(f"[WOW] Added {missing} filler items for player {player} to match {total_locations} total locations.")
        print(f"[WOW] Added {len(self.ZONES)} zone unlocks, {self.player_max_level - 1} level tokens, and Victory.")

    def create_locations(self):
        for quest_name in self.QUESTS:
            if quest_name not in self.location_name_to_id:
                self.location_name_to_id[quest_name] = len(self.location_name_to_id) + 1

        for spell_name in self.SPELLS:
            if spell_name not in self.location_name_to_id:
                self.location_name_to_id[spell_name] = len(self.location_name_to_id) + 1

        # Also add the level locations (2–max)
        for level in range(2, self.player_max_level + 1):
            loc_name = f"Level {level}"
            if loc_name not in self.location_name_to_id:
                self.location_name_to_id[loc_name] = len(self.location_name_to_id) + 1


