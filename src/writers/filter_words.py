from maikol_utils.file_utils import load_json, save_json

def valid_word(word, filter_letters):
    for letter in word:
        if letter not in filter_letters:
            return False
    return True

def main():
    letters = 'arstgmnriopbjl'
    with open("writers/data/words_alpha.txt", "r", encoding="utf-8") as f:
        data = f.read().splitlines()
    filer_letters = set(list(letters))
    print(f"Filtering words with letters: {filer_letters}")
    filtered_words = [word for word in data if valid_word(word, filer_letters)]
    filtered_text = "\n".join(filtered_words)
    
    print(filtered_text)
    with open(f"writers/data/filtered_words_{letters}.txt", "w", encoding="utf-8") as f:
        f.write(filtered_text)


if __name__ == "__main__":
    main()