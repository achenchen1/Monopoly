from __future__ import annotations
import random

from typing import Optional, Sequence, List, Any

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
        self.players = []
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
        bid_price = 1
        winner = None

        property_string = self.__class__.game_strings["auction_property_string"].format(
            self.font_formatter(property)
        )
        self.player_output(property_string)

        for p in players_in_auction:
            auction_string = self.__class__.game_strings["auction_string"].format(
                self.font_formatter(p), bid_price
            )
            self.player_output(auction_string)
            player_choice = self.player_input()

            if player_choice is False:
                # For input validation - specifically check if it's False, not just Falsey
                players_in_auction.pop(p)
            elif (new_bid := int(player_choice)) <= p.balance:
                if new_bid > bid_price:
                    bid_price = new_bid
                    winner = p
            else:
                raise NotImplementedError

        return winner

    @staticmethod
    def font_formatter(arg: Any) -> str:
        return str(arg)

    @staticmethod
    def player_output(prompt: str) -> None:
        raise NotImplementedError

    @staticmethod
    def player_input() -> None:
        raise NotImplementedError

    def list_properties(self, player: Player.Player) -> None:
        raise NotImplementedError

    def add_players(self, num_players: int = 1) -> List[Player.Player]:
        if num_players < 1:
            raise ValueError(
                f"Can't add {num_players} players - num_players must be >= 1."
            )

        new_players = []
        for i in range(num_players):
            player = Player.Player(i + len(self.players))
            new_players.append(player)
            self.players.append(player)
            self.player_positions[player] = 0
        return new_players

    def trade(
        self,
        l: Player,
        r: Player,
        l_assets: Sequence[int, Square.Buyable],
        r_assets: Sequence[int, Square.Buyable],
    ):
        # TODO
        pass

    def show_menu(self, player: Player.Player, rolled: bool = False) -> Result:
        choices = ["Manage", "Trade", "End Turn"]
        if not rolled:
            choices.append("Roll")

        action = None
        while action not in choices:
            choice_string = self.__class__.game_strings["choose_action_string"].format(
                self.font_formatter(player), ", ".join(choices)
            )
            self.player_output(choice_string)
            action = self.player_input()
            # TODO - should we be exiting here? like below?
            # return Error(f"Don't recognize choice: '{action}'")

        match action:
            case "Manage":
                self.player_output(self.list_properties(player))
                return Ok("Manage called")
            case "Trade":
                self.player_output(self.list_properties(player))
                return Ok("Trade called")
            case "Roll":
                if not rolled:
                    self.roll_and_move(player)
                    return Rolled()
            case "End Turn":
                if not rolled:
                    return Error("Can't end a turn without rolling.")
                return TurnOver()
            case _:
                raise ValueError(f"Unrecognized action {action}")

    def roll_and_move(self, player: Player.Player):
        if not player._jailed:
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            total_roll = dice_1 + dice_2
            self.player_output("Test")
            self.player_output(
                self.__class__.game_strings["dice_string"].format(dice_1, dice_2)
            )

            self.player_positions[player] = (
                self.player_positions[player] + total_roll
            ) % len(self.squares)
            self.player_output(
                self.__class__.game_strings["position_string"].format(
                    self.player_positions[player]
                )
            )

            square = self.squares[self.player_positions[player]]
            self.player_output(
                self.__class__.game_strings["new_position_string"].format(
                    self.font_formatter(square)
                )
            )
            square.execute_action(player)
