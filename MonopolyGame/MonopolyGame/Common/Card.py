from __future__ import annotations

from MonopolyGame.Common import Player
from MonopolyGame.Common import Game
from MonopolyGame.Common import Square


class Card:
    def __init__(self, name: str, description: str) -> None:
        # TODO : type hinting
        self.name: str = name
        self.description = description

    def execute(self, game: Game.Game, player: Player.Player) -> None:
        print(
            f"\033[38;2;{player._hex_color[0]};{player._hex_color[1]};{player._hex_color[2]}mLanded on \033[0m'{self.name}'!\n"
        )


class GoToGo(Card):
    def execute(self, game: Game.Game, player: Player.Player) -> None:
        start_position = 0
        while start_position < len(game.squares) and not isinstance(game.squares[start_position], Square.Start):
            start_position += 1

        game.player_positions[player] = start_position
        game.squares[start_position].execute_action(player)
