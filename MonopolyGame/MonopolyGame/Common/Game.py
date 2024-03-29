from __future__ import annotations
import random

from typing import Optional, Sequence, List, Any, Tuple

from MonopolyGame.Utils.DataClasses import Ring
from MonopolyGame.Common import Square
from MonopolyGame.Common import Player
from MonopolyGame.Utils.DataClasses import Result, Ok, Error


class NoMoreHouses(Error):
    default_message = "No more houses left in the game."


class NoMoreHotels(Error):
    default_message = "No more hotels left in the game."


class TurnOver(Ok):
    default_message = "End turn."


class Rolled(Ok):
    pass


class Game:
    game_strings = {}

    def __init__(
        self,
        squares: List[Square.Square],
        chance_cards: List,
        community_chest_cards: List,
    ) -> None:
        self.players: List[Player.Player] = []
        self.squares = squares
        # TODO: Ring buffer
        self.chance_cards = chance_cards
        self.community_chest_cards = community_chest_cards

        self.player_positions = {}

        self.houses = 0
        self.hotels = 0

    def auction(
        self, property: Square.Buyable, starting_player: Player = None
    ) -> Optional[Player.Player]:
        players_in_auction = Ring(self.players)
        players_in_auction.set_head(starting_player)
        bid_price = 0
        winner = None

        property_string = self.__class__.game_strings["auction_property_string"].format(
            self.font_formatter(property)
        )
        # self.player_output(property_string)
        print(property_string)

        for p in players_in_auction:
            # I/O fragment
            auction_string = self.__class__.game_strings["auction_string"].format(
                self.font_formatter(p), bid_price
            )
            # self.player_output(auction_string)
            # player_choice = self.player_input()
            print(auction_string)
            player_choice = input()

            if player_choice == "N":
                # For input validation - specifically check if it's False, not just Falsey
                players_in_auction.pop(p)
            elif (new_bid := int(player_choice)) <= p.balance:
                if new_bid > bid_price:
                    bid_price = new_bid
                    winner = p
            else:
                raise NotImplementedError

            if len(players_in_auction) == 1 and winner is not None:
                return winner, bid_price

        return winner, bid_price

    @staticmethod
    def font_formatter(arg: Any) -> str:
        return str(arg)

    # I/O fragment
    # @staticmethod
    # def player_output(prompt: str) -> None:
    #     raise NotImplementedError

    # I/O fragment
    # @staticmethod
    # def player_input() -> None:
    #     raise NotImplementedError

    def add_players(self, num_players: int = 1) -> List[Player.Player]:
        if num_players < 1:
            raise ValueError(
                f"Can't add {num_players} players - num_players must be >= 1."
            )

        new_players = []
        for i in range(num_players):
            player = Player.Player(i, self)
            new_players.append(player)
            self.players.append(player)
            self.player_positions[player] = 0
        return new_players

    def trade(self, trading_player):
        formatted_eligible_players = [
            f"{p._id}: {self.font_formatter(p)}"
            for p in sorted(self.players, key=lambda x: x._id)
            if p != trading_player
        ]

        id_to_players = {str(p._id): p for p in self.players if p != trading_player}
        player = None

        while str(player) not in id_to_players:
            player = input(
                "Choose a player in the game:\n{}\n".format(
                    "\n".join(formatted_eligible_players)
                )
            )

        return player

    def show_menu(self, player: Player.Player, rolled: bool = False) -> Result:
        choices = ["Manage", "Trade", "End Turn"]
        if (
            player._jailed > 0
        ):  # TODO: change $50 to be "rule agnostic" (i.e. allow different values)
            choices = ["Pay $50 fine"]
            if len(player.get_out_of_jail_cards) > 0:
                choices.append("Use card")
        if not rolled:
            choices.append("Roll")

        action = None
        while action not in choices:
            choice_string = self.__class__.game_strings["choose_action_string"].format(
                self.font_formatter(player), ", ".join(choices)
            )
            # I/O fragment
            # self.player_output(choice_string)
            # self.player_output("Balance: " + str(player.balance))
            # action = self.player_input()
            print(choice_string)
            print("Balance: " + str(player.balance))
            action = input()

            # TODO - should we be exiting here? like below?
            # return Error(f"Don't recognize choice: '{action}'")

        match action:  # We can safely match action here, as we check action validity in the chunk of code above
            # Non-jail
            case "Manage":
                player.manage()
                return Ok("Manage called")
            case "Trade":
                # I/O fragment
                # self.player_output(self.list_properties(player))
                print(player.list_properties())
                self.trade(player)
                return Ok("Trade called")
            case "Roll":
                if not rolled:
                    roll = self.roll()
                    if player._jailed:
                        self.jail_roll(player, roll)
                    else:
                        self.move(player, sum(roll))
                    return Rolled()
            case "End Turn":
                if not rolled:
                    return Error("Can't end a turn without rolling.")
                return TurnOver()
            # Jail
            case _:
                raise ValueError(f"Unrecognized action {action}")

    def roll(self):
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        # I/O fragment
        # self.player_output(
        #     self.__class__.game_strings["dice_string"].format(dice_1, dice_2)
        # )
        print(self.__class__.game_strings["dice_string"].format(dice_1, dice_2))

        return dice_1, dice_2

    def move(self, player: Player.Player, total_roll: int):
        self.player_positions[player] = (
            self.player_positions[player] + total_roll
        ) % len(self.squares)
        # self.player_output(
        #     self.__class__.game_strings["position_string"].format(
        #         self.player_positions[player]
        #     )
        # )
        # I/O fragment
        print(
            self.__class__.game_strings["position_string"].format(
                self.player_positions[player]
            )
        )

        square = self.squares[self.player_positions[player]]
        # I/O fragment
        # self.player_output(
        print(
            self.__class__.game_strings["new_position_string"].format(
                self.font_formatter(square)
            )
        )
        square.execute_action(player)

    def jail_roll(self, player: Player.Player, rolls: Tuple[int]):
        if rolls[0] == rolls[1]:
            self.move(player, sum(rolls))
            player._jailed == 0
        else:
            if player._jailed == 1:
                player.balance -= 50  # TODO: add player balance minus operator
                self.move(player, sum(rolls))
                player._jailed = 0
            else:
                player._jailed -= 1
