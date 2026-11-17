import pytest

from probabilidad.dominio.algoritmo import calcular_probabilidad
from probabilidad.dominio.modelos import Consulta, Registro

CASO = [
    Registro("Estrato1", "Fibra", 120),
    Registro("Estrato1", "Cable", 300),
    Registro("Corporativo", "Fibra", 50),
    Registro("Estrato1", "XDSL", 80),
]


def test_caso_de_la_ficha_da_0_24():
    r = calcular_probabilidad(CASO, Consulta("Estrato1", "Fibra"))
    assert (r.acceso_segmento, r.acceso_ambos) == (500, 120)
    assert r.probabilidad == pytest.approx(0.24)


def test_ignora_mayusculas_y_tildes():
    regs = [Registro("Estrato1", "Inalámbrico", 10), Registro("Estrato1", "Fibra", 30)]
    assert calcular_probabilidad(regs, Consulta("estrato1", "INALAMBRICO")).probabilidad == pytest.approx(0.25)


def test_segmento_inexistente_da_cero():
    assert calcular_probabilidad(CASO, Consulta("Rural", "Fibra")).probabilidad == 0


def test_traza_va_de_la_linea_2_a_la_20():
    r = calcular_probabilidad(CASO, Consulta("Estrato1", "Fibra"), con_traza=True)
    assert r.pasos[0].linea == 2 and r.pasos[-1].linea == 20
