"""Contratos que la capa de aplicación necesita de la infraestructura."""
from __future__ import annotations

from typing import Protocol

from probabilidad.dominio.modelos import Lectura, Registro


class LectorTexto(Protocol):
    def leer(self, texto: str) -> Lectura: ...


class LectorCSV(Protocol):
    def leer(self, contenido: bytes | str) -> Lectura: ...


class GeneradorDatos(Protocol):
    def generar(self, cantidad: int) -> list[Registro]: ...
