from core.pipeline import german_nlp
from services.translator_google import GoogleTranslator
from adapters.cache_sqlite import TranslationCache
from core.flashcard_generator import generate_flashcards
from dotenv import load_dotenv
from pathlib import Path
from core.cefr_loader import load_cefr_files
from core.wiktionary_loader import load_nouns_and_verbs

load_dotenv()

noun_info, verb_info = load_nouns_and_verbs(Path("data/wiktionary/kaikki.org-dictionary-German.jsonl"))

# Load CEFR lookup (A1 for now)
cefr_lookup = load_cefr_files([
    Path("data/cefr/GermanCEFRVocabA1.csv"),
    Path("data/cefr/GermanCEFRVocabA2.csv"),
    Path("data/cefr/GermanCEFRVocabB1.csv"),
])

# Initialize cache + translator
cache = TranslationCache("translations.db")
translator = GoogleTranslator(cache)

# Test text
text = """Russlands Angriffskrieg bringt Leid und Zerstörung, beeinträchtigt die globale Stabilität und erfordert internationale Reaktionen. Wir informieren über Hintergründe und jüngste Entwicklungen."""

# Run NLP pipeline
word_data, vocab_list = german_nlp(text)

print("\nVocab List:", vocab_list)

# Translate vocab list
translations = translator.translate(vocab_list, study_lang="de", native_lang="en")

print("\nTranslations:", translations)

# Generate flashcards WITH CEFR
flashcards = generate_flashcards(
    word_data,
    translations,
    cefr_lookup,
    noun_info,
    verb_info
)

print("\nFlashcards:")
for card in flashcards:
    print(card)
