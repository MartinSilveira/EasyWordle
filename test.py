from sources.others.config import *

with open(WORD_DUPS_PATH, "r") as all_words_file:
    all_words = [line[:5] for line in all_words_file]

og_all_words = all_words

used_letters = set()
while True:
    word_to_try = None
    
    word_in = input("Insert Word: ")
    if word_in == 'q':
        exit()

    og_all_words.remove(word_in)
    
    for letter in word_in:
        used_letters.add(letter)

    print("Used Letters: ", used_letters)

    extra_letters = set()
    for word in all_words:
        for letter in word:
            if letter not in used_letters:
                extra_letters.add(letter)

    print("Extra Letters: ", extra_letters)

    for word in all_words:
        if not (set(word) & used_letters) and len(set(word)) == N_LETTERS:
            if (set(word) & extra_letters):
                word_to_try = word
                print("Used Option 1")
                break
            else:
                word_to_try = word
                print("Used Option 2")
                break
    
    if word_to_try == None:
        for word in og_all_words:
            if (len(set(word) & used_letters) <= 2) and len(set(word)) == N_LETTERS:
                word_to_try = word
                print("Used Option 3")
                break
        
    print(word)