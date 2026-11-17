# Datos para el prototipo

## Archivo de prueba incluido
`datos_ejemplo/accesos_internet_fijo_muestra.csv`: 15 filas reales del conjunto
«Accesos de Internet Fijo desde 2024-1T» (Postdata / CRC). Sirve para comprobar que todo corre.

Consultas que puedes probar con ese archivo:
| Segmento | Tecnología | Resultado |
|---|---|---|
| Corporativo | Fiber to the home (FTTH) | 0,5 (9 de 18 accesos) |
| Residencial - Estrato 1 | Fiber to the home (FTTH) | ≈ 0,4493 (394 de 877) |

## Archivo completo
Página: https://www.postdata.gov.co/resource/accesos-de-internet-fijo-desde-2024-1t
Botón «Descargar» (CSV de unos 128 MB). Trae estas columnas, que el programa reconoce solas:
SEGMENTO, TECNOLOGIA y ACCESOS (obligatorias), más DEPARTAMENTO, ANNO y TRIMESTRE (para filtrar).
Las demás se ignoran.

En la página, abre «Pruebas de eficiencia y de carga», sube el CSV y elige Departamento (por ejemplo CAUCA)
y Período. Si no filtras, el programa suma todo el país y todos los trimestres.

Escribe el segmento y la tecnología tal como aparecen en el archivo, por ejemplo
`Residencial - Estrato 3` y `Hybrid Fiber Coaxial (HFC)`.
