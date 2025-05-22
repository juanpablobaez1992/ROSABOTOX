# core/docx_parser.py

from docx import Document
from typing import List

def extract_text_from_docx(file_path: str) -> str:
    """
    Extrae y devuelve el contenido textual de un archivo .docx.

    :param file_path: Ruta al archivo .docx.
    :return: Texto completo extraído del documento.
    """
    try:
        doc = Document(file_path)
    except Exception as e:
        raise ValueError(f"No se pudo abrir el archivo .docx: {e}")
    
    # Extraer párrafos no vacíos
    paragraphs: List[str] = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    if not paragraphs:
        return "El archivo .docx no contiene texto legible."

    full_text: str = "\n\n".join(paragraphs)
    return full_text
