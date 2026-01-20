import json
import requests


def load_nouns_and_verbs_from_url(url):
    """
    Stream Wiktionary JSONL from a remote URL (HuggingFace)
    and extract noun and verb info just like the local loader.
    """
    noun_info = {}
    verb_info = {}

    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # fail fast if bad URL

        for raw_line in r.iter_lines(decode_unicode=True):
            if not raw_line:
                continue

            try:
                entry = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            pos = entry.get("pos", "").lower()
            lemma = entry.get("word")

            if not lemma or not pos:
                continue

            # --------------------
            # NOUN EXTRACTION LOGIC
            # --------------------
            if pos == "noun":
                gender = entry.get("gender")
                plural = entry.get("plural")
                definition = entry.get("definition")
                example = entry.get("example")

                noun_info[lemma] = {
                    "gender": gender,
                    "plural": plural,
                    "definition": definition,
                    "example": example,
                }

            # --------------------
            # VERB EXTRACTION LOGIC
            # --------------------
            elif pos == "verb":
                # You may expand this later to include conjugations
                definition = entry.get("definition")
                example = entry.get("example")

                verb_info[lemma] = {
                    "definition": definition,
                    "example": example,
                }

    return noun_info, verb_info
