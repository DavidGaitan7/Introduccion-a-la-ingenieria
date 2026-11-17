"""Capa de dominio: los conceptos del problema, sin depender de nada externo."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Registro:
    """Un dato de entrada: accesos de una tecnología en un segmento."""
    segmento: str
    tecnologia: str
    acceso: float
    departamento: str = ""   # opcional: solo si el archivo lo trae
    periodo: str = ""        # opcional: por ejemplo "2024-T1"


@dataclass(frozen=True)
class Consulta:
    """Lo que el usuario quiere saber: P(tecnologia | segmento)."""
    segmento: str
    tecnologia: str


@dataclass(frozen=True)
class Paso:
    """Una fila de la prueba de escritorio."""
    linea: int
    instruccion: str
    se_cumple: bool | None
    acceso_segmento: float
    acceso_ambos: float
    detalle: str = ""


@dataclass
class Resultado:
    acceso_segmento: float
    acceso_ambos: float
    probabilidad: float
    pasos: list[Paso] = field(default_factory=list)


@dataclass
class Lectura:
    """Registros válidos y los errores encontrados al leer una fuente."""
    registros: list[Registro]
    errores: list[str] = field(default_factory=list)
