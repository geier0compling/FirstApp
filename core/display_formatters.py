def format_noun(article: str, lemma: str, plural: str | None) -> dict:
    """
    Produces display-ready noun forms:
    - 'display_word' → e.g., 'das Haus'
    - 'display_details' → e.g., 'Plural: Häuser'
    """
    # Capitalize lemma for German nouns
    lemma_cap = lemma.capitalize()

    display_word = f"{article} {lemma_cap}" if article else lemma_cap

    if plural:
        # Plural also capitalized
        plural_cap = plural.capitalize()
        display_details = f"die {plural_cap}"
    else:
        display_details = None

    return {
        "display_word": display_word,
        "display_details": display_details
    }

def format_verb(lemma: str, conjugations: dict) -> dict:
    """
    Create display-ready verb forms.
    Handles separable-prefix detection and formatting.
    Returns:
      {
        "display_word": "mit·teilen",
        "display_details": "3sg: ...\nPräteritum: ...\nPartizip II: ..."
      }
    """

    # --- 1. Detect separable verb prefix using 3sg form ---
    display_lemma = lemma
    sep_dot = "·"

    third = conjugations.get("3sg")

    if third and " " in third:
        # Example: "teilt mit" -> ["teilt", "mit"]
        parts = third.split()
        verb_stem = parts[0]           # "teilt"
        prefix = parts[-1]             # "mit"

        # If lemma starts with prefix (normal case)
        if lemma.startswith(prefix):
            base = lemma[len(prefix):]
            display_lemma = f"{prefix}{sep_dot}{base}"

    # --- 2. Build details list ---
    lines = []

    if conjugations.get("3sg"):
        lines.append(f"3sg: {conjugations['3sg']}")

    if conjugations.get("preterite"):
        lines.append(f"Präteritum: {conjugations['preterite']}")

    if conjugations.get("participle"):
        lines.append(f"Partizip II: {conjugations['participle']}")

    display_details = "\n".join(lines) if lines else None

    return {
        "display_word": display_lemma,
        "display_details": display_details
    }
