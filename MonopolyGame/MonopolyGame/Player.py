from __future__ import annotations
from typing import Set, Tuple

import Global
import Result
import Square


class Player:
    def __init__(self, id: int, color: Tuple[int] = tuple()):
        self._id: int = id
        self.square: int = 1
        self.balance: int = 1500
        self.properties: Set[Square.Buyable] = {}
        self._jailed: int = 0
        self._hex_color: Tuple[int] = color

    # Buying choices
    def buy_square(self, property: Square.Buyable) -> bool:
        choice = ""
        if self.balance >= property.value:
            while choice not in ["Y", "N"]:
                choice = input("Want to buy? Y/N\n")

            return choice == "Y"
        else:
            while self.balance < property.value:
                while choice.lower() not in ["Y", "N"]:
                    choice = input(
                        "Insufficient funds to buy; want to manage assets? Y/N\n"
                    )
                    if choice == "Y":
                        raise NotImplementedError
                    return False

        return False

    # Building choices
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

    # Mortgaging/unmortgaging
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

    def pay_rent(self, rent_value: int):
        if self.balance < rent_value:
            raise NotImplementedError
        else:
            self.balance -= rent_value

    class OwnershipError(Result.Result):
        default_message = "Property not owned by player."
