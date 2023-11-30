from __future__ import annotations
import random
import json
from Result import Result
from typing import Optional, Sequence, List, Tuple

import Card
import Square
import Player


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
            match v["type"]:
                case "S":
                    squares.append(Square.Start(k, v["name"]))
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
                        )
                    )
                case "R":
                    squares.append(
                        Square.Railroad(
                            k, v["name"], v["value"], v["rent"], v["mortgage_value"]
                        )
                    )
                case "T":
                    squares.append(Square.Tax(k, v["name"], v["value"]))
                case "CC":
                    squares.append(
                        Square.CardSquare(k, v["name"], community_chest, game)
                    )
                case "CH":
                    squares.append(Square.CardSquare(k, v["name"], chance, game))
                case "F":
                    # TODO will raise a notimplementederror
                    squares.append(Square.Square(k, v["name"]))
                case "G":
                    # TODO will raise a notimplementederror
                    squares.append(Square.Square(k, v["name"]))


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
        # TODO
        # players_left = len(self.players)
        # players_list = self._game.players.copy()
        # current_value = 1

        # if starting_player is not None:
        #     current_player = players_list.index(starting_player)
        # else:
        #     current_player = 0

        # while players_left > 0:
        #     response: str = input(f"Current to bid on {property.name} is {current_value}")
        #     if response == 'N':
        #         players_left -= 1
        #         players_list

        return starting_player

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
                for p in player.properties:
                    print(p)
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


if __name__ == "__main__":
    squares = []
    chance = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    community_chest = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    game = Game(squares, chance, community_chest)
    importer(
        "/Users/alexchen/Projects/Monopoly/resources/squares.json",
        squares,
        chance,
        community_chest,
        game,
    )
    player = game.add_player(0, (33, 150, 243))
    player = game.add_player(1, (226, 50, 107))
    while len(game.players) > 1:
        for p in game.players:
            game.show_menu(p)
    # print("\n".join([str(i) for i in squares]))
