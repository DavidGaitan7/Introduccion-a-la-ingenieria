"""Capa de presentación (Streamlit). Solo habla con el servicio de aplicación."""
import pandas as pd
import streamlit as st

from probabilidad.aplicacion.servicios import ErrorDeEntrada, Respuesta, ServicioProbabilidad

EJEMPLO = """segmento=Estrato1, acceso=120, tecnologia=Fibra
segmento=Estrato1, acceso=300, tecnologia=Cable
segmento=Corporativo, acceso=50, tecnologia=Fibra
segmento=Estrato1, acceso=80, tecnologia=XDSL"""


def _coma(x: float, dec: int = 4) -> str:
    return f"{x:.{dec}f}".replace(".", ",")


def _mostrar_respuesta(r: Respuesta) -> None:
    res = r.resultado
    st.metric(f"P({r.consulta.tecnologia} | {r.consulta.segmento})", _coma(res.probabilidad))
    st.progress(min(res.probabilidad, 1.0), text=f"{_coma(res.probabilidad * 100, 2)} % de los accesos del segmento")
    st.code(
        f"P = accesoAmbos / accesoSegmento = {res.acceso_ambos:g} / {res.acceso_segmento:g} = {_coma(res.probabilidad)}",
        language=None,
    )
    if r.filtros:
        st.caption(f"Filtro aplicado: {r.filtros}")
    c1, c2 = st.columns(2)
    c1.metric("Registros leídos", f"{r.total_registros:,}")
    c2.metric("Tiempo de cálculo", f"{r.milisegundos:.2f} ms")
    if r.segmento_sin_datos:
        st.warning(f"Ningún registro pertenece al segmento «{r.consulta.segmento}». Revisa cómo está escrito.")
    if r.con_traza:
        st.markdown("**Prueba de escritorio paso a paso**")
        filas = [
            {
                "Paso": i,
                "Línea": p.linea,
                "Instrucción": p.instruccion + (f"  ({p.detalle})" if p.detalle else ""),
                "¿Se cumple?": "—" if p.se_cumple is None else ("Sí" if p.se_cumple else "No"),
                "accesoSegmento": p.acceso_segmento,
                "accesoAmbos": p.acceso_ambos,
            }
            for i, p in enumerate(res.pasos, start=1)
        ]
        st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    else:
        st.caption("Con más de 30 registros no se muestra la prueba de escritorio.")


def mostrar(servicio: ServicioProbabilidad) -> None:
    st.set_page_config(page_title="Probabilidad por segmento", page_icon="📊", layout="wide")
    st.title("¿Qué tan probable es una tecnología de acceso dentro de un segmento?")
    st.caption("Calcula P(tecnología | segmento) = accesos de la tecnología en el segmento ÷ accesos totales del segmento.")

    if "grandes" not in st.session_state:
        st.session_state.grandes = None
        st.session_state.origen = ""
        st.session_state.opciones = ([], [])
    departamento = periodo = None

    izq, der = st.columns(2, gap="large")

    with izq:
        st.subheader("1. Datos y consulta")
        texto = st.text_area(
            "Registros (uno por línea)", value=EJEMPLO, height=190,
            help="Formato: segmento=Estrato1, acceso=120, tecnologia=Fibra",
            disabled=st.session_state.grandes is not None,
        )
        c1, c2 = st.columns(2)
        segmento = c1.text_input("Segmento", "Estrato1")
        tecnologia = c2.text_input("Tecnología", "Fibra")

        with st.expander("Pruebas de eficiencia y de carga"):
            archivo = st.file_uploader("Cargar un CSV (segmento, tecnologia, acceso)", type=["csv", "txt"])
            if archivo is not None and st.session_state.origen != archivo.name:
                try:
                    registros, errores = servicio.cargar_csv(archivo.getvalue())
                    st.session_state.grandes, st.session_state.origen = registros, archivo.name
                    st.session_state.opciones = servicio.opciones_filtro(registros)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
            n = st.number_input("Registros sintéticos", 100, 2_000_000, 50_000, step=1000)
            if st.button("Generar datos de prueba"):
                try:
                    st.session_state.grandes = servicio.generar_datos(int(n))
                    st.session_state.origen = f"{int(n):,} registros generados"
                    st.session_state.opciones = ([], [])
                    st.rerun()
                except ErrorDeEntrada as e:
                    st.error(str(e))
            if st.session_state.grandes is not None:
                st.info(f"Usando: {st.session_state.origen} ({len(st.session_state.grandes):,} registros)")
                deps, pers = st.session_state.opciones
                if deps or pers:
                    st.caption("El archivo trae varios departamentos y períodos. Elige uno para no sumarlos todos.")
                    departamento = st.selectbox("Departamento", ["(todos)"] + deps) if deps else None
                    periodo = st.selectbox("Período", ["(todos)"] + pers) if pers else None
                    departamento = None if departamento == "(todos)" else departamento
                    periodo = None if periodo == "(todos)" else periodo
                if st.button("Volver a escribir a mano"):
                    st.session_state.grandes, st.session_state.origen = None, ""
                    st.session_state.opciones = ([], [])
                    st.rerun()

        calcular = st.button("Calcular probabilidad", type="primary")

    with der:
        st.subheader("2. Resultado")
        if not calcular:
            st.info("Pulsa «Calcular probabilidad» para ver el resultado.")
            return
        try:
            if st.session_state.grandes is not None:
                r = servicio.consultar(
                    st.session_state.grandes, segmento, tecnologia,
                    departamento=departamento, periodo=periodo,
                )
            else:
                r = servicio.consultar_texto(texto, segmento, tecnologia)
        except ErrorDeEntrada as e:
            st.error(str(e))
            return
        if r.errores_lectura:
            st.warning("Se ignoraron líneas con problemas:\n\n" + "\n".join(f"- {e}" for e in r.errores_lectura[:5]))
        _mostrar_respuesta(r)
