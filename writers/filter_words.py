import pandas as pd

def valid_word(word, filter_letters):
    for letter in word:
        if letter not in filter_letters:
            return False
    return True

def main():
    letters = 'a r s t g m n r i o p b j l c d v k w f u y'
    must_include = 'w f u y j b k'
    filter_letters = set(letters.split(" "))
    print(f"Filtering words with letters: {filter_letters}")
    
    # ================== ENGLISH WORDS ==================
    with open("writers/data/words_alpha.txt", "r", encoding="utf-8") as f:
        data = f.read().splitlines()

    filtered_words = [word for word in data if valid_word(word, filter_letters)]
    filtered_text_en = "\n".join(filtered_words)
    # ================== SPANISH WORDS ==================
    spanish_words_df = pd.read_csv("writers/data/10000_formas.TXT", sep="\t", skipinitialspace=True, encoding="latin-1")
    spanish_words = spanish_words_df.iloc[:, 1].dropna().tolist()
    spanish_filtered = [word for word in spanish_words if valid_word(str(word), filter_letters)]
    filtered_text_es = "\n".join(spanish_filtered)
    
    print(f"\nEnglish words: {len(filtered_words)}")
    print(f"Spanish words: {len(spanish_filtered)}")
    # print(f"\nCombined filtered words:\n{filtered_text_es + filtered_text_en}")

    with open(f"writers/data/filtered_words_en_es{letters}.txt", "w", encoding="utf-8") as f:
        f.write(filtered_text_en)
        f.write(filtered_text_es)


if __name__ == "__main__":
    main()