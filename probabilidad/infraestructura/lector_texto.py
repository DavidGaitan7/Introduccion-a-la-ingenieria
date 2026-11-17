from probabilidad.dominio.modelos import Lectura, Registro
from probabilidad.dominio.normalizacion import normalizar


def a_numero(valor) -> float:
    n = float(str(valor).strip().replace(",", "."))
    if n < 0:
        raise ValueError("el acceso no puede ser negativo")
    return n


class LectorTextoPlano:
    """Lee líneas como: segmento=Estrato1, acceso=120, tecnologia=Fibra"""

    def leer(self, texto: str) -> Lectura:
        registros, errores = [], []
        for i, linea in enumerate(texto.splitlines(), start=1):
            if not linea.strip():
                continue
            datos = {}
            for par in linea.split(","):
                if "=" in par:
                    clave, valor = par.split("=", 1)
                    datos[normalizar(clave)] = valor.strip()
            try:
                registros.append(Registro(datos["segmento"], datos["tecnologia"], a_numero(datos["acceso"])))
            except (KeyError, ValueError):
                errores.append(
                    f"Línea {i}: usa el formato segmento=…, acceso=…, tecnologia=… con un acceso numérico."
                )
        return Lectura(registros, errores)
