"""Verde Vida nursery agent configuration — data loaders and system prompt."""

from __future__ import annotations

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_catalog() -> list[dict]:
    """Load the product catalog from disk as a flat list.

    Flattens the nursery catalog into a uniform list where every product
    has a ``categoria`` field (``"arboles"`` or ``"plantas"``).
    """
    raw = json.loads((DATA_DIR / "catalog.json").read_text(encoding="utf-8"))
    products: list[dict] = []
    categorias = raw.get("categorias", {})
    for item in categorias.get("arboles", []):
        products.append({**item, "categoria": "arboles"})
    for item in categorias.get("plantas", []):
        products.append({**item, "categoria": "plantas"})
    return products


def load_faqs() -> list[dict]:
    """Load the FAQ entries from disk."""
    return json.loads((DATA_DIR / "faqs.json").read_text(encoding="utf-8"))


SYSTEM_PROMPT = """\
Eres Vera, una asesora amigable del vivero Verde Vida.

Tu función es ayudar a los clientes:
- Encontrar plantas y árboles que se ajusten a sus necesidades
- Responder preguntas sobre las políticas del vivero
- Proporcionar información y recomendaciones de productos

Sé siempre útil, concisa y profesional.
Si recomiendas un producto, menciona su precio.
"""
