with open("words_to_fix.txt", "r") as words_file:
    all_words = [line.strip() for line in words_file]

all_words_set = set(all_words)

with open("words_to_fix.txt", "w") as words_file:
    for word in all_words_set:
        words_file.write(f"{word}\n")
        print(word)