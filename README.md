# Wordle Solver

A Python script that automatically solves Wordle puzzles using an entropy-based algorithm to maximize information gain with each guess.

## Features
- Suggests optimal guesses based on remaining possibilities.
- Calculates entropy and expected uncertainty reduction for each guess.
- Can solve a single game or run batch simulations to measure performance.
- Provides detailed output for each guess including feedback, entropy, and remaining possibilities.

## Requirements
- Python 3.7 or higher.
- A `words.py` file containing a list of valid 5-letter words. Make sure this file is in the same folder as `wordle_solver.py`.

## Installation
1. Clone the repository or download the files directly:

```bash
git clone https://github.com/yourusername/wordle-solver.git
cd wordle-solver

## Running the Script
```python
# with random target word
python3 wordle_solver.py
# with a given target word
python3 wordle_solver.py -t crane
# as a batch of 100 words
python3 wordle_solver.py -c 100
