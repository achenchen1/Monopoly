from __future__ import annotations
from typing import Any

from MonopolyGame.Common import Game


class CmdLineGame(Game.Game):
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
