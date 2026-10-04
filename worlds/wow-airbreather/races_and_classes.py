from typing import Literal

WoWRace = Literal[
    "Human", "Orc", "Dwarf", "Night Elf", "Undead", "Tauren", "Gnome", "Troll", "Blood Elf", "Draenei",
]
WoWClass = Literal[
    "Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "Druid",
]

ALL_RACES = frozenset[WoWRace]((
    "Human", "Orc", "Dwarf", "Night Elf", "Undead", "Tauren", "Gnome", "Troll", "Blood Elf", "Draenei",
))
ALL_CLASSES = frozenset[WoWClass]((
    "Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "Druid",
))


class RaceAndClass:
    race: WoWRace
    clazz: WoWClass
    capstone_quest_level: int

    def __init__(self, race: WoWRace, clazz: WoWClass, capstone_quest_level: int):
        self.race = race
        self.clazz = clazz
        self.capstone_quest_level = capstone_quest_level

    def __hash__(self):
        return hash((self.race, self.clazz, self.capstone_quest_level))

    def __eq__(self, other: object):
        return isinstance(other, RaceAndClass) and self.race == other.race and self.clazz == other.clazz

    def __str__(self):
        return f"{self.race} {self.clazz}"


# excluding Death Knight: all races can be one, and it's special anyway.
RACES_AND_CLASSES = frozenset[RaceAndClass]((
    RaceAndClass("Human", "Mage", 10),
    RaceAndClass("Human", "Paladin", 12), # paladins' very first non-letter quest teaches Redemption at 12
    RaceAndClass("Human", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Human", "Rogue", 10),
    RaceAndClass("Human", "Warlock", 10),
    RaceAndClass("Human", "Warrior", 10),
    RaceAndClass("Dwarf", "Hunter", 10),
    RaceAndClass("Dwarf", "Paladin", 12), # paladins' very first non-letter quest teaches Redemption at 12
    RaceAndClass("Dwarf", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Dwarf", "Rogue", 10),
    RaceAndClass("Dwarf", "Warrior", 10),
    RaceAndClass("Night Elf", "Druid", 10),
    RaceAndClass("Night Elf", "Hunter", 10),
    RaceAndClass("Night Elf", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Night Elf", "Rogue", 10),
    RaceAndClass("Night Elf", "Warrior", 10),
    RaceAndClass("Gnome", "Mage", 10),
    RaceAndClass("Gnome", "Rogue", 10),
    RaceAndClass("Gnome", "Warlock", 10),
    RaceAndClass("Gnome", "Warrior", 10),
    RaceAndClass("Draenei", "Hunter", 10),
    RaceAndClass("Draenei", "Mage", 10),
    RaceAndClass("Draenei", "Paladin", 12), # paladins' very first non-letter quest teaches Redemption at 12
    RaceAndClass("Draenei", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Draenei", "Shaman", 10),
    RaceAndClass("Draenei", "Warrior", 10),
    RaceAndClass("Orc", "Hunter", 10),
    RaceAndClass("Orc", "Rogue", 10),
    RaceAndClass("Orc", "Shaman", 10),
    RaceAndClass("Orc", "Warlock", 10),
    RaceAndClass("Orc", "Warrior", 10),
    RaceAndClass("Undead", "Mage", 10),
    RaceAndClass("Undead", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Undead", "Rogue", 10),
    RaceAndClass("Undead", "Warlock", 10),
    RaceAndClass("Undead", "Warrior", 10),
    RaceAndClass("Tauren", "Druid", 10),
    RaceAndClass("Tauren", "Hunter", 10),
    RaceAndClass("Tauren", "Shaman", 10),
    RaceAndClass("Tauren", "Warrior", 10),
    RaceAndClass("Troll", "Hunter", 10),
    RaceAndClass("Troll", "Mage", 10),
    RaceAndClass("Troll", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Troll", "Rogue", 10),
    RaceAndClass("Troll", "Shaman", 10),
    RaceAndClass("Troll", "Warrior", 10),
    RaceAndClass("Blood Elf", "Hunter", 10),
    RaceAndClass("Blood Elf", "Mage", 10),
    RaceAndClass("Blood Elf", "Paladin", 12), # paladins' very first non-letter quest teaches Redemption at 12
    RaceAndClass("Blood Elf", "Priest", 5), # priests' level 10 quest was removed in 3.0 and replaced with nothing
    RaceAndClass("Blood Elf", "Rogue", 10),
    RaceAndClass("Blood Elf", "Warlock", 10),
))
