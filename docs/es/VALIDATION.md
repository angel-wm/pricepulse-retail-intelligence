# Validación y evidencia

[English](../../VALIDATION.md) · [Inicio en español](../../README.es.md)

Esta página resume en español los resultados registrados. Los enlaces llevan a las entradas originales en inglés con comandos, recuentos, referencias y límites de cada prueba.

## Viabilidad, adquisición e historial

| Hito | Resultado observado | Registro original |
| --- | --- | --- |
| Viabilidad inicial | Se recuperaron cuatro listas oficiales para dos tiendas y dos fechas. El análisis con precios promocionales halló 8.869 códigos compartidos con precio. En la auditoría de 160 candidatos, 102 descripciones fueron coherentes y 58 quedaron pendientes. | [Auditoría de fase 0](../../VALIDATION.md#final-phase-0-price-and-product-description-audit--2026-11-18) |
| Adaptadores Scrapy | Una prueba acotada por cadena obtuvo archivos reales del 17 de noviembre. También se comprobaron contratos, límites de reintento y manejo de errores con pruebas sintéticas. | [PULSE-12](../../VALIDATION.md#phase-1-pulse-12--2026-11-19) · [PULSE-13](../../VALIDATION.md#phase-1-pulse-13--2026-11-22) |
| PostgreSQL privado | Se cargó y reprodujo un archivo real de cada cadena original. Se conciliaron las filas, se revisaron cuatro de 6.418 pares elegibles y se comprobaron sus precios contra SQL. | [Revisión de fase 2](../../VALIDATION.md#phase-2-private-real-file-review--2026-11-23) |
| Revisión técnica | La versión examinada pasó 62 pruebas locales y las comprobaciones alojadas. La fase 5 verificó además una instalación limpia y PostgreSQL desechable. | [Revisión de fase 5](../../VALIDATION.md#phase-5-technical-review--2026-11-23) · [Configuración reproducible](../../VALIDATION.md#phase-5-reproducible-setup--2026-11-23) |

## Captura operativa

- La revisión del 23 de noviembre registra un cambio en los nombres de archivo de Kaufland, recuperación manual y comprobaciones temporizadas en Windows. [Revisión de fase 3](../../VALIDATION.md#phase-3-owner-review-evidence--2026-11-23)
- El 24 de noviembre la tarea instalada obtuvo las tres listas, terminó con código 0 y no registró alertas. La evidencia no permite confirmar el disparador original. [Captura instalada](../../VALIDATION.md#installed-windows-collection-with-three-retailers--2026-11-24)
- El 25 de noviembre, el disparador regular de las 12:20 de Bogotá inició la tarea. Kaufland y Konzum aportaron 23.830 y 26.590 precios utilizables. SPAR se detuvo en la comprobación de encabezados y el lote quedó `incomplete`, código 1. El reintento independiente con el analizador actualizado recuperó 32.329 precios de SPAR, 26.565 regulares y 5.764 promocionales. La repetición de los archivos anteriores de SPAR conservó sus recuentos. Pasaron 58 pruebas locales y se omitieron 11 de integración por falta de una base de pruebas configurada. [Disparo regular y recuperación de SPAR](../../VALIDATION.md#regular-windows-tick-and-spar-schema-recovery--2026-11-25)

- El 26 y 27 de noviembre, los lotes de captura quedaron incompletos. SPAR y Kaufland completaron ambos intentos y Konzum registró cero archivos coincidentes para la tienda y fecha seleccionadas. El responsable descartó la prueba prevista de las 06:20 de Bogotá. [Registro original](../../VALIDATION.md#three-store-collection-review--2026-11-27)

## Tableau y cierre de la entrega

- **Fase 4.** El libro privado original de dos tiendas se concilió con PostgreSQL. Se verificó la interacción en Desktop. El cierre del 23 de noviembre cubre ese libro privado. [Revisión privada](../../VALIDATION.md#phase-4-private-real-tableau-review--2026-11-23)
- **Tercera fuente.** Se validó la expansión a Konzum y el libro de 165.322 precios de seis archivos, con 41.363 comparaciones en una misma tienda. La vista de códigos incluye 13.700 coincidencias consultables para el 23 de noviembre y cuatro productos con revisión manual. [Expansión](../../VALIDATION.md#konzum-expansion-validation--2026-11-23) · [Validación de tres fuentes](../../VALIDATION.md#three-source-tableau-validation--2026-11-23) · [Explorador](../../VALIDATION.md#tableau-barcode-explorer--2026-11-24)
- **Fase 5.** El cierre aprobado el 25 de noviembre cubre la conciliación de extremo a extremo con la cohorte original, la instalación reproducible y el libro público con extractos incluidos. Se verificaron la apertura y el ajuste del panel en el tamaño de presentación probado. [Presentación](../../VALIDATION.md#tableau-portfolio-presentation--2026-11-25) · [Cierre de fase 5](../../VALIDATION.md#phase-5-closeout--2026-11-25)

## Recuperación y validación pendiente

La corrección del 27 de noviembre aplica la política de archivo no disponible solo al HTTP 403 de robots.txt en el CDN oficial durante una captura de Konzum. El CSV respondió HTTP 200. El lote manual terminó en 35,38 segundos con 32.405 precios de SPAR, 23.823 de Kaufland y 26.641 de Konzum. Se comprobaron los tres SHA-256 y pasaron 76 pruebas con PostgreSQL desechable. Queda pendiente verificar la captura automática regular con la corrección. [Evidencia de la corrección](../../VALIDATION.md#konzum-cdn-capture-recovery--2026-11-27)

La revisión posterior confirmó que el CDN era la única ruta enlazada para la tienda 1280 en las listas del 25 al 27 de noviembre. Se reprodujeron las tres capturas del 24 de noviembre en PostgreSQL desechable. Al repetir la carga, se conservaron las tres versiones, las 82.888 filas de origen y las 82.880 observaciones de precio sin duplicados. La cola produjo 6.439 pares SPAR–Kaufland, 6.890 SPAR–Konzum y 7.485 Kaufland–Konzum. Todos quedaron pendientes de revisión en la base temporal. [Detalle de la reproducción](../../VALIDATION.md#archived-three-store-replay)

En cuatro lotes registrados del 24 al 27 de noviembre hubo un éxito completo y tres lotes incompletos. Los éxitos por fuente fueron SPAR 3/4, Kaufland 4/4 y Konzum 2/4. Se comprobaron las huellas SHA-256 de los nueve archivos exitosos. Se verificó con una tarea temporal de Windows que una detención conserva el marcador y que archivar ese marcador permite reintentar con datos sintéticos. La suite local pasó 70 pruebas con PostgreSQL desechable.

Antes de la corrección, el colector se detenía al recibir HTTP 403 de robots.txt en el CDN de Konzum. Queda pendiente observar una captura automática completa y medir una línea base estable de tres tiendas. El cierre requiere revisión del responsable. [Revisión operativa en inglés](../../VALIDATION.md#phase-3-operational-review--2026-11-27) Consulta [estado actual](CURRENT_STATE.md) y [fiabilidad](RELIABILITY.md).
