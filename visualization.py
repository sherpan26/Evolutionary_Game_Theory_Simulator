import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set a visually appealing style for the plots
sns.set_theme(style="whitegrid")

def plot_score_progression(score_history: list, p1_name: str, p2_name: str):
    """
    Creates a line chart of score progression using Matplotlib.

    Args:
        score_history: A list of tuples, where each tuple is (p1_score, p2_score).
        p1_name: The name of player 1.
        p2_name: The name of player 2.

    Returns:
        A Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create a DataFrame for easier plotting
    df = pd.DataFrame(score_history, columns=[p1_name, p2_name])
    df.index.name = "Round"

    # Plot the data
    sns.lineplot(data=df, ax=ax, palette=["#1f77b4", "#ff7f0e"])
    
    ax.set_title("Score Progression Over Time", fontsize=16)
    ax.set_xlabel("Round")
    ax.set_ylabel("Total Score")
    ax.legend(title="Strategies")
    plt.tight_layout()
    
    return fig

def plot_tournament_results(leaderboard: list):
    """
    Creates a bar chart of tournament results using Seaborn.

    Args:
        leaderboard: A sorted list of tuples (strategy_name, total_score).

    Returns:
        A Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    df = pd.DataFrame(leaderboard, columns=["Strategy", "Total Score"])

    # Create the bar plot
    barplot = sns.barplot(
        data=df,
        x="Total Score",
        y="Strategy",
        ax=ax,
        palette="viridis",
        orient='h'
    )
    
    ax.set_title("Tournament Final Scores", fontsize=16)
    ax.set_xlabel("Total Score")
    ax.set_ylabel("Strategy")
    plt.tight_layout()
    
    return fig