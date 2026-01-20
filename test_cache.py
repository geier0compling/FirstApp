from adapters.cache_sqlite import TranslationCache, Key

# Path to your SQLite database file
DB_PATH = "translations.db"

# Create the cache object
cache = TranslationCache(DB_PATH)

# Create a Key to test with
key = Key(text="Hello world", source_lang="en", target_lang="es")

print("Reading before writing...")
print("Result:", cache.get(key))  # should be None at first

print("\nWriting new translation...")
cache.put(key, "Hola mundo")

print("\nReading after writing...")
print("Result:", cache.get(key))  # should print "Hola mundo"
