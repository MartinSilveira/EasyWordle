from src.config.config import *
from src.utils.functions.functions import *

#places every word in the wordle dictionary in a list
with open(WORD_DUPS_PATH, "r") as all_words_file:
    all_words = [line[:5] for line in all_words_file]

#reads the first word to guess
with open(WORD_NODUPS_PATH, "r") as word_file:
    word = (word_file.readline())[:5]

used_letters = set(word)
words_non_used_letters = all_words

for attempt in range(1, N_ATTEMPTS + 1):
    with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
        while True:
            status = wordle_pipe.readline().strip()
            wordle_pipe.seek(0)
            if status == "Wordle Solved!":
                exit()
            elif (attempt == 1 and status != "waiting for solver") or (attempt > 1 and len(status) != WORDLE_OUT_LEN):
                continue
            else:
                break

    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        wordle_pipe.write(word)
    words_non_used_letters.remove(word)

    if PRINTS_ENABLED:
        print(f"Guessed Word: {word} in Attempt {attempt}")

    
    #wordle_out é do formato a0b1c2d0e1 (os números variam entre {0, 2} e indicam a cor da letra antes)
    with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
        while True:
            wordle_out = wordle_pipe.readline().strip()
            wordle_pipe.seek(0)
            if wordle_out in [word, ""]:
                continue
            elif wordle_out == "Wordle Solved!" or attempt == N_ATTEMPTS:
                exit()
            else:
                break

    #e se, ao invés de devolver todas as palavras possíveis, encontra e devolve logo a primeira palavra e não tem de procurar o resto da lista
    #pra fazer isto é preciso ter algumas listas que guardam as posições certas e as letras e etc
    if DEBUG_ENABLED:
        print(wordle_out)

    word_to_try = None
    first_word = None

    extra_letters = set()
    for word in all_words:
        for letter in word:
            if letter not in used_letters:
                extra_letters.add(letter)

    if DEBUG_ENABLED:
        print("Extra Letters: ", extra_letters)

    if (N_ATTEMPTS - attempt + 1) < len(all_words) and attempt < N_ATTEMPTS - 1:
        for word in words_non_used_letters:
            if not (set(word) & used_letters) and len(set(word)) == N_LETTERS: #se não houver nenhuma letra já usada na palavra nem letras repetidas
                if first_word == None:
                    first_word = word
                
                if (set(word) & extra_letters): #se na palavra só existirem apenas as letras que estão nas palavras possíveis
                    word_to_try = word
                    break

        if word_to_try == None:
            for word in all_words:
                if len(set(word) & extra_letters) >= 3:
                    word_to_try = word
                    break

        if word_to_try == None:
            word_to_try = first_word
        
    filtered_words = []
    for word in all_words:
        remove = False
        for i in range(N_LETTERS): 
            letter = wordle_out[2*i]
            colour = wordle_out[2*i + 1]
            if (colour is GREY):
                if letter in word:
                    if marked_as(letter, wordle_out, [GREEN, YELLOW]) == 0: #se a letra é grey e a letra está na palavra e não está marcada a verde noutro lado, remove a palavra
                        remove = True                                                                                      #ou se é amarela e a letra não está na palavra
                        break
                    elif marked_as(letter, wordle_out, [GREEN, YELLOW]) > 0:
                        positions = []
                        for j in range(0, N_LETTERS * 2, 2): #encontra as posições das letras cinzentas no wordle_out
                            if wordle_out[j] == letter and wordle_out[j + 1] == GREY:
                                positions.append(j // 2)
                        for pos in positions:  #remover as palavras que têm uma letra cinzenta em positions
                            if word[pos] == letter:
                                remove = True                                                                                     
                                break
                    
            elif (colour is YELLOW):
                if (letter == word[i] or letter not in word) or n_dups_in_word(letter, wordle_out, i) > n_instances(letter, word):
                    remove = True                                                     
                    break 

            elif (colour is GREEN):
                if letter != word[i]: #se a letra é verde e não está naquela posição da palavra, remove a palavra
                    remove = True
                    break

        if remove == False:
            filtered_words.append(word)
        
    all_words = filtered_words
    if DEBUG_ENABLED:
        print(all_words)
                               #if there's more attempts left than possible words
    if word_to_try == None or (N_ATTEMPTS - attempt) > len(all_words):
        word = all_words[0]
    else:
        word = word_to_try

    #exclui as letras usadas
    for i in range(N_LETTERS):    
        letter = word[i]
        used_letters.add(letter)

    if DEBUG_ENABLED:
        print("Used Letters: ", used_letters)











