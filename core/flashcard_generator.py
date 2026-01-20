from typing import List, Dict
from core.flashcard_model import Flashcard
from core.display_formatters import format_noun, format_verb

def generate_flashcards(
    word_data: List[dict],
    translations: Dict[str, str],
    cefr_lookup: Dict[str, str],
    noun_info: Dict[str, Dict[str, str]],
    verb_info: Dict[str, Dict[str, str]],
) -> List[Flashcard]:

    flashcards: List[Flashcard] = []

    for entry in word_data:
        lemma = entry["lemma"].lower()
        pos = entry["pos_tag"]

        # Skip words without a translation
        if lemma not in translations:
            continue

        # CEFR fallback = B2+ / Unknown
        cefr = cefr_lookup.get(lemma, "B2+ / Unknown")

        # Example sentence from the pipeline
        example_sentence = entry.get("sentence")

        # Base flashcard
        card = Flashcard(
            word=entry["word"],
            lemma=lemma,
            pos=pos,
            translation=translations[lemma],
            cefr=cefr,
            example_sentence=example_sentence,
        )

        # ---------------------
        # NOUN FEATURES
        # ---------------------
        if pos == "NOUN" and lemma in noun_info:
            info = noun_info[lemma]
            card.article = info.get("article")
            card.plural = info.get("plural")

            # Display formatting for nouns
            formatted = format_noun(
                article=card.article,
                lemma=card.lemma,
                plural=card.plural,
            )
            card.display_word = formatted["display_word"]
            card.display_details = formatted["display_details"]

        # ---------------------
        # VERB FEATURES
        # ---------------------
        if pos == "VERB" and lemma in verb_info:
            conj = verb_info[lemma]
            card.conjugations = conj

            # Display formatting for verbs
            formatted = format_verb(lemma, conj)
            card.display_word = formatted["display_word"]
            card.display_details = formatted["display_details"]

        flashcards.append(card)

    return flashcards

