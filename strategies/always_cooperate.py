from .base_strategy import BaseStrategy, COOPERATE

class AlwaysCooperate(BaseStrategy):
    """A simple strategy that always cooperates."""
    def play(self):
        return COOPERATE