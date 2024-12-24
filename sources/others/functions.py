from sources.others.config import *

def read_results(attempt_freq, letter_freqs, position_freqs, wordles_solved, total, avg_attempts, iter):
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


def write_to_probs(path, letter_freqs, position_freqs, total):
    with open(path, "w") as probs:
        probs.write("Letter Probabilities:\n")
        for i in range(len(letter_freqs)):
            probs.write(f"{chr(i + 97)}: {(letter_freqs[i]/total):.6f}\n")

        probs.write("\nPosition Probabilities:")
        for i in range(ALPHABET_SIZE):
            probs.write(f"\n{chr(i + 97)}:\n")
            for j in range(N_LETTERS):
                probs.write(f"{(position_freqs[i][j]/(total/5)):.6f} ")
            probs.write("\n")


def write_to_stats(path, iterations, avg_attempts, wordles_solved, attempt_freq):
    with open(path, "w") as stats:
        stats.write(f"Number of Iterations:\n{iterations}\n")
        stats.write(f"\nAverage Attempts:\n{avg_attempts:.4f}\n")

        wordles_unsolved = iterations - wordles_solved
        wordle_solve_ratio = (wordles_solved/iterations) * 100
        stats.write(f"\nWordles Solved/Unsolved: ({wordle_solve_ratio:.2f}%)\n{wordles_solved}\n{wordles_unsolved}\n")

        stats.write("\nAttempts Frequency:\n")
        for a in range(N_ATTEMPTS):
            stats.write(f"{a + 1}: {attempt_freq[a]} ({((attempt_freq[a]/wordles_solved) * 100):.2f}%)\n")

    
def deleteLines(number_of_lines):
    for _ in range(number_of_lines):
        print("\033[F\033[2K", end="\r")


def marked_as(letter, wordle_out, colours):
    count = 0
    for i in range(0, N_LETTERS * 2, 2):
        if letter == None:
            if wordle_out[i + 1] in colours:
                count += 1
        elif letter == wordle_out[i]:  #encontra a posição da letra no wordle_out
            if wordle_out[i + 1] in colours:  #verifica se a letra está marcada como verde ou amarela
                count += 1
    
    return count

#verifies if there's duplicate letters in wordle_out
def n_dups_in_word(letter, wordle_out, position):
    count = 0
    for i in range(0, N_LETTERS * 2, 2):
        if wordle_out[i] == letter and wordle_out[i + 1] in [GREEN, YELLOW]:
            count += 1
    return count

def n_instances(letter, word):
    count = 0
    for l in word:
        if l == letter:
            count += 1      
    return count


