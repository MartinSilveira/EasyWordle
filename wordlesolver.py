import subprocess
from src.config.config import *
from src.utils.functions.functions import *

letter_freqs = [0] * ALPHABET_SIZE
attempt_freq = [0] * N_ATTEMPTS
position_freqs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]
total = 0
avg_attempts = 0
wordles_solved = 0

if EXECUTE_LETTER_PROBS_FINDER:
    with open(LETTER_PROBS_FINDER_PATH, "r") as letter_probs_finder:
        exec(letter_probs_finder.read())
    exit()

if EXECUTE_PROB_FINDER:
    with open(PROB_FINDER_PATH, "r") as prob_finder:
        exec(prob_finder.read())
    exit()

if TEST_MODE_ENABLED:
    N_ITERATIONS = MAX

print("")
for iter in range(1, N_ITERATIONS + 1):
    if not PRINTS_ENABLED:
        deleteLines(1)
    print(f"Iteration {iter}")

    #resets the wordle_pipe, deleting the content inside
    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        pass

    wordle_process = subprocess.Popen(["python3", WORDLE_MAIN_PATH])
    solver_process = subprocess.Popen(["python3", SOLVER_MAIN_PATH])
  
    wordle_process.wait()
    solver_process.wait()

    if PROBS_UPDATES_ENABLED or STATS_UPDATES_ENABLED:
        with open(RESULTS_PATH, "r") as results:
            word = results.readline().strip()
            attempts = int(results.readline().strip())

        if attempts != 0:
            avg_attempts = ((avg_attempts * (iter - 1)) + attempts) / iter
            wordles_solved += 1
            attempt_freq[attempts - 1] += 1

        position = 0
        for letter in word:
            letter_freqs[ord(letter) - 97] += 1  #97 porque o char 'a' tem a posição 97 na tabela ascii
            position_freqs[ord(letter) - 97][position] += 1
            total += 1
            position += 1

if PROBS_UPDATES_ENABLED:
    write_to_probs(NEW_PROBS_PATH, letter_freqs, position_freqs, total)

    with open(PROB_UPDATER_PATH, "r") as prob_updater:
        exec(prob_updater.read())

if STATS_UPDATES_ENABLED:
    write_to_stats(NEW_STATS_PATH, N_ITERATIONS, avg_attempts, wordles_solved, attempt_freq)
    
    with open(STATS_UPDATER_PATH, "r") as stats_updater:
        exec(stats_updater.read())
    
if TEST_MODE_ENABLED:
    with open(ITERS_PATH, "w") as iters:
        iters.write(f"{1}")












        

    

