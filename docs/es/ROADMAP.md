# Hoja de ruta

[English](../../ROADMAP.md) · [Inicio en español](../../README.es.md)

Cada fase pasa por planificación, autorización explícita, implementación, validación y cierre. La autorización de una fase permite ejecutar su alcance. El cierre se registra con evidencia en [validación](VALIDATION.md) y [estado actual](CURRENT_STATE.md).

| Fase | Entregable y condición de salida | Estado registrado |
| --- | --- | --- |
| 0 · Viabilidad | Probar acceso acotado, dos fechas para las mismas tiendas, interpretación de precios y al menos 100 coincidencias coherentes por descripción. | Cerrada el 19 de noviembre de 2026. Cuatro archivos y 102 de 160 pares revisados. |
| 1 · Scrapy | Adaptadores específicos, descarga acotada, trazabilidad, pruebas de error y CI de comprobación. | Cerrada el 22 de noviembre. |
| 2 · Ingeniería de datos | Conservar procedencia, validar el esquema y repetir la carga de archivos históricos. | Cerrada el 23 de noviembre. Se revisó un archivo real por cadena y cuatro comparaciones. |
| 3 · Fiabilidad | Demostrar programación, registro, detección de fallos y recuperación con ejecuciones medidas. | Autorizada antes del cierre de la fase 2. Sigue abierta para la revisión del responsable. |
| 4 · Tableau | Validar métricas contra SQL y comprobar el libro privado en Desktop. | Cerrada el 23 de noviembre para el libro privado. |
| 5 · Validación y publicación | Comprobar el flujo, la instalación reproducible y el portafolio público. | Autorizada el 23 y cerrada el 25 de noviembre. |

## Validación del lanzamiento

- [PULSE-24](https://angel231995.atlassian.net/browse/PULSE-24) documenta la captura o línea base archivada, la repetición de versiones exactas y la conciliación de SQL con Tableau.
- [PULSE-25](https://angel231995.atlassian.net/browse/PULSE-25) cubre la instalación con dependencias fijadas y la base desechable de PostgreSQL.
- [PULSE-26](https://angel231995.atlassian.net/browse/PULSE-26) cubre el libro empaquetado, las capturas de presentación y la descarga.
- [PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) registra la incorporación de Konzum 1280. El 24 de noviembre se confirmó que Lidl quedaba fuera de la entrega y se eligió un único portafolio con datos reales.

## Trabajo pendiente

La fase 3 conserva su propia condición de cierre. La tarea local programada solo hace capturas. [PULSE-45](https://angel231995.atlassian.net/browse/PULSE-45) cubre PostgreSQL con Docker Compose para desarrollo persistente y pruebas desechables. La revisión privada de más pares puede ampliar la cobertura verificada conservando los casos ambiguos como pendientes. Consulta [fiabilidad](RELIABILITY.md) para el procedimiento de recuperación.
