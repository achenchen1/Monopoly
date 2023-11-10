from Square import Property
from typing import Dict

class Player:
    def __init__(self):
        self.square: int = 1
        self.balance: int = 1500
        self.properties: Dict[Property] = {}
        self._jailed: int = 0
    
    def roll_and_move(self):
        pass
