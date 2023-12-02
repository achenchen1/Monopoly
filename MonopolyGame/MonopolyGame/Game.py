from __future__ import annotations
import random

from typing import Optional, Sequence, List, Any

from . import Card
from . import Square
from . import Player
from . import Utils
from . import Result


class GlobalError(Result.Result):
    pass


class NoMoreHouses(GlobalError):
    default_message = "No more houses left in the game."


class NoMoreHotels(GlobalError):
    default_message = "No more hotels left in the game."


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
        players_in_auction = Utils.Ring(self.players)
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

    def show_menu(self, player: Player.Player, rolled: bool = False) -> bool:
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

        match action:
            case "Manage":
                self.player_output(self.list_properties(player))
            case "Trade":
                self.player_output(self.list_properties(player))
            case "Roll":
                if not rolled:
                    self.roll_and_move(player)
                    return True
            case "End Turn":
                # TODO - just because we rolled, doesn't mean we're done the turn
                if not rolled:
                    return False
                return True
            case _:
                return False

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


class CmdLineGame(Game):
    game_strings = {
        "auction_property_string": "Bidding on {}.",
        "auction_string": "{}: current bid is {}. Enter new bid or select 'N'.",
        "choose_action_string": "{}: Choose an action out of {}",
        "dice_string": "Rolled a {} and a {}.",
        "position_string": "New position: {}.",
        "new_position_string": "Landed on {}.",
    }

    def update_square_colors(self):
        square_colors = {
            "Brown": (48, 139, 69, 19),
            "Light Blue": (48, 173, 216, 230),
            "Pink": (48, 255, 105, 180),
            "Orange": (48, 255, 140, 0),
            "Red": (48, 255, 0, 0),
            "Yellow": (48, 255, 215, 0),
            "Green": (48, 0, 255, 0),
            "Blue": (48, 0, 35, 102),
        }

        for square in self.squares:
            if hasattr(square, "group") and square.group in square_colors:
                square._hex_color = square_colors[square.group]

    @staticmethod
    def font_formatter(arg: Any) -> str:
        if hasattr(arg, "_hex_color"):
            if len(arg._hex_color) == 4:
                prefix = "\033[{};2;{};{};{}m".format(*arg._hex_color)
            else:
                prefix = "\033[38;2;{};{};{}m".format(*arg._hex_color)
            suffix = "\033[0m"
            return prefix + str(arg) + suffix
        return str(arg)

    @staticmethod
    def player_output(prompt: str) -> None:
        print(prompt)
        return

    @staticmethod
    def player_input() -> None:
        player_input = input("> ")

        if player_input == "N":
            player_input = False
        elif player_input == "Y":
            player_input = True

        return player_input

    def list_properties(self, player: Player.Player) -> str:
        properties = []
        for p in sorted(player.properties, key=lambda x: x.id):
            properties.append(self.font_formatter(p))
        return f"Properties: {', '.join(properties)}"

    def add_players(self, num_players: int = 1) -> List[Player.Player]:
        player_colors = [(33, 150, 243), (226, 50, 107)]

        offset = len(self.players)
        new_players = super().add_players(num_players)

        for i, new_player in enumerate(new_players):
            new_player._hex_color = player_colors[i + offset]

        return new_players
