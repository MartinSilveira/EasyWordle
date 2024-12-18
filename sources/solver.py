import time
from others.config import *

with open(WORD_DUPS_PATH, "r") as all_words_file:
    all_words = [line[:5] for line in all_words_file.readlines()]

with open(WORD_NODUPS_PATH, "r") as word_file:
    word = (word_file.readline())[:5]

for attempt in range(1, N_ATTEMPTS + 1):
    while True:
        with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
            status = wordle_pipe.readline().strip()
        if status == "Wordle Solved!":
            exit()
        elif (attempt == 1 and status != "waiting for solver") or (attempt > 1 and len(status) != 10):
            time.sleep(0.00035)
        else:
            break

    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        wordle_pipe.write(word)
    print(f"Guessed Word: {word}")
    
    #wordle_out é do formato a0b1c2d0e1 (os números variam entre {0, 2} e indicam a cor da letra antes)
    while True:
        with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
            wordle_out = wordle_pipe.readline().strip()
        if wordle_out == word or wordle_out == "":
            time.sleep(0.0015)
        elif wordle_out == "Wordle Solved!":
            exit()
        else:
            break

    filtered_words = []
    grey_letters = []
    yellow_letters = [None] * N_LETTERS
    green_letters = [None] * N_LETTERS

    position = 0
    green_counter = 0
    for i in range(0, N_LETTERS * 2, 2):
        letter = wordle_out[i]
        colour = wordle_out[i + 1]
        if colour == GREY:
            grey_letters.append(letter)
        elif colour == YELLOW:
            yellow_letters[position] = letter
        elif colour == GREEN:
            green_letters[position] = letter
        position += 1

    for word in all_words:
        remove = False
        used_positions = [False] * N_LETTERS
        
        for position in range(0, N_LETTERS):
            if green_letters[position] and green_letters[position] != word[position]:
                remove = True
                break
            if green_letters[position]:
                used_positions[position] = True

            if yellow_letters[position]:
                if yellow_letters[position] not in word or yellow_letters[position] == word[position]:
                    remove = True
                    break
            
                found_position = False
                for j in range(N_LETTERS):
                    if word[j] == yellow_letters[position] and j != position and not used_positions[j]:
                        used_positions[j] = True
                        found_position = True
                        break

                if found_position == False:
                    remove = True
                    break

        for grey_letter in grey_letters:
            for i in range(N_LETTERS):
                if word[i] == grey_letter and not (green_letters[i] == grey_letter 
                or any(yellow_letter == grey_letter for yellow_letter in yellow_letters if yellow_letter)):
                    remove = True
                    break
            if remove == True:
                break
        
        if remove == False:
            filtered_words.append(word)

    all_words = filtered_words
    word = all_words[0]
    





