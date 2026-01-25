from pathlib import Path
from dataclasses import asdict
from typing import Any, Dict, List
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from core.pipeline import german_nlp
from core.flashcard_generator import generate_flashcards
from core.cefr_loader import load_cefr_files
from adapters.cache_sqlite import TranslationCache
from services.translator_google import GoogleTranslator
from core.wiktionary_loader import load_nouns_and_verbs_from_url
import requests


# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

# ---------------------------
# Create FastAPI app
# ---------------------------
app = FastAPI(title="German Flashcard App")

@app.get("/api/random-german")
def random_german():
    url = "https://de.wikipedia.org/api/rest_v1/page/random/summary"
    headers = {
        "User-Agent": "GermanFlashcardApp/1.0 (local dev)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=8)

        # If Wikipedia blocks us, don't crash the app
        if r.status_code != 200:
            return {"text": "Ich lerne gerade Deutsch. Das ist ein Beispielsatz. Heute ist das Wetter schön."}

        data = r.json()
        text = (data.get("extract") or "").strip()

        if not text:
            text = "Ich lerne gerade Deutsch. Das ist ein Beispielsatz. Heute ist das Wetter schön."

        return {"text": text}

    except Exception:
        # Any network/JSON issue: still return something usable
        return {"text": "Ich lerne gerade Deutsch. Das ist ein Beispielsatz. Heute ist das Wetter schön."}

# ---------------------------
# CORS (safe for local dev)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "ui"

# ---------------------------
# Serve frontend
# ---------------------------
app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

@app.get("/")
def serve_ui():
    return FileResponse(UI_DIR / "index.html")

# ---------------------------
# Load CEFR files
# ---------------------------
cefr_lookup = load_cefr_files([
    BASE_DIR / "data/cefr/GermanCEFRVocabA1.csv",
    BASE_DIR / "data/cefr/GermanCEFRVocabA2.csv",
    BASE_DIR / "data/cefr/GermanCEFRVocabB1.csv",
])

# ---------------------------
# Load Wiktionary data
# ---------------------------
WIKTIONARY_URL = os.getenv("WIKTIONARY_URL")
print("WIKTIONARY_URL =", WIKTIONARY_URL)
print("GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

noun_info, verb_info = load_nouns_and_verbs_from_url(WIKTIONARY_URL)

# ---------------------------
# Translator + cache
# ---------------------------
cache = TranslationCache(str(BASE_DIR / "translations.db"))
translator = GoogleTranslator(cache)

# ---------------------------
# Request model
# ---------------------------
class FlashcardRequest(BaseModel):
    text: str

# ---------------------------
# API Routes
# ---------------------------
@app.post("/api/flashcards")
def create_flashcards(payload: FlashcardRequest) -> Dict[str, List[Dict[str, Any]]]:
    text = payload.text.strip()
    if not text:
        return {"flashcards": []}

    # 1. NLP pipeline
    word_data, vocab_list = german_nlp(text)

    # 2. Translate
    translations = translator.translate(
        vocab_list,
        study_lang="de",
        native_lang="en",
    )

    # 3. Generate flashcards
    flashcards = generate_flashcards(
        word_data=word_data,
        translations=translations,
        cefr_lookup=cefr_lookup,
        noun_info=noun_info,
        verb_info=verb_info,
    )

    # 4. Convert to JSON-safe dicts
    return {"flashcards": [asdict(card) for card in flashcards]}

@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}
