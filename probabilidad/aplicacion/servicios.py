"""Capa de aplicación: casos de uso. Coordina el dominio y los puertos."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from probabilidad.dominio.algoritmo import calcular_probabilidad
from probabilidad.dominio.modelos import Consulta, Registro, Resultado

from .puertos import GeneradorDatos, LectorCSV, LectorTexto

MAX_REGISTROS_CON_TRAZA = 30
MIN_SINTETICOS, MAX_SINTETICOS = 100, 2_000_000


class ErrorDeEntrada(ValueError):
    """El usuario dio datos que no se pueden procesar."""


@dataclass
class Respuesta:
    consulta: Consulta
    resultado: Resultado
    total_registros: int
    milisegundos: float
    con_traza: bool
    errores_lectura: list[str] = field(default_factory=list)
    filtros: str = ""

    @property
    def segmento_sin_datos(self) -> bool:
        return self.resultado.acceso_segmento == 0


class ServicioProbabilidad:
    def __init__(self, lector_texto: LectorTexto, lector_csv: LectorCSV, generador: GeneradorDatos):
        self._lector_texto = lector_texto
        self._lector_csv = lector_csv
        self._generador = generador

    def consultar_texto(self, texto: str, segmento: str, tecnologia: str) -> Respuesta:
        lectura = self._lector_texto.leer(texto)
        return self.consultar(lectura.registros, segmento, tecnologia, lectura.errores)

    def consultar(
        self,
        registros: list[Registro],
        segmento: str,
        tecnologia: str,
        errores_lectura: list[str] | None = None,
        departamento: str | None = None,
        periodo: str | None = None,
    ) -> Respuesta:
        filtros = ""
        if departamento or periodo:
            registros = self.filtrar(registros, departamento, periodo)
            filtros = " · ".join(x for x in (departamento, periodo) if x)
            if not registros:
                raise ErrorDeEntrada(f"No hay registros para {filtros}.")
        if not segmento.strip() or not tecnologia.strip():
            raise ErrorDeEntrada("Escribe el segmento y la tecnología que quieres consultar.")
        if not registros:
            raise ErrorDeEntrada("No hay registros válidos para calcular.")

        consulta = Consulta(segmento.strip(), tecnologia.strip())
        con_traza = len(registros) <= MAX_REGISTROS_CON_TRAZA
        t0 = time.perf_counter()
        resultado = calcular_probabilidad(registros, consulta, con_traza)
        ms = (time.perf_counter() - t0) * 1000
        return Respuesta(consulta, resultado, len(registros), ms, con_traza, errores_lectura or [], filtros)

    @staticmethod
    def opciones_filtro(registros: list[Registro]) -> tuple[list[str], list[str]]:
        """Departamentos y períodos que trae el archivo (vacíos si no los tiene)."""
        deps = sorted({r.departamento for r in registros if r.departamento})
        pers = sorted({r.periodo for r in registros if r.periodo})
        return deps, pers

    @staticmethod
    def filtrar(registros: list[Registro], departamento: str | None = None, periodo: str | None = None) -> list[Registro]:
        return [
            r for r in registros
            if (not departamento or r.departamento == departamento) and (not periodo or r.periodo == periodo)
        ]

    def cargar_csv(self, contenido: bytes | str) -> tuple[list[Registro], list[str]]:
        lectura = self._lector_csv.leer(contenido)
        if not lectura.registros:
            raise ErrorDeEntrada("El archivo no tiene registros válidos.")
        return lectura.registros, lectura.errores

    def generar_datos(self, cantidad: int) -> list[Registro]:
        if not MIN_SINTETICOS <= cantidad <= MAX_SINTETICOS:
            raise ErrorDeEntrada(f"La cantidad debe estar entre {MIN_SINTETICOS:,} y {MAX_SINTETICOS:,}.")
        return self._generador.generar(cantidad)
