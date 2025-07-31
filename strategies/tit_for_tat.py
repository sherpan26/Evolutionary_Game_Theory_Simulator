from .base_strategy import BaseStrategy, COOPERATE, DEFECT

class TitForTat(BaseStrategy):
    """
    Starts by cooperating, then mirrors the opponent's last move.
    """
    def play(self):
        if not self.opponent_history:
            return COOPERATE  # Cooperate on the first move
        return self.opponent_history[-1]  # Copy opponent's previous move