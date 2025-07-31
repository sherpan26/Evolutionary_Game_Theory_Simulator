import random
from .base_strategy import BaseStrategy, COOPERATE, DEFECT

class Random(BaseStrategy):
    """A strategy that randomly chooses to cooperate or defect."""
    def play(self):
        return random.choice([COOPERATE, DEFECT])