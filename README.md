# Evolutionary Game Theory Simulator (Iterated Prisoner’s Dilemma)

A Streamlit app that simulates the Iterated Prisoner’s Dilemma (IPD) using classic strategies, round-robin tournaments, and an evolutionary mode to visualize how strategy populations change over time.

## Features
- **Single Match:** Run one strategy vs another and view score progression + move history
- **Tournament Mode:** Round-robin tournament across all strategies with a leaderboard + plot
- **Evolution Mode:** Simulate strategy selection over generations (elite selection + mutation)
- **Noise Support:** Optional “move flip” probability to model mistakes/real-world randomness
- **Modular Strategies:** Strategies live in `strategies/` and can be added easily

## Tech Stack
- Python
- Streamlit
- Pandas
- Matplotlib (via your visualization helpers)

## Project Structure
```text
.
├── app.py               # Streamlit UI (tabs: match / tournament / evolution)
├── tournament.py        # Round-robin tournament logic
├── evolution.py         # Evolutionary simulation (selection + mutation)
├── visualization.py     # Plot helpers
├── strategies/          # Strategy implementations
│   ├── base_strategy.py
│   ├── tit_for_tat.py
│   ├── always_cooperate.py
│   ├── always_defect.py
│   └── random_strategy.py
└── README.md
```
## Setup
```bash
git clone https://github.com/sherpan26/Evolutionary_Game_Theory_Simulator.git
cd Evolutionary_Game_Theory_Simulator

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
If you don’t have a requirements.txt yet, create one with:

pip install streamlit pandas matplotlib
pip freeze > requirements.txt
```
## Run
```bash
streamlit run app.py
Then open the local URL Streamlit prints (usually http://localhost:8501).

Adding a New Strategy
Create a file in strategies/ (example: grudger.py)

Implement the same interface as the other strategies (see base_strategy.py)

Add it to STRATEGY_MAP in app.py
Notes
Noise level represents the probability a move is randomly flipped (cooperate ↔ defect).

Evolution mode uses elite selection (top performers survive) plus mutation to explore new mixes.

Future Improvements
Add more strategies (Grudger, Pavlov/Win-Stay-Lose-Shift, Generous Tit-for-Tat)

Export tournament results to CSV

Add tests + CI
```
