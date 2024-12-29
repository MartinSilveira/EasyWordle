from sources.others.config import *

with open(WORDLE_DATABASE, "r") as wordle_file:
    wordle_dict = [line[:5] for line in wordle_file]

letter_freqs = [0] * ALPHABET_SIZE
position_freqs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]
total = 0

for word in wordle_dict:
    position = 0
    for letter in word:
        letter_freqs[ord(letter) - 97] += 1  #97 porque o char 'a' tem a posição 97 na tabela ascii
        position_freqs[ord(letter) - 97][position] += 1
        total += 1
        position += 1

with open(PROBS_PATH, "w") as probs_file:
    probs_file.write("Letter Probabilities:\n")
    for i in range(len(letter_freqs)):
        probs_file.write(f"{chr(i + 97)}: {(letter_freqs[i]/total):.6f}\n")

    probs_file.write("\nPosition Probabilities:")
    for i in range(ALPHABET_SIZE):
        probs_file.write(f"\n{chr(i + 97)}:\n")
        for j in range(N_LETTERS):
            probs_file.write(f"{(position_freqs[i][j]/(total/5)):.6f} ")
        probs_file.write("\n")