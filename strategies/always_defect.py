from .base_strategy import BaseStrategy, DEFECT

class AlwaysDefect(BaseStrategy):
    """A simple strategy that always defects."""
    def play(self):
        return DEFECT