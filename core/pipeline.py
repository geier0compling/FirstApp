import spacy
from typing import List, Dict, Tuple

nlp = spacy.load('de_core_news_md')
POS_WHITELIST = {"NOUN", "VERB", "ADJ", "ADV", "NUM"}

def german_nlp(text: str) -> Tuple[List[Dict], List[str]]:
    # Load Spacy's German model
    doc = nlp(text)

    # 🔹 Pre-calculate all sentence boundaries once
    sentences = list(doc.sents)

    # Initialize a list
    word_data: List[Dict] = []

    # append token, pos, and lemma to the list
    for token in doc:
        # 🔹 Find the sentence this token belongs to
        sentence_text = token.sent.text

        entry = {
            "word": token.text,
            "pos_tag": token.pos_,
            "lemma": token.lemma_,
            "is_stop": token.is_stop,
            "is_punct": token.is_punct,
            "is_space": token.is_space,
            "lemma_lower": token.lemma_.lower(),
            "is_alpha": token.is_alpha,

            # 🔹 New field: the full example sentence
            "sentence": sentence_text
        }
        word_data.append(entry)

    filtered: List[Dict] = []
    for w in word_data:
        if w["pos_tag"] not in POS_WHITELIST:
            continue
        if w["is_stop"] or w["is_punct"] or w["is_space"]:
            continue
        if not w["is_alpha"]:
            continue
        if w["pos_tag"] == "PROPN":
            continue
        filtered.append(w)

    # Deduplicate by lemma (case-insensitive)
    seen = set()
    vocab_list: List[str] = []
    for w in filtered:
        lemma_norm = w["lemma"].lower().strip()
        if lemma_norm and lemma_norm not in seen:
            seen.add(lemma_norm)
            vocab_list.append(lemma_norm)

    # Optional: quick console preview for sanity
    print("Original words:")
    for w in word_data:
        print(
            f"{w['word']:>15}  stop={w['is_stop']} punct={w['is_punct']} space={w['is_space']} pos={w['pos_tag']}")

    print("\nFiltered (kept) lemmas:")
    for l in vocab_list:
        print(f"  {l}")

    return word_data, vocab_list

if __name__ == "__main__":
    sample = (
        "Ich habe vor einem Jahr angefangen, regelmäßig zu reisen, um neue Kulturen kennenzulernen. Besonders beeindruckt hat mich Japan, weil die Menschen dort unglaublich höflich und respektvoll sind. Während meiner Reise habe ich viele traditionelle Gerichte probiert und versucht, ein paar japanische Wörter zu lernen. Seitdem interessiere ich mich noch mehr für Sprachen und möchte eines Tages fließend Japanisch sprechen. Reisen hat mir gezeigt, wie wichtig Offenheit und Neugier im Leben sind."
    )
    _, vocab = german_nlp(sample)
    print("\nUnique vocab lemmas:", vocab)

 #def french_nlp(text):

#def spanish_nlp(text):

#def korean_nlp(text):

#def chinese_nlp(text):



# def generate_flash_cards(text):
#     # Load Spacy's German model
#     nlp = spacy.load('de_core_news_md')
#     doc = nlp(text)
#
#     # Initialize the dictionary of lists
#     tagged_words_dict = {
#         "NOUN": [],
#         "VERB": [],
#         "ADJ": [],
#         "PRON": [],
#         "PUNCT": [],
#         "ADV": [],
#         "AUX": [],
#         "ADP": [],
#         "DET": []
#     }
#
#     # Add the words to the correct list based on their POS tag
#     for token in doc:
#         if token.pos_ in tagged_words_dict:
#             tagged_words_dict[token.pos_].append(token.text)
#
#     # Load Spacy's German model
#     nlp = spacy.load('de_core_news_md')
#
#     # Initialize a new dictionary of lists for the lemmas
#     lemmatized_words_dict = {
#         "NOUN": [],
#         "VERB": [],
#         "ADJ": [],
#         "PRON": [],
#         "PUNCT": [],
#         "ADV": [],
#         "AUX": [],
#         "ADP": [],
#         "DET": []
#     }
#
#     # Iterate over each category and each word in each category
#     for tag in tagged_words_dict:
#         for word in tagged_words_dict[tag]:
#             # Lemmatize the word
#             lemma = nlp(word)[0].lemma_
#             # Add the lemma to the correct list
#             lemmatized_words_dict[tag].append(lemma)
#
#     # Set up the Google Cloud Translation API client
#     # create translator object
#     translator = Translator()
#
#     # define a function that will translate a list of words from german to english
#     def translate_text(text, source_lang="de", target_lang="en"):
#         translator = Translator()
#         translation = translator.translate(text, src=source_lang, dest=target_lang)
#         return translation.text
#
#     def translate_words(words, source_lang="de", target_lang="en"):
#         translation_dict = {}
#         for word in words:
#             translated_word = translate_text(word, source_lang, target_lang)
#             translation_dict[word] = translated_word
#         return translation_dict
#
#     # translate nouns
#     nouns = lemmatized_words_dict["NOUN"]
#     translated_nouns = translate_words(nouns)
#     print("Translated Nouns:", translated_nouns)
#
#     # translate verbs
#     verbs = lemmatized_words_dict["VERB"]
#     translated_verbs = translate_words(verbs)
#     print("Translated Verbs:", translated_verbs)
#
#     # translate adj
#     adj = lemmatized_words_dict["ADJ"]
#     translated_adj = translate_words(adj)
#     print("Translated Adjectives:", translated_adj)
#
#     output_str = ""
#
#     gender_dict = {'Femininum': 'die', 'Maskulinum': 'der', 'Neutrum': 'das'}
