# core/link_parser.py

from newspaper import Article

def extract_article_from_link(url: str) -> dict:
    """
    Extrae el artículo completo desde un link.
    Incluye título, texto y URL de imagen destacada.
    """
    article = Article(url)
    article.download()
    article.parse()

    return {
        "title": article.title.strip(),
        "text": article.text.strip(),
        "top_image": article.top_image,  # puede estar vacío
        "source": article.source_url or url
    }

