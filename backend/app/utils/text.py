import re


def clean_complaint_text(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized


def excerpt(text: str, limit: int = 240) -> str:
    clean = clean_complaint_text(text)
    return clean if len(clean) <= limit else f"{clean[: limit - 3]}..."

