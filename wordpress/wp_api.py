# wordpress/wp_api.py

import requests
from typing import Dict, List
from config import WP_URL, WP_USER, WP_APP_PASSWORD

auth = (WP_USER, WP_APP_PASSWORD)

def get_or_create_category(name: str) -> int:
    """
    Busca una categoría por nombre o la crea si no existe. Devuelve su ID.
    """
    name = name.strip()
    endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
    response = requests.get(endpoint, auth=auth, params={"search": name})

    if response.status_code == 200 and response.json():
        return response.json()[0]["id"]

    # Crear categoría si no existe
    response = requests.post(endpoint, auth=auth, json={"name": name})
    if response.status_code in [200, 201]:
        return response.json()["id"]
    else:
        raise Exception(f"Error al crear categoría: {response.text}")

def get_or_create_tag(name: str) -> int:
    """
    Busca una etiqueta por nombre o la crea si no existe. Devuelve su ID.
    """
    name = name.strip()
    endpoint = f"{WP_URL}/wp-json/wp/v2/tags"
    response = requests.get(endpoint, auth=auth, params={"search": name})

    if response.status_code == 200 and response.json():
        return response.json()[0]["id"]

    # Crear etiqueta si no existe
    response = requests.post(endpoint, auth=auth, json={"name": name})
    if response.status_code in [200, 201]:
        return response.json()["id"]
    else:
        raise Exception(f"Error al crear etiqueta: {response.text}")

def create_draft_post(article: Dict, featured_image_id: int = None) -> Dict:
    """
    Publica un post como borrador en WordPress.
    Si se detectan categorías o etiquetas, las verifica/crea y asocia.
    """
    category_ids = [get_or_create_category(cat) for cat in article.get("categories", [])]
    tag_ids = [get_or_create_tag(tag) for tag in article.get("tags", [])]

    payload = {
        "title": article["title"],
        "slug": article["slug"],
        "excerpt": article["excerpt"],
        "content": article["body"],
        "status": "draft",
        "categories": category_ids,
        "tags": tag_ids,
    }

    if featured_image_id:
        payload["featured_media"] = featured_image_id

    endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
    response = requests.post(endpoint, auth=auth, json=payload)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Error al crear post: {response.status_code} – {response.text}")
