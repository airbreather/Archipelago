import uuid

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region
from rule_builder.rules import And, CanReachLocation, Has, Rule
from worlds.AutoWorld import World

from .options import WowAirbreatherGameOptions
from .races_and_classes import ALL_CLASSES, RACES_AND_CLASSES, RaceAndClass

GAME_NAME = "World of Warcraft - airbreather Variant"
LEVEL_CAP_INCREMENTS = [4, 6, 8, 10, 12]

class WoWCharacterSlotRegion(Region):
    race_and_class: RaceAndClass

    def __init__(self, race_and_class: RaceAndClass, player: int, multiworld: MultiWorld):
        super().__init__(str(race_and_class), player, multiworld)
        self.race_and_class = race_and_class


def create_item_name_to_id():
    result: dict[str, int] = {
        "1 Gold": 99998,
    }

    for race_and_class in RACES_AND_CLASSES:
        result[f"{race_and_class} - Progressive Level Cap"] = len(result) + 1

    return result


def create_location_name_to_id():
    result: dict[str, int] = { }

    for race_and_class in RACES_AND_CLASSES:
        result[f"{race_and_class} - Complete Capstone Quest"] = len(result) + 1
        for level in range(2, 13):
            result[f"{race_and_class} - Reach Level {level}"] = len(result) + 1

    return result


def level_caps_needed_for_level(level: int):
    for i, unlocked in enumerate(LEVEL_CAP_INCREMENTS):
        if unlocked >= level:
            return i + 1
    raise ValueError("level is not accessible")

class WoWAirbreatherWorld(World):
    game = GAME_NAME
    options_dataclass = WowAirbreatherGameOptions
    options: WowAirbreatherGameOptions

    item_name_to_id = create_item_name_to_id()
    location_name_to_id = create_location_name_to_id()

    slots: list[RaceAndClass]

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.slots = []

    def generate_early(self):
        # start by picking the 6 classes
        classes = [clazz for clazz in ALL_CLASSES if clazz != "Death Knight"]
        self.multiworld.random.shuffle(classes)
        for clazz in classes[:6]:
            self.slots.append(self.multiworld.random.choice([
                race_and_class for race_and_class in RACES_AND_CLASSES if race_and_class.clazz == clazz
            ]))
        self.multiworld.push_precollected(self.create_item(f"{self.slots[0]} - Progressive Level Cap"))

    def create_item(self, name: str):
        item_id = WoWAirbreatherWorld.item_name_to_id[name]
        classification = \
            ItemClassification.filler if item_id == 99998 \
            else ItemClassification.progression

        return Item(name, classification, item_id, self.player)

    def create_items(self):
        for slot in self.slots:
            for level in range(2, 13):
                # only add progressive level cap items for the ones that are NEEDED to reach their
                # corresponding milestones.
                if level in LEVEL_CAP_INCREMENTS:
                    self.multiworld.itempool.append(self.create_item(f"{slot} - Progressive Level Cap"))
                else:
                    # we're going to add locations for all levels. locations and items need to be
                    # balanced, so add fillers to balance that out
                    self.multiworld.itempool.append(self.create_filler())
            # add one more item corresponding to the "complete capstone quest"
            self.multiworld.itempool.append(self.create_filler())

    def create_regions(self):
        origin_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(origin_region)
        self.origin_region_name = origin_region.name
        goal_completion_rules: list[Rule] = []

        for slot in self.slots:
            slot_region = WoWCharacterSlotRegion(slot, self.player, self.multiworld)
            origin_region.connect(slot_region, rule=Has(f"{slot} - Progressive Level Cap"))
            capstone_quest_location_name = f"{slot} - Complete Capstone Quest"
            capstone_quest_location = Location(
                self.player,
                capstone_quest_location_name,
                self.location_name_to_id[capstone_quest_location_name],
                slot_region,
            )

            for level in range(2, 13):
                level_location_name = f"{slot} - Reach Level {level}"
                level_location = Location(
                    self.player,
                    level_location_name,
                    self.location_name_to_id[level_location_name],
                    slot_region,
                )
                slot_region.locations.append(level_location)
                if level == slot.capstone_quest_level:
                    slot_region.locations.append(capstone_quest_location)
                    goal_completion_rules.append(CanReachLocation(capstone_quest_location_name, slot_region.name))
                    self.set_rule(capstone_quest_location, CanReachLocation(level_location_name, slot_region.name))
                level_caps_needed = level_caps_needed_for_level(level)
                self.set_rule(level_location, Has(f"{slot} - Progressive Level Cap", level_caps_needed))
                if level == 12:
                    goal_completion_rules.append(CanReachLocation(level_location_name, slot_region.name))
            self.multiworld.regions.append(slot_region)

        # goal: complete all capstone quests and reach level 12 in all slots.
        self.set_completion_rule(And(*goal_completion_rules))

    def get_filler_item_name(self):
        assert "1 Gold" in self.item_name_to_id
        return "1 Gold"

    def fill_slot_data(self):
        return {
            "ap_id": str(uuid.uuid4()),
        }
