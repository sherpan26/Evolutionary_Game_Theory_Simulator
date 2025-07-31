import itertools
from game_engine import play_game

def run_tournament(strategy_map: dict, rounds: int, noise: float):
    """
    Runs a round-robin tournament for a given set of strategies.

    Each strategy plays one game against every other strategy, including itself.

    Args:
        strategy_map: A dictionary mapping strategy names to their classes.
        rounds: The number of rounds to play in each game.
        noise: The noise level for each game.

    Returns:
        A list of tuples (strategy_name, total_score), sorted by score descending.
    """
    strategy_names = list(strategy_map.keys())
    scores = {name: 0 for name in strategy_names}

    # Generate all unique pairs of strategies for the matchups
    # `combinations_with_replacement` includes games where a strategy plays itself
    matchups = itertools.combinations_with_replacement(strategy_names, 2)

    for name1, name2 in matchups:
        # Get the strategy classes from the map
        Strategy1 = strategy_map[name1]
        Strategy2 = strategy_map[name2]

        # Instantiate fresh strategies for this specific match
        player1 = Strategy1()
        player2 = Strategy2()

        # Run the game
        results = play_game(player1, player2, rounds=rounds, noise=noise)
        score1, score2 = results["final_scores"]

        # Add the scores to the running totals
        scores[name1] += score1
        scores[name2] += score2

    # Sort the strategies by final score in descending order
    leaderboard = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    return leaderboard


# Example usage for direct testing of this file
if __name__ == '__main__':
    from strategies.tit_for_tat import TitForTat
    from strategies.always_cooperate import AlwaysCooperate
    from strategies.always_defect import AlwaysDefect
    from strategies.random_strategy import Random

    # A map of strategies to test
    TEST_STRATEGIES = {
        "Tit for Tat": TitForTat,
        "Always Cooperate": AlwaysCooperate,
        "Always Defect": AlwaysDefect,
        "Random": Random,
    }

    print("Running tournament...")
    final_leaderboard = run_tournament(TEST_STRATEGIES, rounds=100, noise=0.05)
    print("\n--- 🏆 Tournament Leaderboard ---")
    for rank, (name, score) in enumerate(final_leaderboard, 1):
        print(f"#{rank:<3} {name:<20} Score: {score}")