import subprocess
from sources.others.config import *
from sources.others.functions import *

letter_freqs = [0] * ALPHABET_SIZE
attempt_freq = [0] * N_ATTEMPTS
position_freqs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]
total = 0
avg_attempts = 0
wordles_solved = 0


for iter in range(1, N_ITERATIONS + 1):
    #deleteLines(1)
    print(f"Iteration {iter}")

    #seria possivel passar estes opens para fora deste loop, para só ter de abrir os processos 1 vez?
    #depois dentro de cada processo é que se faz os loops?
    wordle_process = subprocess.Popen(["python3", WORDLE_MAIN_PATH])
    solver_process = subprocess.Popen(["python3", SOLVER_MAIN_PATH])
    
    #resets the wordle_pipe, deleting the content inside
    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        pass
    
    wordle_process.wait()
    solver_process.wait()

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


#update probabilities
with open(NEW_PROBS_PATH, "w") as probs:
    probs.write("Letter Probabilities:\n")
    for i in range(len(letter_freqs)):
        probs.write(f"{chr(i + 97)}: {(letter_freqs[i]/total):.6f}\n")

    probs.write("\nPosition Probabilities:")
    for i in range(ALPHABET_SIZE):
        probs.write(f"\n{chr(i + 97)}:\n")
        for j in range(N_LETTERS):
            probs.write(f"{(position_freqs[i][j]/(total/5)):.6f} ")
        probs.write("\n")

with open(PROB_UPDATER_PATH, "r") as prob_updater:
    exec(prob_updater.read())

#update stats
with open(NEW_STATS_PATH, "w") as stats:
    stats.write(f"Number of Iterations:\n{N_ITERATIONS}\n")
    stats.write(f"\nAverage Attempts:\n{avg_attempts:.4f}\n")

    wordles_unsolved = N_ITERATIONS - wordles_solved
    wordle_solve_ratio = (wordles_solved/N_ITERATIONS) * 100
    stats.write(f"\nWordles Solved/Unsolved: ({wordle_solve_ratio:.2f}%)\n{wordles_solved}\n{wordles_unsolved}\n")

    stats.write("\nAttempts Frequency:\n")
    for a in range(N_ATTEMPTS):
        stats.write(f"{a + 1}: {attempt_freq[a]} ({((attempt_freq[a]/wordles_solved) * 100):.2f}%)\n")


with open(STATS_UPDATER_PATH, "r") as stats_updater:
    exec(stats_updater.read())

    












        

    

