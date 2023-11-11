from __future__ import annotations
from collections import defaultdict
from typing import DefaultDict, Dict, List, Set

import Global
import py.MonopolyGame.MonopolyGame.Result as Result
import Player


class Square:
    __all_squares__: Dict[int, Square] = {}

    def __init__(self, id: int, name: str):
        Square.__all_squares__[id] = self
        self.id: int = id
        self.name: str = name

    def __eq__(self, other):
        return self == other

    def __hash__(self):
        return self.id

    def execute_action(self, player: Player):
        raise NotImplementedError

    def _get_square_from_id(self, id):
        return self.__class__.__all_squares__[id]


class Buyable(Square):
    def __init__(
        self, id: int, name: str, value: int, rent: List[int], mortgage_value: int
    ):
        super().__init__(id, name)
        self.rent: List[int] = rent  # How much each tier costs - houses, e.g.
        self.value: int = value  # How much this property costs
        self.mortgage_value: int = mortgage_value

        self.owner: Player = None

        self._mortgaged = False

    def execute_action(self, player: Player, multiplier: int = 1):
        if self.owner is None:
            self._offer(player)
        elif self.owner != player:
            self._charge_rent(player, multiplier)

    def _offer(self, player: Player):
        if player._buy(self):
            self.owner = player
        else:
            self.owner = Player.auction(self)

    def _charge_rent(self, player: Player, multiplier: int) -> int:
        if self._mortgaged:
            return False
        else:
            rent_value = self._rent_value(multiplier)

    def _rent_value(self, multiplier: int) -> int:
        raise NotImplementedError("Buyable properties must define their rent value")


class Property(Buyable):
    groups: DefaultDict[str, List[Property]] = defaultdict(list)
    completed_groups: Set[str] = set()

    def __init__(
        self,
        id: int,
        name: str,
        group: str,
        value: int,
        rent: List[int],
        building_cost: int,
        mortgage_value: int,
    ):
        super().__init__(id, name, value, rent, mortgage_value)
        self.building_cost: int = building_cost
        self.buildings: int = 0
        self.__class__.groups[group].append(self)

        # Because of how Python works, all properties should refer to the same list.
        self.group_list = self.__class__.groups[group]
        self.group = group

    def _rent_value(self, multiplier: int):
        if multiplier != 1:
            raise ValueError("Properties should not have multipliers.")

        if self.group not in self.__class__.completed_groups:
            return self.rent[0]
        else:
            if self.buildings == 0:
                return self.rent[0] * 2
            else:
                return self.rent[self.buildings]

    def buy_building(self) -> Result.Error:
        if self.buildings == 5:
            return Result.BuildingOutOfBoundsError
        elif any(other.buildings < self.buildings for other in self.group_list):
            return Result.UnequalNumberOfBuildingsError
        elif self.buildings == 4 and Global.hotels == 0:
            return Global.NoMoreHotels
        elif Global.houses == 0:
            return Global.NoMoreHouses

        self.buildings += 1
        if self.buildings == 4:
            Global.houses += 4
            Global.hotels -= 1
        else:
            Global.houses += 1
        return Result.NoError

    def sell_building(self) -> Result.Error:
        if self.buildings == 0:
            return Result.BuildingOutOfBoundsError
        elif any(other.buildings > self.buildings for other in self.group_list):
            return Result.UnequalNumberOfBuildingsError

        if self.buildings == 5:
            if Global.houses < 4:
                return Global.NoMoreHouses
            else:
                Global.houses -= 4
                Global.hotels += 1
        else:
            Global.houses += 1

        self.buildings -= 1
        return Result.NoError

    class BuildingOutOfBoundsError(Result.Error):
        default_message = "Cannot buy or sell another property - would lead to too many or too few buildings."

    class UnequalNumberOfBuildingsError(Result.Error):
        default_message = "Cannot buy or sell another property - would lead to imbalance of buildings in the same group."


class Railroad(Buyable):
    owners: DefaultDict[Player.Player, Set[Railroad]] = defaultdict(set)

    def __init__(
        self, id: int, name: str, value: int, rent: List[int], mortgage_value: int
    ):
        super().__init__(id, name, value, rent, mortgage_value)

    def _rent_value(self, multiplier: int) -> int:
        railroads_owned = self.__class__.owners[self.owner]
        return multiplier * self.rent[railroads_owned - 1]


class Utility(Buyable):
    owners: DefaultDict[Player.Player, Set[Utility]] = defaultdict(set)

    def _rent_value(self, multiplier: int) -> int:
        # Treat "multiplier" as the dice roll
        utilities_owned = self.__class__.owners[self.owner]
        if utilities_owned == 1:
            return 10 * multiplier
        elif utilities_owned == 2:
            return 4 * multiplier
        else:
            raise ValueError(f"Cannot own {utilities_owned} utilities and charge rent!")


def importer(json: Dict):
    pass
