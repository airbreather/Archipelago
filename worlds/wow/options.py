"""
Option definitions for World of Warcraft
"""
from dataclasses import dataclass

from Options import (Choice, DeathLink, DefaultOnToggle, OptionSet, NamedRange, Range, Toggle, PerGameCommonOptions)

class WoWRace(Choice):
    display_name = "Character Race"
    default = 0
    option_human = 0
    option_dwarf = 1
    option_gnome = 2
    option_night_elf = 3
    option_draenei = 4
    option_orc = 5
    option_troll = 6
    option_tauren = 7
    option_forsaken = 8
    option_blood_elf = 9
    #option_random = 10

class WoWClass(Choice):
    display_name = "Character Class"
    default = 0
    option_warrior = 0
    option_death_knight = 1
    option_paladin = 2
    option_hunter = 3
    option_shaman = 4
    option_rogue = 5
    option_druid = 6
    option_priest = 7
    option_warlock = 8
    option_mage = 9
    #option_random = 10

class WoWRaceClassCombo(OptionSet):
    """
    Choose which race and class you will play as.
    Only valid race/class combos are accepted for now.
    You may choose multiple characters to play.

    The format is ["Race/Class"], ex:
    ["Human/Warrior"] or ["Night Elf Hunter/Blood Elf Mage"]

    """
    display_name = "Character Selection"
    valid_keys = [
        "Human/Warrior", "Human/Paladin", "Human/Rogue", "Human/Death Knight", "Human/Priest", "Human/Mage", "Human/Warlock",
        "Dwarf/Warrior", "Dwarf/Paladin", "Dwarf/Hunter", "Dwarf/Rogue", "Dwarf/Death Knight", "Dwarf/Priest",
        "Night Elf/Warrior", "Night Elf/Hunter", "Night Elf/Rogue", "Night Elf/Priest", "Night Elf/Druid",
        "Gnome/Warrior", "Gnome/Rogue", "Gnome/Death Knight", "Gnome/Mage", "Gnome/Warlock",
        "Draenei/Warrior", "Draenei/Paladin", "Draenei/Hunter", "Draenei/Death Knight", "Dranei/Shaman", "Draenei/Priest", "Draenei/Mage",
        "Orc/Warrior", "Orc/Hunter", "Orc/Rogue", "Orc/Death Knight", "Orc/Shaman", "Orc/Warlock",
        "Undead/Warrior", "Undead/Rogue", "Undead/Death Knight", "Undead/Priest", "Undead/Mage", "Undead/Warlock",
        "Tauren/Warrior", "Tauren/Hunter", "Tauren/Death Knight", "Tauren/Shaman", "Tauren/Druid",
        "Troll/Warrior", "Troll/Hunter", "Troll/Rogue", "Troll/Death Knight", "Troll/Shaman", "Troll/Priest", "Troll/Mage",
        "Blood Elf/Paladin", "Blood Elf/Hunter", "Blood Elf/Death Knight", "Blood Elf/Priest", "Blood Elf/Mage", "Blood Elf/Warlock"
    ]

    #option_random = 10

class StartingZone(Choice):
    """
    Determines which zone you start in. Currently unsupported.

    - Normal = The zone assigned to your race
    - Elwynn Forest = Default Human starting zone
    - Dun Morogh = Default Dwarf and Gnome starting zone
    - Teldrassil = Default Night Elf starting zone
    - Azuremyst Isle = Default Draenei starting zone
    - Durotar = Default Orc and Troll starting zone
    - Mulgore = Default Tauren starting zone
    - Tirisfal Glades = Default Forsaken starting zone
    - Eversong Woods = Default Blood Elf starting zone
    - Random = Any starting zone
    """
    display_name = "Starting Zone"
    default = 0
    option_normal = 0
    option_elwynn_forest = 1
    option_dun_morogh = 2
    option_teldrassil = 3
    option_azuremyst_isle = 4
    option_durotar = 5
    option_mulgore = 6
    option_tirisfal_glades = 7
    option_eversong_woods = 8
    #option_random = 9

class RandomizeSpells(Toggle):
    """
    Choose to either shuffle spells into the pool (default), or randomize which spells you can get from your entire class list
    """
    display_name = "Shuffle/Randomize Spells"

class Goal(Choice):
    """
    Choose what the goal of the game is.
    For now, choose which level to end at.
    """
    display_name = "Goal"
    default = 0
    option_level_10 = 0
    option_level_20 = 1
    option_level_30 = 2
    option_level_40 = 3
    option_level_50 = 4
    option_level_60 = 5
    option_level_70 = 6
    option_level_80 = 7

class SpeedBoost(Range):
    """
    Multiplies player movement speed.

    1 is default
    2 is journeyman riding
    5 is the max
    """
    display_name = "Speed Multiplier"
    range_start = 1
    range_end = 5
    default = 1

class ExpBoost(Range):
    """
    Multiplies gained experience.

    1 is default
    2 is double
    10 is the max
    """
    display_name = "Exp Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class HeirloomWeapons(Toggle):
    """
    Choose if class-appropriate heirloom weapons should be given to the player at the start of the game.
    """
    display_name = "Start with Heirloom Weapons"

class HeirloomArmor(Toggle):
    """
    Choose if class-appropriate heirloom armor should be given to the player at the start of the game.
    """
    display_name = "Start with Heirloom Armor"

class HeirloomTrinkets(Toggle):
    """
    Choose if heirloom trinkets should be given to the player at the start of the game.
    """
    display_name = "Start with Heirloom Trinkets"

class Traps(Toggle):
    """
    Choose if traps should be enabled.
    Traps are random debuffs.
    """
    display_name = "Enable Traps"

class WoWDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__

class PrimaryProfessions(OptionSet):
    """
    Adds quests that require the player to have specific professions in order to accept and complete.
    It is highly recommended to choose a maximum of two per character.
    """
    display_name = "Primary Professions"
    valid_keys = ["Skinning", "Herbalism", "Mining", "Leatherworking", "Alchemy", "Inscription", "Blacksmithing", "Jewelcrafting", "Tailoring", "Enchanting"]

class Fishing(Toggle):
    """
    Adds quests that require the player to have trained fishing.
    """
    display_name = "Enable Fishing Quests"

class FirstAid(DefaultOnToggle):
    """
    Adds quests that require the player to have trained first aid.
    """
    display_name = "Enable First Aid Quests"

class Cooking(DefaultOnToggle):
    """
    Adds quests that require the player to have trained cooking.
    """
    display_name = "Enable Cooking Quests"


@dataclass
class WorldOfWarcraftOptions(PerGameCommonOptions):
    wow_race: WoWRace
    wow_class: WoWClass
    wow_race_and_class_combo: WoWRaceClassCombo
    randomize_spells: RandomizeSpells
    starting_zone: StartingZone
    goal: Goal
    speed_boost: SpeedBoost
    exp_boost: ExpBoost
    heirloom_armor: HeirloomArmor
    heirloom_weapons: HeirloomWeapons
    heirloom_trinkets: HeirloomTrinkets
    traps: Traps
    death_link: WoWDeathLink
    primary_professions: PrimaryProfessions
    fishing: Fishing
    first_aid: FirstAid
    cooking: Cooking
