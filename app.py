import streamlit as st
import pandas as pd
import re

# --- Import Core Logic ---
from game_engine import play_game
from tournament import run_tournament
from evolution import run_evolution
from visualization import plot_score_progression, plot_tournament_results

# --- Import Strategies ---
from strategies.tit_for_tat import TitForTat
from strategies.always_cooperate import AlwaysCooperate
from strategies.always_defect import AlwaysDefect
from strategies.random_strategy import Random
from strategies.base_strategy import COOPERATE

# --- App Configuration ---
st.set_page_config(
    page_title="IPD Simulator",
    page_icon="🎭",
    layout="wide"
)

# --- Strategy Mapping ---
# This dictionary is crucial for the app to find the strategy classes.
STRATEGY_MAP = {
    "Tit for Tat": TitForTat,
    "Always Cooperate": AlwaysCooperate,
    "Always Defect": AlwaysDefect,
    "Random": Random,
}

# --- Sidebar for Global Settings ---
with st.sidebar:
    st.title("⚙️ Global Settings")
    st.info("These settings apply to all simulation modes.")
    num_rounds = st.slider("Number of Rounds", min_value=10, max_value=200, value=100, step=10)
    noise_level = st.slider("Noise Level", min_value=0.0, max_value=0.5, value=0.05, step=0.01,
                              help="The probability a player's move will be randomly flipped.")

# --- Main App Layout ---
st.title("🎭 Iterated Prisoner's Dilemma Simulator")

tab1, tab2, tab3 = st.tabs(["Single Match", "🏆 Tournament", "🧬 Evolution"])

# --- Tab 1: Single Match Simulation ---
with tab1:
    st.header("One Strategy vs. Another")

    col1, col2 = st.columns(2)
    with col1:
        p1_name = st.selectbox("Choose Player 1", options=list(STRATEGY_MAP.keys()), key="p1_select")
    with col2:
        p2_name = st.selectbox("Choose Player 2", options=list(STRATEGY_MAP.keys()), index=2, key="p2_select")

    if st.button("Run Simulation", key="run_single"):
        player1, player2 = STRATEGY_MAP[p1_name](), STRATEGY_MAP[p2_name]()
        results = play_game(player1, player2, rounds=num_rounds, noise=noise_level)
        final_score1, final_score2 = results["final_scores"]

        st.subheader("📊 Results")
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric(label=f"**Player 1 ({p1_name}) Final Score**", value=final_score1)
        metric_col2.metric(label=f"**Player 2 ({p2_name}) Final Score**", value=final_score2)

        st.subheader("Score Progression")
        score_fig = plot_score_progression(results["score_history"], p1_name, p2_name)
        st.pyplot(score_fig)

        st.subheader("Round-by-Round History")
        move_df = pd.DataFrame(results["move_history"], columns=["P1 Move", "P2 Move"])
        move_df.index.name = "Round"
        move_df.index += 1
        st.dataframe(move_df.style.applymap(
            lambda val: 'background-color: #AEC6CF' if val == COOPERATE else 'background-color: #FFB347'
        ), use_container_width=True)

# --- Tab 2: Tournament Mode ---
with tab2:
    st.header("Round-Robin Tournament")
    st.markdown("All strategies play against each other and themselves. Scores are cumulative.")

    if st.button("Run Tournament", key="run_tournament"):
        with st.spinner("Running tournament... This may take a moment."):
            leaderboard = run_tournament(STRATEGY_MAP, rounds=num_rounds, noise=noise_level)
            leaderboard_df = pd.DataFrame(leaderboard, columns=["Strategy", "Total Score"])
            leaderboard_df.index += 1
            leaderboard_df.index.name = "Rank"

        st.subheader("🏆 Final Leaderboard")
        st.dataframe(leaderboard_df, use_container_width=True)

        st.subheader("Score Visualization")
        leaderboard_fig = plot_tournament_results(leaderboard)
        st.pyplot(leaderboard_fig)

# --- Tab 3: Evolutionary Simulation ---
with tab3:
    st.header("Evolutionary Simulation")
    st.markdown("Observe how a population of strategies evolves over generations based on performance.")

    evo_col1, evo_col2 = st.columns(2)
    with evo_col1:
        population_size = st.slider("Population Size", 50, 500, 100, 10)
        num_generations = st.slider("Number of Generations", 10, 200, 50, 5)
    with evo_col2:
        elite_percentage = st.slider("Elite Selection (%)", 1, 50, 10, 1, help="Percentage of top performers that pass to the next generation.")
        mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.05, 0.01)

    if st.button("Run Evolutionary Simulation", key="run_evolution"):
        num_elites = int(population_size * (elite_percentage / 100.0))

        with st.spinner(f"Running evolution for {num_generations} generations... This will take time."):
            history = run_evolution(
                strategy_map=STRATEGY_MAP,
                generations=num_generations,
                population_size=population_size,
                elite_size=num_elites,
                mutation_rate=mutation_rate,
                rounds=num_rounds,
                noise=noise_level
            )

            history_df = pd.DataFrame(history).fillna(0)
            # Make column names more readable (e.g., "TitForTat" -> "Tit For Tat")
            history_df.columns = [re.sub(r'(?<!^)(?=[A-Z])', ' ', c) for c in history_df.columns]

        st.subheader("📈 Population Dynamics Over Time")
        st.line_chart(history_df)

        st.subheader("Final Population Composition")
        final_composition = history_df.iloc[-1].sort_values(ascending=False)
        st.dataframe(final_composition)