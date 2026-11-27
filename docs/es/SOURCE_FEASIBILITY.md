# Viabilidad de las fuentes

[English](../../SOURCE_FEASIBILITY.md) · [Inicio en español](../../README.es.md)

La fase 0 cerró el 19 de noviembre de 2026 tras pruebas acotadas con SPAR Zagreb Jankomir 8702 y Kaufland Zagreb Antuna Šoljana 5630. La evaluación pasó de páginas de instrumentos musicales a listas oficiales croatas de supermercados y artículos del hogar. Las fuentes ofrecen archivos por tienda y fecha con una identidad útil para análisis histórico.

## Base normativa documentada

La regulación croata NN 132/2026-1584 se publicó el 16 de noviembre de 2026 y entró en vigor al día siguiente. La revisión de ingeniería registró que contempla el acceso automatizado, formatos CSV o XML y un conjunto de atributos de producto y precio que no exige existencias. Permite listas por tienda, exige publicar los cambios antes de las 11:00 y mantener los archivos reemplazados durante 15 días. La ubicación de una lista se puede reutilizar, por lo que se conservan hashes y fechas para distinguir versiones. En los archivos observados hubo diferencias de codificación y delimitador. [Texto oficial de la regulación](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html)

La evaluación de fuentes distingue el acceso automatizado y los derechos de redistribución. Los flujos locales conservan de forma privada archivos originales y artefactos de procesamiento. La decisión posterior de publicar el libro seleccionado se registra en [D-019](DECISIONS.md#registro-de-decisiones). Para el alcance del análisis de las condiciones de SPAR, consulta el [registro original](../../SOURCE_FEASIBILITY.md#regulatory-baseline-effective-2026-11-17).

## Evidencia de acceso y precios

- En noviembre de 2026, pruebas locales acotadas con Scrapy obtuvieron HTTP 200 en índices y archivos de SPAR y Kaufland. El JSON diario de SPAR y el índice de recursos de Kaufland se tratan como interfaces sujetas a cambios.
- Se obtuvieron listas para las mismas dos tiendas el 16 y 17 de noviembre. SPAR usó CP1250 con punto y coma y Kaufland UTF-8 con BOM y tabulador.
- El primer análisis usó el campo regular y encontró 8.263 coincidencias con precio. La lectura de precios especiales recuperó 3.103 filas de SPAR del 17 de noviembre que tenían vacío ese campo.
- El análisis final encontró 8.869 códigos con precio compartidos el mismo día, 7.772 presentes en los cuatro archivos y 4.155 candidatos estrictos. De 160 pares revisados, 102 mostraron descripciones coherentes y 58 quedaron sin resolver. La muestra documenta coherencia de descripción, marca y presentación. Carece de certificación de fabricante y no estima la precisión del catálogo.
- Kaufland mostró un aumento del 47,9 % en filas en la transición normativa. Un cambio de cobertura debe investigarse antes de atribuirlo a variaciones de surtido.
- Un estudio independiente de mayo de 2025 encontró 583 códigos compartidos entre siete cadenas y 4.126 entre las seis sin Lidl. Es evidencia histórica externa, con fecha y metodología distintas de las pruebas directas. [Estudio de mayo de 2025](https://analiza.usporedicijene.info/)

## Selección de la tercera fuente

Se comparó Konzum 1280 con Lidl 158 para las mismas dos fechas de noviembre y contra las tiendas seleccionadas de SPAR y Kaufland. Se excluyeron códigos inválidos y precios ambiguos. Para ordenar precios también se excluyeron casos con múltiples observaciones en cualquiera de las tiendas participantes.

| Medida | 17 de noviembre | 23 de noviembre |
| --- | ---: | ---: |
| Códigos con precio compartidos entre SPAR y Kaufland | 8.869 | 8.854 |
| También en Konzum | 5.968 | 5.961 |
| También en Lidl | 870 | 877 |
| Presentes en las cuatro tiendas | 771 | 777 |
| Precio de Konzum inferior al de ambas tiendas base | 818 | 672 |
| Precio de Lidl inferior al de ambas tiendas base | 215 | 218 |
| Precio de Lidl inferior al de las otras tres tiendas | 168 | 168 |
| Códigos de Lidl compartidos con alguna tienda base y ausentes de Konzum | 234 | 243 |

Entre fechas persistieron 5.900 códigos de la cohorte de tres tiendas con Konzum y 836 con Lidl. En una revisión puntual privada de 12 candidatos con menor precio por cadena se observaron detalles de presentación ausentes y un posible conflicto de variante en Lidl. Las cifras son resultados de selección previa a verificar variantes y elegibilidad de promociones.

El CSV de Konzum mantuvo encabezados y separador de coma. Lidl cambió encabezados, campos de código y separador y presentó 1.934 y 1.706 filas con solo precio especial, respectivamente. El 23 de noviembre se autorizó Konzum como tercera fuente. El 24 se confirmó que Lidl quedaba fuera de la entrega. [PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) · [Tablas completas de la evaluación](../../SOURCE_FEASIBILITY.md#expansion-feasibility--2026-11-23)
