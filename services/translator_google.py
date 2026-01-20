# services/translator_google.py

from typing import List, Dict
from services.translator import Translator
from adapters.cache_sqlite import TranslationCache, Key
from google.cloud import translate_v2 as translate

def split_into_batches(items, batch_size=50):
    """Yield slices of the list in chunks of batch_size."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

class GoogleTranslator(Translator):

    def __init__(self, cache: TranslationCache):
        # store the cache so translate() can use it
        self.cache = cache
        self.client = translate.Client()

    def translate(self, words: List[str], study_lang: str, native_lang: str) -> Dict[str, str]:
        translations: Dict[str, str] = {}
        to_translate: List[str] = []

        # First pass: check cache
        for word in words:
            key = Key(
                source_text=word,
                study_lang=study_lang,
                native_lang=native_lang
            )

            cached_value = self.cache.get(key)

            if cached_value is not None:
                print(f"[CACHE HIT] {word} -> {cached_value}")
                translations[word] = cached_value
            else:
                to_translate.append(word)

        # If everything was cached
        if not to_translate:
            return translations

        # Batching
        for batch in split_into_batches(to_translate, batch_size=50):
            try:
                # First API attempt
                api_results = self.client.translate(
                    batch,
                    source_language=study_lang,
                    target_language=native_lang,
                    format_="text",
                )
            except Exception as e:
                print(f"[WARNING] Batch failed, retrying once... {e}")
                # Retry once
                api_results = self.client.translate(
                    batch,
                    source_language=study_lang,
                    target_language=native_lang,
                    format_="text",
                )

            # Process batch results
            for word, res in zip(batch, api_results):
                translated_text = res["translatedText"]

                key = Key(
                    source_text=word,
                    study_lang=study_lang,
                    native_lang=native_lang
                )

                # Save to cache
                self.cache.put(key, translated_text)

                # Save to output
                translations[word] = translated_text

        return translations
