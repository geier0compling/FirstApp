
# This Translator class will represent a contract
# Whatever text is getting translated we will ensure that these parameters are met before sending translating
# The actual translator itself will need to follow these rules
# translate method:
#   Accept a list of strings ("texts") to translate.
#   Accept language codes ("src", "tgt") in ISO form (e.g., "de", "en").
#   Return a list of translated strings in the same order.
#   Raise a clear error if languages are unsupported.


from abc import ABC, abstractmethod
from typing import List, Dict

class Translator(ABC):
    """
    This class defines the 'contract' or rule that all translator classes must follow.
    Any translator you create (Google, DeepL, etc.) must have the same translate() method.
    """

    @abstractmethod
    def translate(self, words: List[str], study_lang: str, native_lang: str) -> Dict[str, str]:
        """
        Translate a list of words from the language you're studying into your native language.

        Parameters:
            words (List[str]): The list of words you want translated.
            study_lang (str):  The language you are learning (for example: 'de' for German).
            native_lang (str): Your native language (for example: 'en' for English).

        Returns:
            Dict[str, str]: A dictionary mapping each word to its translated version.
                            Example: { 'Haus': 'house', 'laufen': 'to run' }
        """
        pass
