"""Verifica la regla de dependencias entre capas leyendo los imports."""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "probabilidad"

# capa -> imports que NO puede usar
PROHIBIDO = {
    "dominio": ["streamlit", "pandas", "probabilidad.aplicacion", "probabilidad.infraestructura", "probabilidad.presentacion"],
    "aplicacion": ["streamlit", "pandas", "probabilidad.infraestructura", "probabilidad.presentacion"],
    "infraestructura": ["streamlit", "probabilidad.presentacion", "probabilidad.aplicacion.servicios"],
    "presentacion": ["probabilidad.infraestructura", "probabilidad.dominio.algoritmo"],
}


def imports_de(archivo):
    texto = archivo.read_text(encoding="utf-8")
    return re.findall(r"^\s*(?:from|import)\s+([\w.]+)", texto, flags=re.M)


def test_ninguna_capa_rompe_la_regla_de_dependencias():
    fallos = []
    for capa, prohibidos in PROHIBIDO.items():
        for py in (RAIZ / capa).glob("*.py"):
            for imp in imports_de(py):
                if any(imp == p or imp.startswith(p + ".") for p in prohibidos):
                    fallos.append(f"{capa}/{py.name} importa {imp}")
    assert fallos == []
