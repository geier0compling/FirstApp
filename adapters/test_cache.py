from adapters.cache_sqlite import TranslationCache, Key

def main():
    # 1) Create cache (this will also create translations.db and the table)
    cache = TranslationCache("translations.db")

    # 2) Make a key: German ("de") word → English ("en")
    key = Key(
        source_text="Haus",
        study_lang="de",
        native_lang="en"
    )

    # 3) First read: should be empty (None)
    print("First get (should be None):", cache.get(key))

    # 4) Save a translation
    cache.put(key, "house")

    # 5) Second read: should now return 'house'
    print("Second get (should be 'house'):", cache.get(key))

if __name__ == "__main__":
    main()

