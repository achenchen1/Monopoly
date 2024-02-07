from __future__ import annotations
from collections import defaultdict
from typing import DefaultDict, List, Set

from MonopolyGame.Common import Game
from MonopolyGame.Common import Player
from MonopolyGame.Common import Card
from MonopolyGame.Utils.DataClasses import Result, Error, Ok


class Square:
    def __repr__(self) -> str:
        return f"{self.id}: {self.name} ({self.__class__.__name__})"

    def __str__(self) -> str:
        return f"{self.name}"

    def __init__(self, id: int, name: str, game: Game.Game):
        self.id: int = id
        self.name: str = name
        self.game: Game.Game = game

    def __eq__(self, other):
        return type(self) == type(other) and self == other

    def __hash__(self):
        return self.id

    def execute_action(self, player: Player):
        raise NotImplementedError


class Buyable(Square):
    def __init__(
        self,
        id: int,
        name: str,
        value: int,
        rent: List[int],
        mortgage_value: int,
        game: Game.Game,
    ):
        super().__init__(id, name, game)
        self.rent: List[int] = rent  # How much each tier costs - houses, e.g.
        self.value: int = value  # How much this property costs
        self.mortgage_value: int = (
            mortgage_value  # Note - unmortgage value is always 1.1*mortgage_value
        )

        self.owner: Player = None

        self._mortgaged = False

    def execute_action(self, player: Player, multiplier: int = 1) -> None:
        if self.owner is None:
            new_owner: Player = self.offer(player)
            if new_owner is not None:
                # TODO - else condition
                if new_owner.modify_balance(-self.value):
                    new_owner.properties.append(self)
        elif self.owner != player and not self._mortgaged:
            self.charge_rent(player, multiplier)

    def offer(self, player: Player) -> None:
        if player.buy_square(self):
            self.owner = player
        else:
            self.owner = self.game.auction(self, player)
        return self.owner

    def charge_rent(self, player: Player, multiplier: int) -> int:
        rent_value = self._rent_value(multiplier)
        player.pay_rent(rent_value)

    def mortgage(self) -> Result:
        if self._mortgaged:
            return self.MortgageStatusError
        else:
            self._mortgaged = True
            return Ok

    def unmortgage(self) -> Result:
        if not self._mortgaged:
            return self.MortgageStatusError
        elif self.owner.balance >= 1.1 * self.mortgage_value:
            self._mortgaged = False
            return Ok
        else:
            return self.InsufficientBalanceError

    def _rent_value(self, multiplier: int) -> int:
        raise NotImplementedError("Buyable properties must define their rent value")

    def liquidate_value(self) -> int:
        if self._mortgaged:
            return 0
        else:
            return self.mortgage_value

    class MortgageStatusError(Error):
        default_message = (
            "Could not mortgage/unmortgage if already mortgated/unmortgaged."
        )

    class InsufficientBalanceError(Error):
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
        game: Game.Game,
    ):
        super().__init__(id, name, value, rent, mortgage_value, game)
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

    def buy_building(self) -> Error:
        if self._mortgaged:
            return self.BuildingOnMortgagedError
        elif self.buildings == 5:
            return self.BuildingOutOfBoundsError
        elif any(other.buildings < self.buildings for other in self.group_list):
            return self.UnequalNumberOfBuildingsError
        elif self.buildings == 4 and self.game.hotels == 0:
            return Game.NoMoreHotels
        elif self.game.houses == 0:
            return Game.NoMoreHouses

        self.buildings += 1
        if self.buildings == 4:
            self.game.houses += 4
            self.game.hotels -= 1
        else:
            self.game.houses += 1
        return Ok(self.building_cost)

    def sell_building(self) -> Result:
        if self.buildings == 0:
            return self.BuildingOutOfBoundsError
        elif any(other.buildings > self.buildings for other in self.group_list):
            return self.UnequalNumberOfBuildingsError

        if self.buildings == 5:
            if self.game.houses < 4:
                return Game.NoMoreHouses
            else:
                self.game.houses -= 4
                self.game.hotels += 1
        else:
            self.game.houses += 1

        self.buildings -= 1
        return Ok(self.building_cost // 2)

    def unmortgage(self) -> Result:
        if any(other.buildings > 0 for other in self.group_list):
            # TODO
            return self.BuildingOnMortgagedError
        return super().unmortgage()

    def liquidate_value(self) -> int:
        total = super().liquidate_value()
        if not self._mortgaged:
            total += self.buildings * self.building_cost // 2
            # TODO: think about the logic for selling all buildings and bank building availability
        return total

    class BuildingOnMortgagedError(Error):
        default_message = "Cannot build buildings on a mortgaged property"

    class BuildingOutOfBoundsError(Error):
        default_message = "Cannot buy or sell another property - would lead to too many or too few buildings."

    class UnequalNumberOfBuildingsError(Error):
        default_message = "Cannot buy or sell another property - would lead to imbalance of buildings in the same group."


class Railroad(Buyable):
    owners: DefaultDict[Player.Player, Set[Railroad]] = defaultdict(set)

    def __init__(
        self,
        id: int,
        name: str,
        value: int,
        rent: List[int],
        mortgage_value: int,
        game: Game.Game,
    ):
        super().__init__(id, name, value, rent, mortgage_value, game)

    def _rent_value(self, multiplier: int) -> int:
        # TODO - need to modify how owners are added
        railroads_owned = len(self.__class__.owners[self.owner])
        return multiplier * self.rent[railroads_owned - 1]


class Utility(Buyable):
    owners: DefaultDict[Player.Player, Set[Utility]] = defaultdict(set)

    def __init__(self, id: int, name: str, value: int, mortgage_value: int, game: Game):
        # Utilities don't have a set rent
        super().__init__(id, name, value, 0, mortgage_value, game)

    def _rent_value(self, multiplier: int) -> int:
        # See TODO - need to modify how owners are added
        # Treat "multiplier" as the dice roll
        utilities_owned = self.__class__.owners[self.owner]
        if utilities_owned == 1:
            return 10 * multiplier
        elif utilities_owned == 2:
            return 4 * multiplier
        else:
            raise ValueError(f"Cannot own {utilities_owned} utilities and charge rent!")


class CardSquare(Square):
    def __init__(self, id: int, name: str, deck: List, game: Game.Game):
        # TODO - make this a circular linkedlist
        super().__init__(id, name, game)

        self.deck: List[Card.Card] = deck

    def execute_action(self, player: Player):
        card = self.deck.pop()
        card.execute(self.game, player)


class Start(Square):
    def execute_action(self, player: Player.Player):
        player.balance += 200


class Tax(Square):
    def __init__(self, id: int, name: str, value: int, game: Game.Game):
        super().__init__(id, name, game)
        self.value = value

    def execute_action(self, player: Player.Player):
        # TODO - should probably just work on the player "-" operator
        player.modify_balance(-self.value, force=True)


class FreeParking(Square):
    def execute_action(self, player: Player.Player):
        # Do nothing
        return
