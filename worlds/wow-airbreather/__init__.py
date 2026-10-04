import uuid

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region
from rule_builder.rules import And, CanReachLocation, Has, Rule
from worlds.AutoWorld import World

from .options import WowAirbreatherGameOptions
from .races_and_classes import ALL_CLASSES, RACES_AND_CLASSES, RaceAndClass

GAME_NAME = "World of Warcraft - airbreather Variant"


class WoWCharacterSlotRegion(Region):
    slot_number: int
    race_and_class: RaceAndClass
    unlock_requirement: Rule

    def __init__(self,
                 slot_number: int,
                 race_and_class: RaceAndClass,
                 player: int,
                 multiworld: MultiWorld,
                 hint: str | None = None):

        super().__init__(f"Slot {slot_number} - {race_and_class}", player, multiworld, hint)
        self.slot_number = slot_number
        self.race_and_class = race_and_class


def create_item_name_to_id():
    result: dict[str, int] = {
        "1 Gold": 99998,
    }

    for slot_index in range(6):
        slot_number = slot_index + 1
        slot_location_id_base = slot_number * 1000
        result[f"Slot {slot_number} - Progressive Level Cap"] = slot_location_id_base + 1

    return result


def create_location_name_to_id():
    result: dict[str, int] = { }

    for slot_index in range(6):
        slot_number = slot_index + 1
        slot_location_id_base = slot_number * 1000
        result[f"Slot {slot_number} - Complete Capstone Quest"] = slot_location_id_base + 1
        for level in range(2, 13):
            result[f"Slot {slot_number} - Reach Level {level}"] = slot_location_id_base + level

    return result


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
        for _ in range(2):
            self.multiworld.push_precollected(self.create_item("Slot 1 - Progressive Level Cap"))

    def create_item(self, name: str):
        item_id = WoWAirbreatherWorld.item_name_to_id[name]
        classification = \
            ItemClassification.filler if item_id == 99998 \
            else ItemClassification.progression

        return Item(name, classification, item_id, self.player)

    def create_items(self):
        for slot_index in range(6):
            slot_number = slot_index + 1
            for level_index in range(12):
                if slot_index == 0 and level_index < 2:
                    # first 2 progressive level caps are already precollected.
                    # we need to balance locations and items, though, so...
                    self.multiworld.itempool.append(self.create_item("1 Gold"))
                else:
                    self.multiworld.itempool.append(self.create_item(f"Slot {slot_number} - Progressive Level Cap"))

    def create_regions(self):
        origin_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(origin_region)
        self.origin_region_name = origin_region.name
        goal_completion_rules: list[Rule] = []

        for slot_index in range(6):
            slot = self.slots[slot_index]
            slot_number = slot_index + 1
            slot_region = WoWCharacterSlotRegion(slot_number, slot, self.player, self.multiworld)
            origin_region.connect(slot_region, rule=Has(f"Slot {slot_number} - Progressive Level Cap"))
            capstone_quest_location_name = f"Slot {slot_number} - Complete Capstone Quest"
            capstone_quest_location = Location(
                self.player,
                capstone_quest_location_name,
                self.location_name_to_id[capstone_quest_location_name],
                slot_region,
            )
            slot_region.locations.append(capstone_quest_location)
            goal_completion_rules.append(CanReachLocation(capstone_quest_location_name, slot_region.name))

            for level in range(2, 13):
                level_location_name = f"Slot {slot_number} - Reach Level {level}"
                level_location = Location(
                    self.player,
                    level_location_name,
                    self.location_name_to_id[level_location_name],
                    slot_region,
                )
                slot_region.locations.append(level_location)
                if level == slot.capstone_quest_level:
                    self.set_rule(capstone_quest_location, CanReachLocation(level_location_name, slot_region.name))
                self.set_rule(level_location, Has(f"Slot {slot_number} - Progressive Level Cap", level))
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
