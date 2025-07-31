from abc import ABC, abstractmethod

# Define moves for clarity and to avoid magic strings
COOPERATE = 'C'
DEFECT = 'D'

class BaseStrategy(ABC):
    """
    Abstract base class for all Iterated Prisoner's Dilemma strategies.
    """
    def __init__(self):
        self.my_history = []
        self.opponent_history = []

    def record_round(self, my_move, opponent_move):
        """Records the moves from the current round."""
        self.my_history.append(my_move)
        self.opponent_history.append(opponent_move)

    def reset(self):
        """Resets the history for a new match."""
        self.my_history = []
        self.opponent_history = []

    @abstractmethod
    def play(self):
        """
        Determines the strategy's next move.
        Must be implemented by all subclasses.

        Returns:
            str: 'C' for Cooperate or 'D' for Defect.
        """
        pass