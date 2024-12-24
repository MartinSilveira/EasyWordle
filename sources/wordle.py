#import time
from termcolor import colored
import random
from others.config import *

if TEST_MODE_ENABLED:
    with open("iters.txt", "r") as iters:
        iter = int(iters.readline().strip())

    with open("iters.txt", "w") as iters:
        iters.write(f"{iter + 1}")

    #iter = ---
    index = random.randint(iter, iter)
    with open(WORDLE_DATABASE, "r") as words_file:
        for _ in range(1, index + 1):
            word = words_file.readline()

else:
    index = random.randint(1, MAX)
    with open(WORDLE_DATABASE, "r") as words_file:
        for _ in range(1, index + 1):
            word = words_file.readline()

if CUSTOM_WORD == "":
    correct_word = word.strip()
else:
    correct_word = CUSTOM_WORD

if PRINTS_ENABLED:
    print(f"Correct Word: {correct_word}")

with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
    wordle_pipe.write("waiting for solver")

output = ""
solved = False
for attempt in range(1, N_ATTEMPTS + 1):
    with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
        while True:
            wordle_in = wordle_pipe.readline().strip()
            wordle_pipe.seek(0)
            if wordle_in in ["waiting for solver", "", output]:  #espera pela palavra guessed do solver
                #time.sleep(PC_SLEEPTIME1)
                continue
            elif wordle_in == "EXIT":
                exit()
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

    if correct_letters == N_LETTERS:
        with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
            wordle_pipe.write("Wordle Solved!\n")    

        if PRINTS_ENABLED:
            print(colored(wordle_in, "white", "on_green"))      #removing both of these prints saves around 1 second over 500 iterations
            print(f"Wordle Solved!\nAttempts Taken: {attempt}")
        
        solved = True
        break

    output = "".join([f"{wordle_in[i]}{colours[i]}" for i in range(N_LETTERS)])
    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        wordle_pipe.write(output + "\n")

with open(RESULTS_PATH, "w") as results:
    if solved == False:
        attempt = 0
        with open("words_to_fix.txt", "a") as words_to_fix:
            words_to_fix.write(f"{correct_word}\n")
    results.write(f"{correct_word}\n{attempt}\n")



