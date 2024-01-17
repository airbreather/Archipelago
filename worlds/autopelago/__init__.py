from typing import Callable, Literal

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .ArbitraryGameDefs import \
    BASE_ID, GAME_NAME, AutopelagoRegion, num_locations_in, \
    prog_count_balancing_excluding_goal, prog_count_skip_balancing, useful_count, filler_count, trap_count

from .Items import \
    a_item_name, b_item_name, c_item_name, d_item_name, e_item_name, f_item_name, goal_item_name, \
    all_item_names, generic_item_table, game_specific_items, item_name_to_defined_classification

def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1


class AutopelagoItem(Item):
    game = GAME_NAME


class AutopelagoLocation(Location):
    game = GAME_NAME


class AutopelagoWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Autopelago',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Joe Amenta']
        )
    ]


class AutopelagoWorld(World):
    '''
    An idle game, in the same vein as ArchipIDLE but intended to be more sophisticated.
    '''
    game = GAME_NAME
    topology_present = False # it's static, so setting this to True isn't actually helpful
    data_version = 0
    web = AutopelagoWebWorld()

    # location_name_to_id and item_name_to_id must be filled VERY early, but seemingly only because
    # they are used in Main.main to log the ID ranges in use. if not for that, we probably could've
    # been able to get away with populating these just based on what we actually need.
    location_name_to_id = { }
    _id_gen = _gen_ids()
    for r in AutopelagoRegion:
        for i in range(num_locations_in[r]):
            location_name_to_id[r.get_location_name(i)] = next(_id_gen)
    item_name_to_id = { }
    _id_gen = _gen_ids()
    for item_name in all_item_names:
        item_name_to_id[item_name] = next(_id_gen)
    del _id_gen

    # insert other ClassVar values... suggestions include:
    # - item_name_groups
    # - item_descriptions
    # - location_name_groups
    # - location_descriptions
    # - hint_blacklist (should it include the goal item?)

    # other variables we use are INSTANCE variables that depend on the specific multiworld.
    _item_name_to_classification: dict[str, ItemClassification]
    _all_live_items_excluding_goal: list[str]
    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self._item_name_to_classification = { item_name: classification for item_name, classification in item_name_to_defined_classification.items() if classification is not None }
        self._all_live_items_excluding_goal: list[str] = [a_item_name, b_item_name, c_item_name, d_item_name, e_item_name, f_item_name]

    def generate_early(self):
        # finalize the list of possible items, based on which games are present in this multiworld.
        full_item_table = { c: [item_name for item_name in items] for c, items in generic_item_table.items() }
        dlc_games = { game for game in game_specific_items }
        for category, items in full_item_table.items():
            replacements_made = 0
            for game_name in self.multiworld.game.values():
                if game_name not in dlc_games:
                    continue
                dlc_games.remove(game_name)
                for item in game_specific_items[game_name][category]:
                    items[replacements_made] = item
                    replacements_made += 1

        category_to_next_offset = { category: 0 for category in full_item_table }
        def append_next_n_item_names(category: Literal['other_progression', 'useful_nonprogression', 'filler', 'trap', 'uncategorized'], n: int, classification: ItemClassification):
            def next_up_to_n_item_names(category: Literal['other_progression', 'useful_nonprogression', 'filler', 'trap', 'uncategorized'], n: int):
                items = full_item_table[category]
                offset = category_to_next_offset[category]
                avail = len(items) - offset
                if avail < n:
                    n = avail
                yield from (items[offset + i] for i in range(n))
                category_to_next_offset[category] += n

            for item_name in next_up_to_n_item_names(category, n):
                self._all_live_items_excluding_goal.append(item_name)
                self._item_name_to_classification[item_name] = classification
                n -= 1

            if n > 0:
                for item_name in next_up_to_n_item_names('uncategorized', n):
                    self._all_live_items_excluding_goal.append(item_name)
                    self._item_name_to_classification[item_name] = classification
                    n -= 1

        num_key_items = len(self._all_live_items_excluding_goal)
        append_next_n_item_names('other_progression', prog_count_balancing_excluding_goal - num_key_items, ItemClassification.progression)
        append_next_n_item_names('other_progression', prog_count_skip_balancing, ItemClassification.progression_skip_balancing)
        append_next_n_item_names('useful_nonprogression', useful_count, ItemClassification.useful)
        append_next_n_item_names('filler', filler_count, ItemClassification.filler)
        append_next_n_item_names('trap', trap_count, ItemClassification.trap)

    def set_rules(self):
        def _connect(r_from: AutopelagoRegion, r_to: AutopelagoRegion, access_rule: Callable[[CollectionState], bool] | None = None):
            r_from_real = self.multiworld.get_region(r_from.name, self.player)
            r_to_real = self.multiworld.get_region(r_to.name, self.player)
            connection = Entrance(self.player, '', r_from_real)
            if access_rule:
                connection.access_rule = access_rule
            r_from_real.exits.append(connection)
            connection.connect(r_to_real)

        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeA, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeB, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.After8RatsBeforeA, AutopelagoRegion.A)
        _connect(AutopelagoRegion.After8RatsBeforeB, AutopelagoRegion.B)
        _connect(AutopelagoRegion.A, AutopelagoRegion.AfterABeforeC, lambda state: state.has(a_item_name, self.player))
        _connect(AutopelagoRegion.B, AutopelagoRegion.AfterBBeforeD, lambda state: state.has(b_item_name, self.player))
        _connect(AutopelagoRegion.AfterABeforeC, AutopelagoRegion.C)
        _connect(AutopelagoRegion.AfterBBeforeD, AutopelagoRegion.D)
        _connect(AutopelagoRegion.C, AutopelagoRegion.AfterCBefore20Rats, lambda state: state.has(c_item_name, self.player))
        _connect(AutopelagoRegion.D, AutopelagoRegion.AfterDBefore20Rats, lambda state: state.has(d_item_name, self.player))
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.E)
        _connect(AutopelagoRegion.After20RatsBeforeF, AutopelagoRegion.F)
        _connect(AutopelagoRegion.E, AutopelagoRegion.TryingForGoal, lambda state: state.has(e_item_name, self.player))
        _connect(AutopelagoRegion.F, AutopelagoRegion.TryingForGoal, lambda state: state.has(f_item_name, self.player))

        self.multiworld.get_location("goal", self.player).place_locked_item(self.create_item(goal_item_name))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item_name, self.player)

    def create_item(self, name: str):
        id = self.item_name_to_id[name]
        classification = self._item_name_to_classification[name]
        item = AutopelagoItem(name, classification, id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += (self.create_item(name) for name in self._all_live_items_excluding_goal)

    def create_regions(self):
        self.multiworld.regions += (self.create_region(r) for r in AutopelagoRegion)

        # logic assumes that the player starts in a special hardcoded "Menu" region
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        entrance = Entrance(self.player, '', menu)
        menu.exits.append(entrance)
        entrance.connect(self.multiworld.get_region(AutopelagoRegion.Before8Rats.name, self.player))

    def create_region(self, r: AutopelagoRegion):
        region = Region(r.name, self.player, self.multiworld)
        for i in range(num_locations_in[r]):
            location_name = r.get_location_name(i)
            location_id = self.location_name_to_id[location_name]
            location = AutopelagoLocation(self.player, location_name, location_id, region)
            region.locations.append(location)
        return region

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"