# Arquitectura en capas

```
┌──────────────────────────────────────────┐
│ PRESENTACIÓN   probabilidad/presentacion │  Streamlit: formularios, tablas, mensajes
└───────────────────┬──────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│ APLICACIÓN     probabilidad/aplicacion   │  Casos de uso, validaciones, medición de tiempo
└───────────────────┬──────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│ DOMINIO        probabilidad/dominio      │  Registro, Consulta, Resultado y el algoritmo
└──────────────────────────────────────────┘
                    ▲
┌───────────────────┴──────────────────────┐
│ INFRAESTRUCTURA probabilidad/infraestructura │ Lee texto y CSV (pandas), genera datos
└──────────────────────────────────────────┘
```

`app.py` es la raíz de composición: crea los objetos de infraestructura y se los entrega al servicio.

## Qué hace cada capa
| Capa | Responsabilidad | Archivos |
|---|---|---|
| Presentación | Mostrar la interfaz y recoger lo que escribe el usuario. No calcula nada. | `interfaz.py` |
| Aplicación | Orquestar un caso de uso: validar, leer, calcular y medir el tiempo. | `servicios.py`, `puertos.py` |
| Dominio | Las reglas del problema. Aquí vive el pseudocódigo de la Ficha 4. | `algoritmo.py`, `modelos.py`, `normalizacion.py` |
| Infraestructura | Todo lo que toca el exterior: archivos, pandas, datos al azar. | `lector_texto.py`, `lector_csv.py`, `generador.py` |

## Regla de dependencias
- La presentación solo conoce la aplicación.
- La aplicación solo conoce el dominio y los contratos (`puertos.py`).
- El dominio no importa nada de las otras capas, ni `streamlit` ni `pandas`.
- La infraestructura cumple los contratos y usa el dominio.

`tests/test_arquitectura.py` revisa esta regla automáticamente: si alguien rompe una capa, la prueba falla.

## Por qué esta arquitectura (para la diapositiva 12 y la sustentación)
1. Se puede cambiar Streamlit por otra interfaz sin tocar el algoritmo.
2. Se puede cambiar de CSV a una base de datos solo en infraestructura.
3. El algoritmo se prueba sin interfaz ni archivos, como se hizo a mano en la Ficha 4.

## Dónde está cada línea del pseudocódigo
`probabilidad/dominio/algoritmo.py`: decisión (SI) en las líneas 8, 10 y 15 del pseudocódigo; repetición (PARA CADA) en la línea 7.
