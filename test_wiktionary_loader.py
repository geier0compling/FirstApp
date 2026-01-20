from pathlib import Path
from core.wiktionary_loader import load_nouns_and_verbs

# Path to your Kaikki German dictionary
jsonl_path = Path("data/wiktionary/kaikki.org-dictionary-German.jsonl")

# Load noun + verb info
noun_info, verb_info = load_nouns_and_verbs(jsonl_path)

# Quick sanity checks
print("haus:", noun_info.get("haus"))
print("hund:", noun_info.get("hund"))
print("laufen:", verb_info.get("laufen"))
print("mitteilen:", verb_info.get("mitteilen"))
