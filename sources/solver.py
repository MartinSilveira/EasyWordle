from others.config import *
from others.functions import *

with open(WORD_DUPS_PATH, "r") as all_words_file:
    all_words = [line[:5] for line in all_words_file]

with open(WORD_NODUPS_PATH, "r") as word_file:
    word = (word_file.readline())[:5]

used_letters = set()
words_non_used_letters = all_words

for attempt in range(1, N_ATTEMPTS + 1):
    with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
        while True:
            status = wordle_pipe.readline().strip()
            wordle_pipe.seek(0)
            if status == "Wordle Solved!":
                exit()
            elif (attempt == 1 and status != "waiting for solver") or (attempt > 1 and len(status) != 10):
                continue
            else:
                break

    with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
        wordle_pipe.write(word)
    if PRINTS_ENABLED:
        print(f"Guessed Word: {word}  Attempt {attempt}")
    
    #wordle_out é do formato a0b1c2d0e1 (os números variam entre {0, 2} e indicam a cor da letra antes)
    with open(WORDLE_PIPE_PATH, "r") as wordle_pipe:
        while True:
            wordle_out = wordle_pipe.readline().strip()
            wordle_pipe.seek(0)
            if wordle_out in [word, ""]:
                #time.sleep(PC_SLEEPTIME2)
                continue
            elif wordle_out == "Wordle Solved!" or attempt == N_ATTEMPTS:
                exit()
            else:
                break


    #ideia
    #tracker de quais letras já foram usadas
    #se o número de letras já encontradas (amarelas ou verdes) for igual ou maior que 3 
    #e o número de tentativas restantes (N_ATTEMPTS - attempt) for menor que número de palavras na all_word e não seja a última tentativa
    #vai buscar e dá guess da palavra mais provável que não contém nenhuma letra usada
    #se não houver nenhuma palavra nesses critérios, adivinha normalmente (por enquanto)
    #volta a tentar adivinhar a palavra certa se o número de tentativas restantes (N_ATTEMPTS - attempt) for maior ou igual ao número de palavras na all_words
                

    #e se, ao invés de devolver todas as palavras possíveis, encontra e devolve logo a primeira palavra e não tem de procurar o resto da lista
    if DEBUG_ENABLED:
        print(wordle_out)

    for i in range(N_LETTERS):    #exclui as letras usadas na última tentativa
        letter = wordle_out[2*i]
        used_letters.add(letter)

    word_to_try = None


    #se já acertou 3 ou mais letras e tem mais palavras possíveis que tentativas restantes e não está na última tentativa
    if USE_NON_USED_LETTERS_ALG:
        extra_letters = set()
        if attempt > 1:
            for word in all_words:
                for l in word:
                    if l not in used_letters:
                        extra_letters.add(l)

        if (N_ATTEMPTS - attempt + 1) < len(all_words) and attempt < N_ATTEMPTS - 1:
            for word in words_non_used_letters:
                if not (set(word) & used_letters) and len(set(word)) == N_LETTERS: #se não houver nenhuma letra já usada na palavra nem letras repetidas
                    #print(extra_letters)
                    if (set(word) & extra_letters):
                        word_to_try = word
                        break
                    else:
                    #print this out for the next stage
                        word_to_try = word
                        break
            """if word_to_try == None:
                for word in words_non_used_letters:  
                    if len(set(word) & used_letters) < 3 and len(set(word)) == N_LETTERS:
                        #basically this uses words that have mostly (3) non-used letters + 2 used letters
                        word_to_try = word
                        break"""
    
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
    
    if word_to_try == None:
        try:
            word = all_words[0]
        except Exception as e:
            print("Error:", e)
            with open(WORDLE_PIPE_PATH, "w") as wordle_pipe:
                wordle_pipe.write("EXIT")
            exit()

    else:
        word = word_to_try
        if DEBUG_ENABLED:
            print(word_to_try)











