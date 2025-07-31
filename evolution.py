import random
import itertools
from collections import Counter
from game_engine import play_game

def run_population_tournament(population: list, rounds: int, noise: float):
    """
    Plays a round-robin tournament for a list of instantiated strategy objects.

    Args:
        population: A list of instantiated strategy objects.
        rounds: The number of rounds per game.
        noise: The noise level for each game.

    Returns:
        A list of tuples (strategy_instance, total_score), sorted by score.
    """
    scores = {id(p): 0 for p in population}
    
    # Play every individual against every other individual
    for player1, player2 in itertools.combinations(population, 2):
        results = play_game(player1, player2, rounds, noise)
        score1, score2 = results["final_scores"]
        scores[id(player1)] += score1
        scores[id(player2)] += score2
        
    # Create a list of (instance, score) and sort it
    fitness = [(p, scores[id(p)]) for p in population]
    fitness.sort(key=lambda x: x[1], reverse=True)
    
    return fitness


def run_evolution(strategy_map: dict, generations: int, population_size: int, elite_size: int, mutation_rate: float, rounds: int, noise: float):
    """
    Runs a full evolutionary simulation.
    """
    population = []
    # Create the initial, evenly distributed population
    strategy_names = list(strategy_map.keys())
    for i in range(population_size):
        strategy_name = strategy_names[i % len(strategy_names)]
        population.append(strategy_map[strategy_name]())

    population_history = []

    for _ in range(generations):
        # 1. Calculate fitness of the current population
        fitness_results = run_population_tournament(population, rounds, noise)
        
        # 2. Track the current population composition
        counts = Counter(p.__class__.__name__ for p, score in fitness_results)
        population_history.append(counts)
        
        # 3. Selection: Identify the elites
        elites = [p for p, score in fitness_results[:elite_size]]
        
        # 4. Reproduction and Mutation: Create the next generation
        next_population = elites.copy() # Elites are guaranteed to pass on
        
        while len(next_population) < population_size:
            if random.random() < mutation_rate:
                # A mutation occurs: create a random new strategy
                random_strategy_class = random.choice(list(strategy_map.values()))
                next_population.append(random_strategy_class())
            else:
                # No mutation: reproduce from the elites
                parent = random.choice(elites)
                next_population.append(parent.__class__())
        
        population = next_population

    return population_history