import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes y sin espacios sobrantes."""
    t = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")
