"""
Option definitions for World of Warcraft
"""
from dataclasses import dataclass

from Options import (Choice, DeathLink, DefaultOnToggle, OptionSet, NamedRange, Range, Toggle, PerGameCommonOptions)

class WoWRace(Choice):
    """
    Choose which race you will play as.

    - Human
    - Dwarf
    - Gnome
    - Night Elf
    - Draenei
    - Orc
    - Troll
    - Tauren
    - Forsaken
    - Blood Elf
    - Random
    """
    display_name = "Choose Race"
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

class PlayerClass(Choice):
    """
    Choose which class you will play as.
    Note: Death Knight currently unsupported.

    Only valid combinations are usable for now.

    - Warrior
    - Death Knight
    - Paladin
    - Hunter
    - Shaman
    - Rogue
    - Druid
    - Priest
    - Warlock
    - Mage
    - Random
    """
    display_name = "Choose Class"
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

@dataclass
class WorldOfWarcraftOptions(PerGameCommonOptions):
    wow_race: WoWRace
    starting_zone: StartingZone
    player_class: PlayerClass
    goal: Goal
    speed_boost: SpeedBoost
    exp_boost: ExpBoost
    heirloom_armor: HeirloomArmor
    heirloom_weapons: HeirloomWeapons
    heirloom_trinkets: HeirloomTrinkets
    traps: Traps
    death_link: WoWDeathLink
