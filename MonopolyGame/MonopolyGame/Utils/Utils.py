from __future__ import annotations
import json

from MonopolyGame.Common import Square


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
