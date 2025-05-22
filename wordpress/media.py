# wordpress/media.py

import requests
import mimetypes
from config import WP_URL, WP_USER, WP_APP_PASSWORD

def upload_image_to_wordpress(image_path: str, image_name: str) -> int:
    """
    Sube una imagen a WordPress como 'media' y devuelve su ID.
    Soporta JPEG, PNG, WebP, etc.
    """
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"  # valor por defecto

    headers = {
        'Content-Disposition': f'attachment; filename="{image_name}"',
        'Content-Type': mime_type
    }

    endpoint = f"{WP_URL}/wp-json/wp/v2/media"
    auth = (WP_USER, WP_APP_PASSWORD)

    with open(image_path, 'rb') as img:
        response = requests.post(endpoint, headers=headers, auth=auth, data=img)

    if response.status_code in [200, 201]:
        media = response.json()
        print(f"Imagen subida: ID={media['id']} URL={media['source_url']}")
        return media["id"]
    else:
        raise Exception(f"Error al subir imagen: {response.status_code} – {response.text}")
