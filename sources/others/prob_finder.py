from sources.others.config import *

#this program finds the probabilities for each word based on the probs.txt file

letter_probs = [0] * ALPHABET_SIZE
position_probs = [[0 for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]
scores = {}

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

    
with open(WORDS_PATH, "r") as words_file:
    for word in words_file.readlines():
        position = 0
        score = 0
        for letter in word.strip():
            score += position_probs[ord(letter) - 97][position]
            position += 1
        score = score * SCORE_WEIGHT + letter_probs[ord(letter) - 97] * LETTER_PROBS_WEIGHT
        scores[word.strip()] = score

scores_sorted = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

with open(WORD_DUPS_PATH, "w") as word_probs_file:
    for word, score in scores_sorted.items():
        word_probs_file.write(f"{word}: {score:.6f}\n")

for word in list(scores_sorted.keys()):
    if len(word) != len(set(word)): #verifica se o tamanho da palavra muda se forem retiradas as letras duplicadas (se não mudar, não há letras duplicadas)
        del scores_sorted[word]

with open(WORD_NODUPS_PATH, "w") as word_probs_file:
    for word, score in scores_sorted.items():
        word_probs_file.write(f"{word}: {score:.6f}\n")

