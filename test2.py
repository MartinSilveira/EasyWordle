
from sources.others.config import *
from sources.others.functions import *

#places every word in the wordle dictionary in a list
with open(WORD_DUPS_PATH, "r") as all_words_file:
    all_words = [line[:5] for line in all_words_file]

#reads the first word to guess
with open(WORD_NODUPS_PATH, "r") as word_file:
    word = (word_file.readline())[:5]

used_letters = set(word)
words_non_used_letters = all_words

#26 listas com 5 listas cada. para cada letra, mostra as posições onde é amarela
yellow_letters = [["" for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]

#26 listas com 5 listas cada. para cada letra, mostra as posições onde é verde
green_letters = [["" for _ in range(N_LETTERS)] for _ in range(ALPHABET_SIZE)]

grey_letters = set()

for attempt in range(1, N_ATTEMPTS + 1):
    print(f"Guessed Word: {word} in Attempt {attempt}")

    words_non_used_letters.remove(word)
    
    #wordle_out é do formato a0b1c2d0e1 (os números variam entre {0, 2} e indicam a cor da letra antes)
    wordle_out = input("Wordle Out:\n")
    if wordle_out == "solved" or attempt == N_ATTEMPTS:
        exit()

    #encontra letras que não foram usadas apenas nas palavras possíveis
    extra_letters = set()
    
    word_to_try = None
    first_word = None

    if (N_ATTEMPTS - attempt + 1) < len(all_words) and attempt + 1 < N_ATTEMPTS:
        for word in words_non_used_letters:
            if attempt >= N_ATTEMPTS - 1 and len(all_words) >= 3: #se for a penúltima tentativa e tiver mais de 3 palavras possíveis ainda 
                if len(set(word) & grey_letters) == 0:
                    for yellow_letter in yellow_letters:
                        for pos in yellow_letter:
                            pass
                    word_to_try = word
                    break

            elif not (set(word) & used_letters) and len(set(word)) == N_LETTERS: #se não houver nenhuma letra já usada na palavra nem letras repetidas
                if first_word == None:
                    first_word = word
                
                if (set(word) & extra_letters): #se na palavra só existirem apenas as letras que estão nas palavras possíveis
                    word_to_try = word
                    break
                else:
                    word_to_try = first_word

        
    
    filtered_words = []
    for word in all_words:
        remove = False
        for i in range(N_LETTERS): 
            letter = wordle_out[2*i]
            colour = wordle_out[2*i + 1]
            if (colour is GREY):
                grey_letters.add(letter)
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
                yellow_letters[ord(letter) - 97][i]
                if (letter == word[i] or letter not in word) or n_dups_in_word(letter, wordle_out, i) > n_instances(letter, word):
                    remove = True                                                     
                    break 

            elif (colour is GREEN):
                yellow_letters[ord(letter) - 97][i]
                if letter != word[i]: #se a letra é verde e não está naquela posição da palavra, remove a palavra
                    remove = True
                    break

        if remove == False:
            filtered_words.append(word)
        
    all_words = filtered_words
    if DEBUG_ENABLED:
        print(all_words)
    
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

    for wordings in all_words:
        for letter in wordings:
            if letter not in used_letters:
                extra_letters.add(letter)

    if DEBUG_ENABLED:
        print("Extra Letters: ", extra_letters)
