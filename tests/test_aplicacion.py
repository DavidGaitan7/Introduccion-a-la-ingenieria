"""El servicio se prueba con lectores falsos: no depende de la infraestructura real."""
import time

import pytest

from probabilidad.aplicacion.servicios import ErrorDeEntrada, ServicioProbabilidad
from probabilidad.dominio.modelos import Lectura, Registro
from probabilidad.infraestructura.generador import GeneradorSintetico

REGS = [Registro("Estrato1", "Fibra", 120), Registro("Estrato1", "Cable", 380)]


class LectorFalso:
    def leer(self, _):
        return Lectura(REGS, ["Línea 3: mala"])


class GeneradorFalso:
    def generar(self, n):
        return REGS * n


def servicio():
    return ServicioProbabilidad(LectorFalso(), LectorFalso(), GeneradorFalso())


def test_consultar_texto_devuelve_respuesta_completa():
    r = servicio().consultar_texto("x", "Estrato1", "Fibra")
    assert r.resultado.probabilidad == pytest.approx(0.24)
    assert r.errores_lectura == ["Línea 3: mala"] and r.con_traza


def test_consulta_sin_segmento_falla():
    with pytest.raises(ErrorDeEntrada):
        servicio().consultar(REGS, "  ", "Fibra")


def test_sin_registros_falla():
    with pytest.raises(ErrorDeEntrada):
        servicio().consultar([], "Estrato1", "Fibra")


def test_cantidad_sintetica_fuera_de_rango():
    with pytest.raises(ErrorDeEntrada):
        servicio().generar_datos(5)


def test_eficiencia_50000_registros_en_menos_de_2_segundos():
    s = ServicioProbabilidad(LectorFalso(), LectorFalso(), GeneradorSintetico(semilla=1))
    datos = s.generar_datos(50_000)
    t0 = time.perf_counter()
    r = s.consultar(datos, "Estrato1", "Fibra")
    assert time.perf_counter() - t0 < 2 and not r.con_traza


def test_filtra_por_departamento_y_periodo():
    regs = [
        Registro("Corporativo", "WiFi", 10, "CAUCA", "2024-T1"),
        Registro("Corporativo", "FTTH", 30, "CAUCA", "2024-T1"),
        Registro("Corporativo", "FTTH", 500, "ANTIOQUIA", "2024-T1"),
        Registro("Corporativo", "FTTH", 700, "CAUCA", "2024-T2"),
    ]
    s = servicio()
    assert s.opciones_filtro(regs) == (["ANTIOQUIA", "CAUCA"], ["2024-T1", "2024-T2"])
    r = s.consultar(regs, "Corporativo", "FTTH", departamento="CAUCA", periodo="2024-T1")
    assert r.resultado.probabilidad == pytest.approx(0.75) and r.filtros == "CAUCA · 2024-T1"
    with pytest.raises(ErrorDeEntrada):
        s.consultar(regs, "Corporativo", "FTTH", departamento="CHOCÓ")
