from typing import Dict, Iterable
from pathlib import Path
import csv


def load_cefr_files(paths: Iterable[Path]) -> Dict[str, str]:
    """
    Build a lookup dict: lemma_lower -> CEFR level (e.g. 'A1', 'A2', ...)
    If a lemma appears in multiple levels, we keep the first one we see
    (usually the easiest level, like A1).
    """
    cefr: Dict[str, str] = {}

    for path in paths:
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lemma = row["Lower"].strip().lower()
                level = row["Level"].strip()

                if not lemma or not level:
                    continue

                # Keep the first (typically lowest) level we see
                if lemma not in cefr:
                    cefr[lemma] = level

    return cefr
