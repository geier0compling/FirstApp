from pathlib import Path
from core.pipeline import german_nlp
from services.translator_google import GoogleTranslator
from adapters.cache_sqlite import TranslationCache
from core.flashcard_generator import generate_flashcards
from core.wiktionary_loader import load_nouns_and_verbs
from core.cefr_loader import load_cefr_files
from dotenv import load_dotenv

load_dotenv()

# ----- Load CEFR -----
cefr_lookup = load_cefr_files([
    Path("data/cefr/GermanCEFRVocabA1.csv"),
    Path("data/cefr/GermanCEFRVocabA2.csv"),
    Path("data/cefr/GermanCEFRVocabB1.csv"),
])

# ----- Load noun/verb lookup -----
noun_info, verb_info = load_nouns_and_verbs(
    Path("data/wiktionary/kaikki.org-dictionary-German.jsonl")
)

# ----- Set up translator + cache -----
cache = TranslationCache("translations.db")
translator = GoogleTranslator(cache)

# ----- Test German text -----
text = "Das Haus ist groß und der Hund läuft schnell."

word_data, vocab_list = german_nlp(text)
translations = translator.translate(vocab_list, study_lang="de", native_lang="en")

flashcards = generate_flashcards(
    word_data,
    translations,
    cefr_lookup,
    noun_info,
    verb_info
)

# ----- Print results -----
for card in flashcards:
    print("\n----------------------------")
    print("WORD:", card.word)
    print("LEMMA:", card.lemma)
    print("POS:", card.pos)
    print("TRANSLATION:", card.translation)
    print("CEFR:", card.cefr)
    print("EXAMPLE:", card.example_sentence)

    # noun formatting
    if card.pos == "NOUN":
        print("ARTICLE:", card.article)
        print("PLURAL:", card.plural)
        print("DISPLAY WORD:", card.display_word)
        print("DISPLAY DETAILS:", card.display_details)

    if card.pos == "VERB":
        print("CONJUGATIONS:", card.conjugations)
        print("DISPLAY WORD:", card.display_word)
        print("DISPLAY DETAILS:\n", card.display_details)
