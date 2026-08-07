# Griductive Solver

A logic deduction game where players must identify **Criminals** and **Innocents**
based on revealed clues, using propositional logic and SAT solving.

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## 🎮 How to Play

1. **Select** a grid size (3×3, 4×4, or 5×5) and level from the main menu
2. **Click** on a face-down card to submit a verdict (Criminal or Innocent)
3. If your verdict is **logically provable**, the card flips and reveals a new clue
4. If not, you'll see a **NOT_PROVABLE** or **CONTRADICTED** message
5. Click on a **revealed clue** to highlight related cells on the board
6. Use **Hint** to get a suggestion, or **Auto Solve** to watch the AI solve it

## 📁 Project Structure

```
Griductive_Solver_2/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── game/
│   ├── card.py            # Card model
│   ├── board.py           # Board/Grid model
│   └── game_engine.py     # Game Engine (owns hidden state)
├── gui/
│   ├── constants.py       # Colors, fonts, sizes
│   ├── widgets.py         # Reusable UI components
│   ├── menu.py            # Main Menu screen
│   ├── game_scene.py      # Game Board screen
│   └── result_scene.py    # Result/Win screen
├── logic/
│   ├── clue.py            # Clue types & semantic evaluators
│   ├── cnf.py             # CNF data structures
│   ├── encoder.py         # Clue → CNF encoder
│   ├── dpll.py            # DPLL SAT Solver
│   └── logic_agent.py     # Deductive Logic Agent
└── puzzles/
    ├── 3x3_lv1.json       # Small Village
    ├── 3x3_lv2.json       # Harbor Town
    ├── 4x4_lv1.json       # City Square
    ├── 4x4_lv2.json       # Night Market
    ├── 5x5_lv1.json       # Grand Academy
    └── 5x5_lv2.json       # Royal Court
```

## 👥 Team

- **Người 1**: Game Engine, GUI, Puzzle Data
- **Người 2**: Logic, CNF Encoding, DPLL Solver, Logic Agent
