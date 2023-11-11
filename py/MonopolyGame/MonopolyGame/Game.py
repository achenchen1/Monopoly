from __future__ import annotations
from typing import Dict, List


class Player:
    def __init__(self):
        self.square: int = 1
        self.balance: int = 1500
        self.properties: Dict[Property] = {}
        self._jailed: int = 0

    def roll_and_move(self):
        pass

    def _buy(self, property: Property):
        print(Property.owner)


class Square:
    def __init__(self, id: int):
        self.id: int = id
        self.owner: Player = None

    def execute_action(self, player: Player):
        raise NotImplementedError


class Property(Square):
    def __init__(self, id: int, name: str, rents: List[int], values):
        super().__init__(self, id)
        self.name: str = name
        self.rents: List[int] = rents  # How much each tier costs - houses, e.g.
        self.value: int = values  # How much this property costs
        self.owner: Player = None

    def execute_action(self, player: Player, multiplier: int = 1):
        if self.owner is None:
            self._offer(player)
        elif self.owner != player:
            self._charge_rent(player, multiplier)

    def unmortgage(self) -> bool:
        # Just 1.1*mortgage price
        pass

    def build_building(self):
        pass

    def sell_building(self):
        pass

    def _offer(self, player: Player):
        if player._buy(self):
            self.owner = player
        else:
            self.owner = Player.auction(self)

    def _charge_rent(self, player: Player, multiplier: int):
        pass


class Railroad(Property):
    _railroad_to_owner: Dict[Railroad, Player] = {}
    _owner_to_railroad: Dict[Player, bool] = {}

    def _charge_rent(self, player: Player, multiplier: int):
        rent = self.rent[
            len(Railroad._owner_to_railroad[Railroad._railroad_to_owner[self]]) - 1
        ]
        player.charge(rent * multiplier)

    def _offer(self, player: Player):
        super()._offer(self, player)
        Railroad._railroad_to_owner[self] = player
        Railroad._owner_to_railroad[player] = self


class Utility(Property):
    pass


def importer(json: Dict):
    pass
