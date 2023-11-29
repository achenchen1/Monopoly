from __future__ import annotations
from Result import Result
from typing import Optional, Sequence

import json
import Square
import Player

chance_cards = []
houses = 0
hotels = 0


class GlobalError(Result):
    pass


class NoMoreHouses(GlobalError):
    default_message = "No more houses left in the game."


class NoMoreHotels(GlobalError):
    default_message = "No more hotels left in the game."

def importer(input_file, squares, chance, community_chest):
    with open(input_file, "r") as f:
        j = json.load(f)
        for k, v in j.items():
            match v['type']:
                case 'S':
                    squares.append(Square.Start(k, v['name']))
                case 'P':
                    squares.append(Square.Property(k, v['name'], v['group'], v['value'], v['rent'], v['building_cost'], v['mortgage_value']))
                case 'R':
                    squares.append(Square.Railroad(k, v['name'], v['value'], v['rent'], v['mortgage_value']))
                case 'T':
                    squares.append(Square.Tax(k, v['name'], v['value']))
                case 'CC':
                    squares.append(Square.Card(k, v['name'], community_chest))
                case 'CH':
                    squares.append(Square.Card(k, v['name'], chance))
                case "F":
                    # TODO will raise a notimplementederror
                    squares.append(Square.Square(k, v['name']))
                case "G":
                    # TODO will raise a notimplementederror
                    squares.append(Square.Square(k, v['name']))


class Game:
    def __init__(self) -> None:
        self.players = []

    def auction(self, property: Square.Buyable, starting_player: Player = None) -> Optional[Player.Player]:
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


if __name__ == "__main__":
    squares = []
    chance = ["Chance"]
    community_chest = ["Community Chest"]
    importer("/Users/alexchen/Projects/Monopoly/resources/squares.json", squares, chance, community_chest)
    print('\n'.join([str(i) for i in squares]))