import pytest

from probabilidad.infraestructura.generador import GeneradorSintetico
from probabilidad.infraestructura.lector_csv import LectorCSVPandas
from probabilidad.infraestructura.lector_texto import LectorTextoPlano


def test_lector_texto_valido():
    lec = LectorTextoPlano().leer("segmento=Estrato1, acceso=120, tecnologia=Fibra")
    assert lec.errores == [] and lec.registros[0].acceso == 120


def test_lector_texto_reporta_linea_con_error():
    lec = LectorTextoPlano().leer("segmento=B, acceso=abc, tecnologia=X")
    assert lec.registros == [] and len(lec.errores) == 1


def test_lector_csv_con_punto_y_coma():
    lec = LectorCSVPandas().leer("segmento;tecnologia;acceso\nEstrato1;Fibra;120\nEstrato1;Cable;380\n")
    assert lec.errores == [] and len(lec.registros) == 2


def test_lector_csv_sin_columnas_falla():
    with pytest.raises(ValueError):
        LectorCSVPandas().leer("a,b\n1,2\n")


def test_generador_cantidad():
    assert len(GeneradorSintetico(semilla=1).generar(250)) == 250


# ---- Formato real de datos abiertos (postdata.gov.co / datos.gov.co) ----
import pathlib
import time

MUESTRA = pathlib.Path(__file__).resolve().parent.parent / "datos_ejemplo" / "accesos_internet_fijo_muestra.csv"


def test_lee_el_formato_real_con_columna_accesos_y_tildes():
    lec = LectorCSVPandas().leer(MUESTRA.read_bytes())
    assert lec.errores == [] and len(lec.registros) == 15
    primero = lec.registros[0]
    assert (primero.departamento, primero.periodo, primero.acceso) == ("CAUCA", "2024-T1", 3)


def test_muestra_real_corporativo_ftth_da_0_5():
    from probabilidad.dominio.algoritmo import calcular_probabilidad
    from probabilidad.dominio.modelos import Consulta
    regs = LectorCSVPandas().leer(MUESTRA.read_bytes()).registros
    r = calcular_probabilidad(regs, Consulta("Corporativo", "Fiber to the home (FTTH)"))
    assert (r.acceso_ambos, r.acceso_segmento) == (9, 18)
    assert r.probabilidad == 0.5


def test_csv_en_latin1_tambien_se_lee():
    contenido = "SEGMENTO,TECNOLOGIA,ACCESOS\nCorporativo,Cable,5\n".encode("latin-1")
    assert LectorCSVPandas().leer(contenido).registros[0].acceso == 5


def test_csv_grande_carga_rapido():
    filas = ["ANNO,TRIMESTRE,DEPARTAMENTO,SEGMENTO,TECNOLOGIA,ACCESOS"]
    filas += [f"2024,{1 + i % 4},CAUCA,Residencial - Estrato {1 + i % 6},WiFi,{i % 50}" for i in range(300_000)]
    t0 = time.perf_counter()
    lec = LectorCSVPandas().leer("\n".join(filas))
    assert len(lec.registros) == 300_000 and time.perf_counter() - t0 < 15
