# Organización del proyecto con Scrum (Ficha 2)

**Modelo elegido:** Ágil · Scrum
**Producto:** calculadora de P(tecnología | segmento) sobre datos de acceso a internet.

## Por qué Scrum para este problema
1. [Completa con tu razón: p. ej., los requisitos se fueron afinando al leer los datos de datos.gov.co, así que conviene entregar versiones pequeñas y ajustarlas.]
2. [Segunda razón: p. ej., el curso entrega fichas por cortes y cada sprint puede cerrar una ficha.]

## Roles (se corresponden con A · D · P · C de la diapositiva 7)
| Rol Scrum | Rol en la plantilla | Integrante |
|---|---|---|
| Product Owner | Analista (A) | [nombre] |
| Scrum Master | Diseñador (D) | [nombre] |
| Developer | Programador (P) | [nombre] |
| Developer / QA | Calidad (C) | [nombre] |

El docente actúa como cliente que valida cada incremento.

## Product Backlog
| ID | Historia de usuario | Prioridad | Puntos | Sprint |
|---|---|---|---|---|
| H1 | Como analista, quiero escribir registros de acceso para tener datos con los que consultar. | Alta | 3 | 1 |
| H2 | Como analista, quiero elegir un segmento y una tecnología para consultar una probabilidad concreta. | Alta | 2 | 1 |
| H3 | Como analista, quiero ver P(tecnología \| segmento) calculada según el pseudocódigo de la Ficha 4. | Alta | 5 | 1 |
| H4 | Como usuario, quiero ver la prueba de escritorio paso a paso para entender cómo se obtuvo el resultado. | Media | 3 | 2 |
| H5 | Como analista, quiero cargar un CSV de datos.gov.co para trabajar con datos reales. | Alta | 5 | 2 |
| H6 | Como usuario, quiero mensajes claros cuando un dato está mal escrito o el segmento no existe. | Media | 2 | 2 |
| H7 | Como calidad, quiero medir el tiempo de cálculo con muchos registros para comprobar la eficiencia. | Media | 3 | 3 |
| H8 | Como calidad, quiero que 4 de 5 compañeros calculen una probabilidad sin ayuda para comprobar la usabilidad. | Media | 3 | 3 |
| H9 | Como equipo, queremos documentar y preparar la demostración en vivo. | Alta | 3 | 3 |

## Sprints
**Sprint 1 — Núcleo funcional (H1, H2, H3).**
Meta: el programa calcula 0,24 con el caso de la ficha.
Entregable: capa de dominio (`algoritmo.py`, `modelos.py`) y una interfaz básica.

**Sprint 2 — Datos reales y confianza (H4, H5, H6).**
Meta: el sistema lee un CSV real y muestra la prueba de escritorio.
Entregable: capa de infraestructura (`lector_csv.py`), tabla de pasos y pruebas con `pytest`.

**Sprint 3 — Calidad y sustentación (H7, H8, H9).**
Meta: los tres criterios de la Ficha 3 están medidos con resultado.
Entregable: capa de aplicación con medición de tiempo, tabla de resultados de la diapositiva 8 y demo ensayada.

## Eventos de Scrum (versión corta para el curso)
- **Planificación del sprint:** 20 min. Se eligen historias y se reparten tareas.
- **Reunión diaria:** 5 min por chat. Qué hice, qué haré, qué me bloquea.
- **Revisión del sprint:** se muestra el incremento funcionando y se pide opinión.
- **Retrospectiva:** qué mantener, qué mejorar, un compromiso concreto.

## Definición de terminado (DoD)
- El código corre sin errores con `streamlit run app.py`.
- `tests/test_arquitectura.py` pasa: ninguna capa rompe la regla de dependencias (ver `ARQUITECTURA.md`).
- `pytest` pasa completo.
- El caso de la ficha sigue dando 0,24.
- Otro integrante revisó el cambio.
- La historia se probó con un caso real.

## Criterios de calidad (Ficha 3) y cómo se miden en el prototipo
| Atributo | Criterio | Cómo se prueba |
|---|---|---|
| Adecuación funcional | Coincide con el cálculo a mano en 50 registros reales | `test_caso_de_la_ficha_da_0_24` y comparación manual |
| Eficiencia de desempeño | [N] registros en menos de [X] s | `test_eficiencia_…` (en `tests/test_aplicacion.py`) y el tiempo que muestra la app |
| Usabilidad | 4 de 5 compañeros calculan sin ayuda | Prueba con 5 compañeros y conteo de aciertos |

## Cómo ejecutarlo
```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # pruebas
streamlit run app.py             # abre la interfaz en el navegador
```
