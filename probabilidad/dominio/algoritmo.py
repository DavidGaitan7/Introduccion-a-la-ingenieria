"""Proceso principal. Sigue el pseudocódigo de la Ficha 4 (calcularProbabilidadCondicional).

Los números de línea de los comentarios son los del pseudocódigo.
"""
from __future__ import annotations

from .modelos import Consulta, Paso, Registro, Resultado
from .normalizacion import normalizar

PSEUDOCODIGO = {
    2: "ENTRADA: registros (lista)",
    3: "ENTRADA: tecnologia (texto)",
    4: "ENTRADA: segmento (texto)",
    5: "accesoSegmento ← 0",
    6: "accesoAmbos ← 0",
    7: "PARA CADA registro EN registros",
    8: "SI registro.segmento = segmento ENTONCES",
    9: "accesoSegmento ← accesoSegmento + registro.acceso",
    10: "SI registro.tecnologia = tecnologia ENTONCES",
    11: "accesoAmbos ← accesoAmbos + registro.acceso",
    15: "SI accesoSegmento = 0 ENTONCES",
    16: "probabilidad ← 0",
    18: "probabilidad ← accesoAmbos / accesoSegmento",
    20: "SALIDA: probabilidad",
}


def calcular_probabilidad(
    registros: list[Registro], consulta: Consulta, con_traza: bool = False
) -> Resultado:
    """P(tecnologia | segmento) = accesoAmbos / accesoSegmento."""
    pasos: list[Paso] = []
    acceso_segmento = 0.0
    acceso_ambos = 0.0
    seg_n, tec_n = normalizar(consulta.segmento), normalizar(consulta.tecnologia)

    def anotar(linea, se_cumple=None, detalle=""):
        if con_traza:
            pasos.append(
                Paso(linea, PSEUDOCODIGO[linea], se_cumple, acceso_segmento, acceso_ambos, detalle)
            )

    anotar(2, detalle=f"{len(registros)} registros")
    anotar(3, detalle=f'"{consulta.tecnologia}"')
    anotar(4, detalle=f'"{consulta.segmento}"')
    anotar(5)
    anotar(6)

    for n, reg in enumerate(registros, start=1):                      # línea 7
        anotar(7, detalle=f"registro {n}: {reg.segmento}, {reg.acceso:g}, {reg.tecnologia}")
        mismo_segmento = normalizar(reg.segmento) == seg_n            # línea 8
        anotar(8, mismo_segmento)
        if mismo_segmento:
            acceso_segmento += reg.acceso                             # línea 9
            anotar(9)
            misma_tecnologia = normalizar(reg.tecnologia) == tec_n    # línea 10
            anotar(10, misma_tecnologia)
            if misma_tecnologia:
                acceso_ambos += reg.acceso                            # línea 11
                anotar(11)

    sin_accesos = acceso_segmento == 0                                # línea 15
    anotar(15, sin_accesos)
    if sin_accesos:
        probabilidad = 0.0                                            # línea 16
        anotar(16)
    else:
        probabilidad = acceso_ambos / acceso_segmento                 # línea 18
        anotar(18, detalle=f"{acceso_ambos:g} / {acceso_segmento:g} = {probabilidad:.4f}")
    anotar(20, detalle=f"probabilidad = {probabilidad:.4f}")

    return Resultado(acceso_segmento, acceso_ambos, probabilidad, pasos)
