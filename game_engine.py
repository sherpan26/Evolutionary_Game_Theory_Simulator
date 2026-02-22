# game_engine.py
from strategies.base_strategy import COOPERATE, DEFECT

PAYOFFS = {
    (COOPERATE, COOPERATE): (3, 3),
    (COOPERATE, DEFECT):    (0, 5),
    (DEFECT, COOPERATE):    (5, 0),
    (DEFECT, DEFECT):       (1, 1),
}

def _get_move(player):
    # Try common method names across different strategy implementations
    for name in ("choose_action", "choose_move", "get_action", "select_action", "make_move", "play"):
        if hasattr(player, name):
            return getattr(player, name)()
    raise AttributeError(
        f"{player.__class__.__name__} has no move method. "
        "Expected one of: choose_action/choose_move/get_action/select_action/make_move/play"
    )

def play_game(player1, player2, rounds=100, noise=0.0):
    p1_score = p2_score = 0
    score_history, move_history = [], []

    for _ in range(rounds):
        m1 = _get_move(player1)
        m2 = _get_move(player2)

        if noise:
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

        # update hooks (optional)
        if hasattr(player1, "update"):
            player1.update(m1, m2)
        if hasattr(player2, "update"):
            player2.update(m2, m1)

    return {"final_scores": (p1_score, p2_score), "score_history": score_history, "move_history": move_history}
