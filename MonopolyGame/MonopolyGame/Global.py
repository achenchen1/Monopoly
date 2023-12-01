from __future__ import annotations
import random
import json
from .Result import Result
from typing import Optional, Sequence, List, Tuple

from . import Square
from . import Player
from . import Utils


class GlobalError(Result):
    pass


class NoMoreHouses(GlobalError):
    default_message = "No more houses left in the game."


class NoMoreHotels(GlobalError):
    default_message = "No more hotels left in the game."


def importer(input_file, squares, chance, community_chest, game):
    # TODO: type hinting
    with open(input_file, "r") as f:
        j = json.load(f)
        for k, v in j.items():
            k = int(k)
            match v["type"]:
                case "S":
                    squares.append(Square.Start(k, v["name"], game))
                case "P":
                    squares.append(
                        Square.Property(
                            k,
                            v["name"],
                            v["group"],
                            v["value"],
                            v["rent"],
                            v["building_cost"],
                            v["mortgage_value"],
                            game,
                        )
                    )
                case "R":
                    squares.append(
                        Square.Railroad(
                            k,
                            v["name"],
                            v["value"],
                            v["rent"],
                            v["mortgage_value"],
                            game,
                        )
                    )
                case "T":
                    squares.append(Square.Tax(k, v["name"], v["value"], game))
                case "CC":
                    squares.append(
                        Square.CardSquare(k, v["name"], community_chest, game)
                    )
                case "CH":
                    squares.append(Square.CardSquare(k, v["name"], chance, game))
                case "F":
                    squares.append(Square.FreeParking(k, v["name"], game))
                case "G":
                    # TODO will raise a notimplementederror
                    squares.append(Square.Square(k, v["name"], game))


class Game:
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
        self.colors = {
            "Brown": (139, 69, 19),
            "Light Blue": (173, 216, 230),
            "Pink": (255, 105, 180),
            "Orange": (255, 140, 0),
            "Red": (255, 0, 0),
            "Yellow": (255, 215, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 35, 102),
        }

    def auction(
        self, property: Square.Buyable, starting_player: Player = None
    ) -> Optional[Player.Player]:
        players_in_auction = Utils.Ring(self.players)
        players_in_auction.set_head(starting_player)
        bid_price = 1
        winner = None

        if type(property) == Square.Property:
            colors = self.colors[property.group]
            print(
                f"Bidding on \033[48;2;{colors[0]};{colors[1]};{colors[2]}m{property.name}\033[0m\n"
            )
        for p in players_in_auction:
            player_choice = input(
                f"\033[38;2;{p._hex_color[0]};{p._hex_color[1]};{p._hex_color[2]}mPlayer {p._id}\033[0m: current bid is {bid_price}. Enter new bid or select 'N'.\n"
            )

            if player_choice == "N":
                players_in_auction.pop(p)
            elif (new_bid := int(player_choice)) <= p.balance:
                if new_bid > bid_price:
                    bid_price = new_bid
                    winner = p
            else:
                raise NotImplementedError

        return winner

    def trade(
        self,
        l: Player,
        r: Player,
        l_assets: Sequence[int, Square.Buyable],
        r_assets: Sequence[int, Square.Buyable],
    ):
        # TODO
        pass

    def add_player(self, id: int, color: Tuple[int]) -> Player.Player:
        player = Player.Player(id, color)
        self.players.append(player)
        self.player_positions[player] = 0
        return player

    def show_menu(self, player, rolled: bool = False):
        choices = ["Manage", "Trade"]
        if not rolled:
            choices.append("Roll")

        action = None
        while action not in choices:
            action = input(
                f"\033[38;2;{player._hex_color[0]};{player._hex_color[1]};{player._hex_color[2]}mChoose an action: {', '.join(choices)}\033[0m\n"
            )

        # TODO
        match action:
            case "Manage":
                # TODO: need to not cycle to next player
                print("Properties:")
                # TODO: make these colors print from the objects themselves
                properties = []
                for p in sorted(player.properties, key=lambda x: x.id):
                    if type(p) == Square.Property:
                        colors = self.colors[p.group]
                        properties.append(
                            f"\033[48;2;{colors[0]};{colors[1]};{colors[2]}m{p.name}\033[0m"
                        )
                    else:
                        properties.append(f"{p.name}")
                print(", ".join(properties))
            case "Trade":
                for p in player.properties:
                    print(p)
            case "Roll":
                if not rolled:
                    self.roll_and_move(player)
            case _:
                raise ValueError

    def roll_and_move(self, player: Player.Player):
        if not player._jailed:
            dice_emojis = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)
            total_roll = dice_1 + dice_2
            print(f"Rolled a {dice_emojis[dice_1]} and a {dice_emojis[dice_2]}")

            self.player_positions[player] = (
                self.player_positions[player] + total_roll
            ) % len(self.squares)
            print(f"New position: {self.player_positions[player]}")
            if (
                type(s := self.squares[self.player_positions[player]])
                == Square.Property
            ):
                colors = self.colors[s.group]
                print(
                    f"\033[48;2;{colors[0]};{colors[1]};{colors[2]}m{self.squares[self.player_positions[player]].name}\033[0m\n"
                )
            else:
                print(self.squares[self.player_positions[player]].name)
            self.squares[self.player_positions[player]].execute_action(player)
