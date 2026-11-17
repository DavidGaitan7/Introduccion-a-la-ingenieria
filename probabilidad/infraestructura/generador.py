import random

from probabilidad.dominio.modelos import Registro

SEGMENTOS = ["Estrato1", "Estrato2", "Estrato3", "Corporativo", "Rural"]
TECNOLOGIAS = ["Fibra", "Cable", "XDSL", "Satelital", "Inalambrico"]


class GeneradorSintetico:
    """Crea datos al azar para medir la eficiencia."""

    def __init__(self, semilla: int | None = None):
        self._azar = random.Random(semilla)

    def generar(self, cantidad: int) -> list[Registro]:
        a = self._azar
        return [
            Registro(a.choice(SEGMENTOS), a.choice(TECNOLOGIAS), a.randint(1, 500))
            for _ in range(cantidad)
        ]
