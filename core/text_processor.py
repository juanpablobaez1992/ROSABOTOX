# core/text_processor.py

from slugify import slugify
from typing import Dict, List
import re
from collections import Counter

CATEGORIES_KEYWORDS = {
    "Vaticano": ["vaticano", "roma", "santa sede", "curia", "audiencia general"],
    "Papa": ["papa francisco", "sumo pontífice", "bergoglio", "mensaje del papa"],
    "Nuestra Iglesia": ["parroquia", "obispado", "diócesis", "comunidad cristiana", "misa", "sacerdote"],
    "sociedad": ["protesta", "comunidad", "vecinos", "familia", "pobreza", "educación"],
    "Espiritualidad": ["oración", "fe", "espiritualidad", "adoración", "retiro", "reflexión"],
    "Testimonios": ["testimonio", "vida cristiana", "milagro", "conversión", "vocación"]
}


def generate_article_structure(text: str) -> Dict:
    paragraphs: List[str] = [p.strip() for p in text.split("\n") if p.strip()]
    
    if not paragraphs:
        raise ValueError("El texto está vacío o no contiene párrafos válidos.")
    
    title = paragraphs[0]
    slug = slugify(title)
    body_paragraphs = paragraphs[1:]

    # Subtítulo heurístico
    if len(paragraphs) > 1 and len(paragraphs[1]) > 40:
        subtitle = paragraphs[1]
        body = "\n\n".join(paragraphs[2:]) if len(paragraphs) > 2 else ""
    else:
        subtitle = generate_subtitle_from_body(body_paragraphs)
        body = "\n\n".join(body_paragraphs)

    keywords = extract_keywords(text)
    category = guess_category(text)

    return {
        "title": title,
        "slug": slug,
        "excerpt": subtitle,
        "seo": {
            "description": subtitle,
            "keywords": keywords
        },
        "categories": [category] if category else [],
        "tags": keywords[:5],
        "body": body
    }

def extract_keywords(text: str, stopwords: List[str] = None) -> List[str]:
    if stopwords is None:
        stopwords = ["el", "la", "los", "las", "de", "y", "en", "a", "un", "una", "por", "para", "con", "es", "al", "del"]

    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    freq = Counter(filtered_words)
    keywords = [word for word, _ in freq.most_common(10)]
    return keywords

def guess_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORIES_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return "general"

def generate_subtitle_from_body(paragraphs: List[str]) -> str:
    for p in paragraphs:
        if len(p.split()) > 6 and len(p) < 200:
            return p
    return paragraphs[0] if paragraphs else ""
