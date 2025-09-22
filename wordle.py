import math
import random
import sys
from words import words
from collections import Counter

# G - appears at correct index
# Y - appears at wrong index
# X - does not appear at all
def get_feedback(guess, target):
    feedback = ["X"] * 5
    filled = [False] * 5
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = "G"
            filled[i] = True
    for i in range(5):
        if feedback[i] == "X":
            for j in range(5):
                if not filled[j] and guess[i] == target[j]:
                    feedback[i] = "Y"
                    filled[j] = True
                    break
    return "".join(feedback)

def get_entropy(guess, possible):
    num_possible = len(possible)
    if num_possible == 0:
        return 0.0
    feedbacks = Counter(get_feedback(guess, word) for word in possible)
    entropy = 0.0
    for count in feedbacks.values():
        p = count / num_possible
        entropy -= p * math.log2(p)
    return entropy

def get_guess(possible):
    best_guess = ""
    guess_entropy = -1
    for guess in possible:
        entropy = get_entropy(guess, possible)
        if entropy > guess_entropy:
            best_guess = guess
            guess_entropy = entropy
    if len(possible) > 1:
        max_entropy = math.log2(len(possible))
        percentage_reduced = (guess_entropy / max_entropy * 100)
    else:
        percentage_reduced = 0
    return best_guess, guess_entropy, percentage_reduced

def run_wordle(target=None, verbose=True):
    solved = False
    target_word = target if target else random.choice(words)
    guess_pool = words[:]
    round_num = 0

    if verbose:
        print(f"The target word is: {target_word}")

    while round_num < 6 and len(guess_pool) > 0:
        round_num += 1
        if round_num == 1:
            best_guess = "crane"
            guess_entropy = get_entropy(best_guess, guess_pool)
            if len(guess_pool) > 1:
                max_entropy = math.log2(len(guess_pool))
                percentage_reduced = (guess_entropy / max_entropy * 100)
            else:
                percentage_reduced = 0
            result = (best_guess, guess_entropy, percentage_reduced)
        else:
            result = get_guess(guess_pool)

        feedback = get_feedback(result[0], target_word)
        pool_before = len(guess_pool)
        guess_pool = [word for word in guess_pool if get_feedback(result[0], word) == feedback]
        pool_after = len(guess_pool)

        if verbose:
            if pool_before > 1 and pool_after > 0:
                actual_percent_reduced = (math.log2(pool_before) - math.log2(pool_after)) / math.log2(pool_before) * 100
            else:
                actual_percent_reduced = 0
            print(f"Round {round_num} guess: {result[0]}")
            print(f"Feedback: {feedback}")
            print(f"Entropy: {result[1]:.3f} bits")
            print(f"Expected info gain: {result[2]:.1f}%")
            print(f"Actual uncertainty reduction: {actual_percent_reduced:.1f}%")
            print(f"Remaining word count: {pool_after}\n")

        if result[0] == target_word:
            solved = True
            break

    if verbose:
        if solved:
            print(f"Solved! The target word was {target_word}. This algorithm took {round_num} guesses total. :)")
        else:
            print(f"The algorithm failed to guess the target word {target_word}. :(")

    return round_num if solved else None

def batch_runner(num_runs):
    total = 0
    solved = 0
    for _ in range(num_runs):
        guesses = run_wordle(verbose=False)
        if guesses is not None:
            total += guesses
            solved += 1
    return total, solved

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "-c":
        try:
            num_runs = int(sys.argv[2])
            total_guesses, total_solved = batch_runner(num_runs)
            total_unsolved = num_runs - total_solved
            average = total_guesses / total_solved if total_solved > 0 else 0

            print(f"Ran {num_runs} games.")
            print(f"Solved: {total_solved}, Unsolved: {total_unsolved}")
            print(f"Average guesses (solved only): {average:.3f}")

        except ValueError:
            print("Invalid number of runs. Usage: python3 file.py -c 100")

    elif len(sys.argv) >= 3 and sys.argv[1] == "-t":
        target_word = sys.argv[2].lower()
        if target_word not in words:
            print(f"Target word '{target_word}' is not in word list.")
        else:
            run_wordle(target=target_word, verbose=True)

    else:
        run_wordle(verbose=True)

