import time
from termcolor import colored
import random
from others.config import *

index = random.randint(1, MAX)
with open(WORDLE_DATABASE, "r") as words_file:
    for _ in range(1, index + 1):
        word = words_file.readline()

correct_word = word.strip()
print(f"Correct Word: {correct_word}")

with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
    wordle_pipe.write("waiting for solver")

output = ""
solved = False
for attempt in range(1, N_ATTEMPTS + 1):
    while True:
        with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
            wordle_in = wordle_pipe.readline().strip()
        if wordle_in == "waiting for solver" or wordle_in == output or wordle_in == "":  #espera pela palavra guessed do solver
            time.sleep(0.00035)
        else:
            break

    colours = []
    correct_letters = 0
    correct_word_tracker = list(correct_word)  # For tracking unused letters in the correct word
    user_word_marked = [False] * N_LETTERS    # For tracking matched letters in the user's guess

    for i in range(N_LETTERS):
        if wordle_in[i] == correct_word[i]:
            colours.append(GREEN)
            correct_word_tracker[i] = None  # Mark this letter as used
            user_word_marked[i] = True      # Mark this letter as matched (green)
            correct_letters += 1
        else:
            colours.append(None)  # Placeholder for now

    for i in range(N_LETTERS):
        if colours[i] is None:  # Only process if not already marked as green
            if wordle_in[i] in correct_word_tracker:
                colours[i] = YELLOW
                # Mark the first occurrence of this letter as used
                correct_word_tracker[correct_word_tracker.index(wordle_in[i])] = None
            else:
                colours[i] = GREY

    output = "".join([f"{wordle_in[i]}{colours[i]}" for i in range(N_LETTERS)])
    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        wordle_pipe.write(output + "\n")

    if correct_letters == N_LETTERS:
        with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
            wordle_pipe.write("Wordle Solved!\n")    
        print(colored(wordle_in, "white", "on_green"))      #removing both of these prints saves around 1 second over 500 iterations
        print(f"Wordle Solved!\nAttempts Taken: {attempt}")
        solved = True
        break

with open(RESULTS_PATH, "w") as results:
    if solved == False:
        attempt = 0
    results.write(f"{correct_word}\n{attempt}\n")



