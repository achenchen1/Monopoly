from __future__ import annotations
from typing import List, Sequence
from functools import partial

from MonopolyGame.Common import Game
from MonopolyGame.Common import Square
from MonopolyGame.Utils.DataClasses import Result, Error, Ok


class Player:
    def __init__(self, id: int, game: Game.Game):
        self._id: int = id
        self.square: int = 1
        self.balance: int = 1500
        # self.properties: Set[Square.Buyable] = {}
        self.properties: List[Square.Buyable] = []
        self.get_out_of_jail_cards = []
        self._jailed: int = 0
        self._game: Game.Game = game

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

        if property.unmortgage():
            self.balance -= int(1.1 * property.mortgage_value)

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
                if self.liquidate_value() + self.balance + delta < 0:
                    return ValueError("Insufficient value")

                while self.balance + delta < 0:
                    self.manage(settle_debts=True)
                return Ok
            else:
                return ValueError("Insufficient value")
        else:
            self.balance += delta
        return Ok

    def manage(self, settle_debts: bool = False) -> Sequence[int, Result]:
        """Function to allow player to manage their properties.
        Possible actions include:
            - Mortgaging a Buyable
            - Unmortgaging a Buyable
            - Building/destroying a building on a Property

        :param settle_debts: whether or not this function is being called to settle debts the player has incurred (e.g. due to a large amount of rent) defaults to False
        :type settle_debts: bool, optional
        :return: _description_ TODO
        :rtype: Sequence[int, Result]
        """
        # TODO - choice should be checked to ensure type safety.
        # TODO - properties should display number of houses/hotels
        # TODO - "print" isn't going to work for all interfaces.
        print(self.list_properties())
        print(self.balance)
        managing = self.properties[
            int(
                input(
                    "\n".join(f"{i}: {j}" for i, j in enumerate(self.properties)) + "\n"
                )
            )
        ]

        choices = ["Do nothing"]
        choice_mappings = {
            "Mortgage": partial(self.mortgage_buyable, managing),
            "Unmortgage": partial(self.unmortgage_buyable, managing),
            "Do nothing": lambda: None,
        }
        if managing._mortgaged:
            if settle_debts:
                print(
                    "Property being managed is mortgaged; cannot be used to settle debts"
                )
                # TODO return value
                return
            elif self.balance < int(1.1 * managing.mortgage_value):
                print("Property is mortgaged and insufficient balance to unmortgage")
                # TODO return value
                return
            else:
                choices.append("Unmortgage")
        else:
            # print(choice.group)
            # print(choice.group_list)

            # TODO - no action required, just to come back to this - technically, if a property in the group has a building,
            #   but the property with a building is not owned by the player, then this is going to run some risks. However,
            #   that should be undefined behavior (as we shouldn't have another property in the same group both possessing
            #   buildings and owned by someone else)
            if type(managing) == Square.Property:
                # Mortgaging logic
                if all(i.buildings == 0 for i in managing.group_list):
                    choices.append("Mortgage")

                min_buildings = min(managing.group_list, key=lambda p: p.buildings)
                max_buildings = max(managing.group_list, key=lambda p: p.buildings)

                # TODO - global check for houses/hotels left
                if (
                    not settle_debts
                    and managing.buildings == min_buildings
                    and managing.buildings < 5
                ):
                    choices.append("Buy building")
                # TODO - global check for houses/hotels left
                if managing.buildings == max_buildings and managing.buildings > 0:
                    choices.append("Sell building")

                choice_mappings["Buy building"] = managing.buy_building
                choice_mappings["Sell building"] = managing.sell_building
            else:
                # Utilities, railroads
                choices.append("Mortgage")

        choice = input(", ".join(choices) + "\n> ")
        return choice_mappings[choice]()

        # TODO: shoudl return a Result
        # TODO: devise an interface that allows list_properties from Game (or move list_properties here, which probably makes more sense)
        # TODO: function that loops until player ends. Allows players to modify properties and whatnot.
        # Returns True if all decisions are finalized, False otherwise. (if False, should roll back change.)

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
        self.modify_balance(-rent_value)

    class OwnershipError(Result):
        default_message = "Property not owned by player."
