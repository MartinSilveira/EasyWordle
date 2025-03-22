from src.config.config import *
from src.utils.functions.functions import *
#this program takes the probs.txt and prob2.txt and combines it into probs.txt

letter_probs = [0] * ALPHABET_SIZE
position_probs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]
new_letter_probs = [0] * ALPHABET_SIZE
new_position_probs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]

#turn this duplicated code into a function
with open(PROBS_PATH, "r") as probs_file:
    ignore = probs_file.readline()
    for line in range(1, ALPHABET_SIZE + 1): #reads the letter probabilities
        letter_probs[line - 1] = float((probs_file.readline().strip())[3:])

    ignore = probs_file.readline()

    for letter in range(0, ALPHABET_SIZE):
        for i in range(0, 2):
            ignore = probs_file.readline()
        
        line = probs_file.readline().strip() #reads the position probabilities for each letter
        step = 0
        for position in range(0, N_LETTERS):
            position_probs[letter][position] = float(line[(0 + step):(8 + step)])
            step += 9

with open(NEW_PROBS_PATH, "r") as probs_file:
    ignore = probs_file.readline()
    for line in range(1, ALPHABET_SIZE + 1): #reads the letter probabilities
        new_letter_probs[line - 1] = float((probs_file.readline().strip())[3:])

    ignore = probs_file.readline()

    for letter in range(0, ALPHABET_SIZE):
        for i in range(0, 2):
            ignore = probs_file.readline().strip()
        
        line = probs_file.readline().strip() #reads the position probabilities for each letter
        step = 0
        for position in range(0, N_LETTERS):
            new_position_probs[letter][position] = float(line[(0 + step):(8 + step)])
            step += 9

with open(STATS_PATH, "r") as stats_file:
    ignore = stats_file.readline()
    total_iterations = int(stats_file.readline().strip())

#sum lists of both files into the lists of the first file
for i in range(0, ALPHABET_SIZE):
    letter_probs[i] = ((letter_probs[i] * total_iterations) + (new_letter_probs[i] * N_ITERATIONS)) / (total_iterations + N_ITERATIONS) 

    for j in range(0, N_LETTERS):
        position_probs[i][j] = ((position_probs[i][j] * total_iterations) + (new_position_probs[i][j] * N_ITERATIONS)) / (total_iterations + N_ITERATIONS)

#writes the results to the probs.txt file
#write_to_probs(PROBS_PATH, letter_probs, position_probs, total_iterations + N_ITERATIONS)
with open(PROBS_PATH, "w") as probs:
    probs.write("Letter Probabilities:\n")
    for i in range(len(letter_probs)):
        probs.write(f"{chr(i + 97)}: {letter_probs[i]:.6f}\n")

    probs.write("\nPosition Probabilities:")
    for i in range(ALPHABET_SIZE):
        probs.write(f"\n{chr(i + 97)}:\n")
        for j in range(N_LETTERS):
            probs.write(f"{position_probs[i][j]:.6f} ")
        probs.write("\n")

    


