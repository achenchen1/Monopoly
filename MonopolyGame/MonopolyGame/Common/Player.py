from __future__ import annotations
from typing import List, Sequence

from MonopolyGame.Common import Game
from MonopolyGame.Common import Square
from MonopolyGame.Utils.DataClasses import Result, Error, Ok


class Player:
    def __init__(self, id: int):
        self._id: int = id
        self.square: int = 1
        self.balance: int = 1500
        # self.properties: Set[Square.Buyable] = {}
        self.properties: List[Square.Buyable] = []
        self.get_out_of_jail_cards = []
        self._jailed: int = 0

    def __repr__(self) -> str:
        return f"Player {self._id}"

    # Buying choices
    def buy_square(self, property: Square.Buyable) -> bool:
        choice = ""
        if self.balance >= property.value:
            while choice not in ["Y", "N"]:
                choice = input("Want to buy? Y/N\n> ")

            return choice == "Y"
        else:
            while self.balance < property.value:
                while choice.lower() not in ["Y", "N"]:
                    choice = input(
                        "Insufficient funds to buy; want to manage assets? Y/N\n> "
                    )
                    if choice == "Y":
                        raise NotImplementedError
                    return False

        return False

    # Building choices
    def buy_building(self, property: Square.Property) -> Error:
        if property not in self.properties:
            return Player.OwnershipError

        if self.balance >= property.building_cost:
            result = property.buy_building()
            if result:
                self.balance -= result.value
            else:
                raise NotImplementedError

    def sell_building(self, property: Square.Property):
        # TODO - we don't increment the player's cash lmao
        if property not in self.properties:
            return Player.OwnershipError

        if result := property.sell_building():
            self.balance += result.value
            return Ok
        elif result == Game.NoMoreHouses:
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

    def modify_balance(self, delta: int, force: bool = True):
        """Safe function used to modify the player's balance

        :param delta: The amount to add (positive) or subtract (negative) to the player's balance
        :type delta: int
        :param force: whether or not this is a forcing transaction. For example, game taxes are forcing. Defaults to True
        :type force: bool, optional
        :raises ValueError: TODO - maybe should be a separate error type.
        """
        if self.balance + delta < 0:
            if force:
                while self.balance + delta < 0:
                    self.manage()
                return Ok
            return ValueError("Insufficient value")
        else:
            self.balance += delta
        return Ok

    def manage(self) -> Sequence[int, Result]:
        # TODO - choice should be checked to ensure type safety.
        # TODO - properties should display number of houses/hotels
        # TODO - "print" isn't going to work for all interfaces.
        print(self.list_properties())
        print(self.balance)
        choice = int(input("\n".join(f"{i}: {j}" for i, j in enumerate(self.properties)) + "\n"))
        

        # import pdb
        # pdb.set_trace()
        # TODO: shoudl return a Result
        # TODO: devise an interface that allows list_properties from Game (or move list_properties here, which probably makes more sense)
        # TODO: function that loops until player ends. Allows players to modify properties and whatnot.
        # Returns True if all decisions are finalized, False otherwise. (if False, should roll back change.)
        pass

    def bankrupt(self, receiving_player: Player = None):
        # Plan to implement this:
        # Go barebones.
        # * if bank is receiving player, auction everything.
        # * if another player is receiving player, do the normal mortgage thing.
        # * THE CORNER CASE THAT THE SUBSEQUENT PLAYER CANNOT PAY: technically, bank should auction everythign.
        #   This requires that the subsequent player be given the chance to unmortgage selectively first.
        pass

    def liquidate_value(self) -> int:
        total = 0
        for b in self.properties:
            total += b.liquidate_value()
            # TODO

        return total

    def pay_rent(self, rent_value: int):
        # TODO - according to official rules, the owner of the property must point out the player owes rent. Something to consider.
        if self.balance < rent_value:
            raise NotImplementedError
        else:
            self.balance -= rent_value

    class OwnershipError(Result):
        default_message = "Property not owned by player."
