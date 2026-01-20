from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Flashcard:
    word: str                    # surface form from text
    lemma: str                   # dictionary form
    pos: str                     # POS tag
    translation: str             # English translation
    cefr: Optional[str] = None   # CEFR level
    example_sentence: Optional[str] = None  # Example sentence

    # --- Noun features ---
    article: Optional[str] = None
    plural: Optional[str] = None

    # --- Verb features ---
    conjugations: Optional[Dict[str, Optional[str]]] = None

    # --- Display formatting ---
    display_word: Optional[str] = None
    display_details: Optional[str] = None
