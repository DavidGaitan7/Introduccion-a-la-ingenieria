"""Lector de CSV pensado para los archivos de datos abiertos (datos.gov.co / postdata.gov.co).

Reconoce los nombres de columna habituales (SEGMENTO, TECNOLOGIA, ACCESOS, DEPARTAMENTO,
ANNO, TRIMESTRE) sin importar mayúsculas ni tildes, ignora las demás columnas y lee solo
las que necesita, para que archivos de más de 100 MB carguen rápido.
"""
import io
import re

import pandas as pd

from probabilidad.dominio.modelos import Lectura, Registro
from probabilidad.dominio.normalizacion import normalizar

ALIAS = {
    "segmento": {"segmento"},
    "tecnologia": {"tecnologia"},
    "acceso": {"acceso", "accesos", "cantidad", "cantidad accesos", "no accesos", "numero accesos", "numero de accesos"},
    "departamento": {"departamento"},
    "anno": {"anno", "ano"},
    "trimestre": {"trimestre"},
}
OBLIGATORIAS = ("segmento", "tecnologia", "acceso")


def _clave(nombre: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", normalizar(nombre)).strip()


class LectorCSVPandas:
    def leer(self, contenido: bytes | str) -> Lectura:
        if isinstance(contenido, str):
            contenido = contenido.encode("utf-8")
        contenido = contenido.lstrip(b"\xef\xbb\xbf")
        encoding = "utf-8"
        try:
            contenido[:200_000].decode("utf-8")
        except UnicodeDecodeError:
            encoding = "latin-1"

        primera = contenido[:20_000].split(b"\n", 1)[0].decode(encoding, errors="ignore")
        sep = ";" if primera.count(";") > primera.count(",") else ","

        try:
            encabezado = pd.read_csv(io.BytesIO(contenido), sep=sep, nrows=0, encoding=encoding).columns
        except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
            raise ValueError("No se pudo leer el archivo como CSV.") from e

        elegidas: dict[str, str] = {}
        for col in encabezado:
            for campo, nombres in ALIAS.items():
                if campo not in elegidas and _clave(col) in nombres:
                    elegidas[campo] = col
        faltan = [c for c in OBLIGATORIAS if c not in elegidas]
        if faltan:
            raise ValueError(
                "Al CSV le faltan las columnas: " + ", ".join(faltan)
                + ". Columnas encontradas: " + ", ".join(map(str, encabezado))
            )

        df = pd.read_csv(
            io.BytesIO(contenido), sep=sep, usecols=list(elegidas.values()),
            dtype=str, encoding=encoding, keep_default_na=False,
        )
        df = df.rename(columns={v: k for k, v in elegidas.items()})

        acceso = pd.to_numeric(df["acceso"].str.replace(",", ".", regex=False), errors="coerce")
        validas = acceso.notna() & (acceso >= 0)
        n_malas = int((~validas).sum())
        df, acceso = df[validas], acceso[validas]

        segmentos = df["segmento"].str.strip().tolist()
        tecnologias = df["tecnologia"].str.strip().tolist()
        accesos = acceso.tolist()
        deps = df["departamento"].str.strip().tolist() if "departamento" in df else [""] * len(df)
        if "anno" in df and "trimestre" in df:
            periodos = (df["anno"].str.strip() + "-T" + df["trimestre"].str.strip()).tolist()
        else:
            periodos = [""] * len(df)

        registros = [
            Registro(s, t, a, d, p)
            for s, t, a, d, p in zip(segmentos, tecnologias, accesos, deps, periodos)
        ]
        errores = [f"{n_malas} filas con un número de accesos no válido se ignoraron."] if n_malas else []
        return Lectura(registros, errores)
