from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle


class UsingModIndividualProgression(Toggle):
    """Toggle on if you use mod-individual-progression"""
    display_name = "Using module 'Individual Player Progression'"


@dataclass
class WowAirbreatherGameOptions(PerGameCommonOptions):
    using_mod_individual_progression: UsingModIndividualProgression
