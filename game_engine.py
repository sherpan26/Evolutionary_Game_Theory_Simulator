from strategies.base_strategy import COOPERATE, DEFECT

# classic IPD payoff matrix (T, R, P, S) = (5, 3, 1, 0)
PAYOFFS = {
    (COOPERATE, COOPERATE): (3, 3),
    (COOPERATE, DEFECT):    (0, 5),
    (DEFECT, COOPERATE):    (5, 0),
    (DEFECT, DEFECT):       (1, 1),
}

def play_game(player1, player2, rounds: int = 100, noise: float = 0.0):
    """
    Plays Iterated Prisoner's Dilemma between two strategy instances.

    Returns:
        {
          "final_scores": (p1_score, p2_score),
          "score_history": [(p1_total, p2_total), ...],
          "move_history": [(p1_move, p2_move), ...],
        }
    """
    p1_score = 0
    p2_score = 0
    score_history = []
    move_history = []

    for _ in range(rounds):
        m1 = player1.choose_action()
        m2 = player2.choose_action()
        if noise > 0:
            import random
            if random.random() < noise:
                m1 = COOPERATE if m1 == DEFECT else DEFECT
            if random.random() < noise:
                m2 = COOPERATE if m2 == DEFECT else DEFECT

        s1, s2 = PAYOFFS[(m1, m2)]
        p1_score += s1
        p2_score += s2

        move_history.append((m1, m2))
        score_history.append((p1_score, p2_score))

        # update strategies with last round info (common pattern)
        if hasattr(player1, "update"):
            player1.update(m1, m2)
        if hasattr(player2, "update"):
            player2.update(m2, m1)

    return {
        "final_scores": (p1_score, p2_score),
        "score_history": score_history,
        "move_history": move_history,
    }
