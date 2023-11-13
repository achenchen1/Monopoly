from __future__ import annotations
from typing import Sequence, Set

import Global
import Result
import Square


class Player:
    def __init__(self, id):
        self._id: int = id
        self.square: int = 1
        self.balance: int = 1500
        self.properties: Set[Square.Buyable] = {}
        self._jailed: int = 0

    def buy_building(self, property: Square.Property) -> Result.Error:
        if property not in self.properties:
            return Player.OwnershipError

        if self.balance >= property.building_cost:
            result = property.buy_building()
            if result:
                self.balance -= property.building_cost
            else:
                raise NotImplementedError

    def sell_building(self, property: Square.Property):
        if property not in self.properties:
            return Player.OwnershipError

        if result := property.sell_building():
            return Result.Ok
        elif result == Global.NoMoreHouses:
            raise NotImplementedError("Need to add a 'force sell' function")
        else:
            return result

    def mortgage_buyable(self, property: Square.Buyable):
        if property not in self.properties:
            return Player.OwnershipError

        if property.mortgage():
            self.balance += property.mortgage_value

    def unmortgage_buyable(self, property: Square.Buyable):
        if property not in self.properties:
            return Player.OwnershipError

        if property.unmortgage(self.balance):
            self.balance -= 1.1 * property.mortgage_value

    def trade(
        self,
        them: Player,
        self_assets: Sequence[int, Square.Buyable],
        them_assets: Sequence[int, Square.Buyable],
    ):
        # TODO
        pass

    def _buy(self, property: Square.Buyable):
        pass

    def _roll_and_move(self):
        pass

    class OwnershipError(Result.Result):
        default_message = "Property not owned by player."
