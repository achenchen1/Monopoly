from typing import List
from Player import Player

class Square:
    def __init__(self, id: int):
        self.id: int = id
        self.owner: Player = None
    
    def execute_action(self, player: Player):
        raise NotImplementedError
    
class Property(Square):
    def __init__(self, id: int, name: str, rents: List[int], values: List[int]):
        super().__init__(id)
        self.name = name
        self.rents = rents
        self.values = values
    
    def execute_action(self, player: Player):
        if self.owner is None:
            self.offer(player)
        elif self.owner != player:
            self.charge_rent(player)
    
    def offer(self, player: Player):
        pass

    def charge_rent(self, player: Player):
        pass