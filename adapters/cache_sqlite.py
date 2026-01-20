# adapters/cache_sqlite.py
from dataclasses import dataclass
from typing import Optional
import sqlite3

@dataclass(frozen=True)
class Key:
    source_text: str        # the lemma/word in the STUDY language
    study_lang: str         # e.g., "de"
    native_lang: str        # e.g., "en"

class TranslationCache:
    def __init__(self, db_path: str = "translations.db"):
        self.db_path = db_path
        self._ensure_schema()

    def _connection(self):
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self):
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    source_text   TEXT NOT NULL,
                    study_lang    TEXT NOT NULL,
                    native_lang   TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    created_at    TEXT DEFAULT (datetime('now')),
                    PRIMARY KEY (source_text, study_lang, native_lang)
                )
            """)
            conn.commit()

    def get(self, key: Key) -> Optional[str]:
        """
        Return cached translation if present; else None.
        """
        with self._connection() as conn:
            cur = conn.execute(
                """
                SELECT translated_text
                FROM translations
                WHERE source_text = ?
                  AND study_lang  = ?
                  AND native_lang = ?
                LIMIT 1
                """,
                (key.source_text, key.study_lang, key.native_lang)
            )
            row = cur.fetchone()
            return row[0] if row else None

    def put(self, key: Key, translated_text: str) -> None:
        """
        Upsert a translation for (source_text, study_lang, native_lang).
        """
        with self._connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO translations
                    (source_text, study_lang, native_lang, translated_text, created_at)
                VALUES (?, ?, ?, ?, datetime('now'))
                """,
                (key.source_text, key.study_lang, key.native_lang, translated_text)
            )
            conn.commit()
