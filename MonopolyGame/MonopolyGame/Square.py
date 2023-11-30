from __future__ import annotations
from collections import defaultdict
from typing import DefaultDict, List, Set

import Global
import Result
import Player
import Card


class Square:
    def __repr__(self) -> str:
        return f"{self.id}: {self.name} ({self.__class__.__name__})"

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name

    def __eq__(self, other):
        return self == other

    def __hash__(self):
        return self.id

    def execute_action(self, player: Player):
        raise NotImplementedError


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

    def execute_action(self, player: Player, multiplier: int = 1) -> None:
        if self.owner is None:
            self.offer(player)
        elif self.owner != player and not self._mortgaged:
            self.charge_rent(player, multiplier)

    def offer(self, player: Player) -> None:
        if player.buy_square(self):
            self.owner = player
        else:
            self.owner = Global.auction(self, player)

    def charge_rent(self, player: Player, multiplier: int) -> int:
        rent_value = self._rent_value(multiplier)
        player.pay_rent(rent_value)

    def mortgage(self) -> Result.Result:
        if self._mortgaged:
            return self.MortgageStatusError
        else:
            self._mortgaged = True
            return Result.Ok

    def unmortgage(self) -> Result.Result:
        if not self._mortgaged:
            return self.MortgageStatusError
        elif self.owner.balance >= 1.1 * self.mortgage_value:
            self._mortgaged = False
            return Result.Ok
        else:
            return self.InsufficientBalanceError

    def _rent_value(self, multiplier: int) -> int:
        raise NotImplementedError("Buyable properties must define their rent value")

    class MortgageStatusError(Result.Error):
        default_message = (
            "Could not mortgage/unmortgage if already mortgated/unmortgaged."
        )

    class InsufficientBalanceError(Result.Error):
        default_message = "Player doesn't have enough balance."


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
        if self._mortgaged:
            return self.BuildingOnMortgagedError
        elif self.buildings == 5:
            return self.BuildingOutOfBoundsError
        elif any(other.buildings < self.buildings for other in self.group_list):
            return self.UnequalNumberOfBuildingsError
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
            return self.BuildingOutOfBoundsError
        elif any(other.buildings > self.buildings for other in self.group_list):
            return self.UnequalNumberOfBuildingsError

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

    def unmortgage(self, balance: int) -> Result:
        if any(other.buildings > 0 for other in self.group_list):
            # TODO
            return self.BuildingOnMortgagedError
        return super().unmortgage(balance)

    class BuildingOnMortgagedError(Result.Error):
        default_message = "Cannot build buildings on a mortgaged property"

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


class CardSquare(Square):
    def __init__(self, id: int, name: str, deck: List, game: Global.Game):
        # TODO - make this a circular linkedlist
        super().__init__(id, name)

        self.deck: List[Card.Card] = deck
        self.game = game

    def execute_action(self, player: Player):
        card = self.deck.pop()
        card.execute(self.game, player)


class Start(Square):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)

    def execute_action(self, player: Player):
        player.balance += 200


class Tax(Square):
    def __init__(self, id: int, name: str, value: int):
        super().__init__(id, name)
        self.value = value

    def execute_action(self, player: Player):
        # TODO - should probably just work on the player "-" operator
        player.balance -= self.value
