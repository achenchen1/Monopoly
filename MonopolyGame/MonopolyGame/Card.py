from __future__ import annotations

import Player
import Global


class Card:
    def __init__(self, name, description) -> None:
        # TODO : type hinting
        self.name = name
        self.description = description

    def execute(self, game: Global.Game, player: Player.Player) -> None:
        print(
            f"\033[38;2;{player._hex_color[0]};{player._hex_color[1]};{player._hex_color[2]}mLanded on \033[0m'{self.name}'!\n"
        )


class GoToGo(Card):
    def execute(self, game: Global.Game, player: Player.Player) -> None:
        # TODO: is GO always 0?
        game.player_positions[player] = 0
        game.squares[0].execute_action(player)
