# Análisis en Tableau

[English](../../TABLEAU.md) · [Inicio en español](../../README.es.md)

## Libro del portafolio

[Descarga el archivo empaquetado](../../portfolio/tableau/PricePulse-Three-Store-Price-Comparison.twbx?raw=true) y ábrelo en Tableau Desktop Public Edition 2026.3 o posterior. Incluye siete extractos Hyper. Pulsa **F7** para ver el diseño de 1840 × 920 en modo presentación. [Panel](../../portfolio/tableau/dashboard.png) · [Búsqueda en modo presentación](../../portfolio/tableau/search-presentation.jpg)

El libro está en inglés. La vista inicial compara 13.700 códigos de barras del 23 de noviembre de 2026. De ellos, 5.961 aparecen en tres tiendas y 7.739 en dos. Escribe parte del nombre o un código en **Search** y pulsa Enter. Borra el campo y pulsa Enter para restaurar todos los resultados. Un guion indica que la lista seleccionada de la tienda carece de una observación comparable con precio.

- **Barcode match** indica un código normalizado compartido y una fila con precio por tienda participante.
- **Verified** identifica los cuatro productos que también pasaron revisión manual de producto, variante y tamaño. Sus gráficos aparecen a la derecha. El libro local conserva los 12 pares revisados y cuatro decisiones históricas SPAR–Kaufland.
- **Price catalog** muestra 165.322 precios de los días 17 y 23 de noviembre, incluso productos de una sola tienda. Filtra por tienda, fecha y producto. **Price type** indica origen regular, especial o ambos importes iguales.
- **Catalog coverage** muestra los seis recuentos por fecha y tienda. **Product price history** incluye 41.363 comparaciones en la misma tienda, con precios que subieron, bajaron o se mantuvieron.

Los archivos proceden de SPAR Zagreb Jankomir 8702, Kaufland Zagreb Antuna Šoljana 5630 y Konzum Zagreb Velimira Škorpika 1280. La revisión de productos entre las tres tiendas usa las listas del 23 de noviembre. [SPAR](https://www.spar.hr/usluge/cjenici) · [Kaufland](https://www.kaufland.hr/akcije-novosti/popis-mpc.html) · [Konzum](https://www.konzum.hr/cjenici)

## Definiciones de las métricas

| Métrica | Cálculo |
| --- | --- |
| Precio publicado | Importe resuelto en EUR por SKU, tienda y fecha. Se incluyen importes válidos únicos o dos importes iguales. |
| Cambio en la misma tienda | Precio actual menos el de la observación seleccionada anterior del SKU, con GTIN válido y descriptores estables. |
| Brecha de precio | Precio mayor menos precio menor entre las tiendas mostradas para el código y la fecha. |
| Diferencia por par | Precio izquierdo menos derecho para las dos filas exactas en el orden de revisión. Un valor positivo indica menor precio a la derecha. |
| Variación relativa | Diferencia dividida por el precio anterior o por el precio de la derecha, según el cálculo, multiplicada por 100. Omite denominadores ausentes o cero. El libro privado muestra diferencias absolutas en EUR. |
| Calidad del archivo | Filas con precio o GTIN válido sobre filas totales. Edad igual a fecha de referencia menos fecha de la lista. |

**Search** filtra la tabla de códigos. Las cifras de resumen describen el conjunto completo del 23 de noviembre. Seleccionar un producto en el gráfico de precios verificados filtra su gráfico de brecha.

## Exportación analítica privada

Con una [base privada inicializada y poblada](POSTGRESQL.md), selecciona como máximo una versión por cadena, tienda y fecha. Configura `PRICEPULSE_DSN` de forma privada. Ejemplo con identificadores ilustrativos:

```powershell
uv run --locked python -m pricepulse.analytics --file-id 1 --file-id 2 --directory data/tableau-private --as-of 2026-11-23
```

Las selecciones inválidas, duplicadas o incompatibles fallan antes de escribir. Los cuatro CSV son entradas locales.

| Archivo | Granularidad |
| --- | --- |
| `observations.csv` | Una fila con precio por archivo seleccionado. Puede contener excepciones de revisión. |
| `changes.csv` | Observaciones consecutivas dentro de la selección, con SKU y descriptores estables y sin excepciones. Las fechas pueden estar separadas por varios días. |
| `comparisons.csv` | Pares aprobados sin excepciones entre tiendas, con archivos seleccionados y misma fecha. `price_difference` sigue el orden de revisión. |
| `quality.csv` | Una fila por archivo. Proporciones, fecha de referencia y antigüedad. Un archivo vacío tiene una proporción indefinida. |

Al importar CSV en Tableau, asigna tipo texto a los GTIN para conservar los ceros iniciales. Mantén la granularidad de producto, tienda y fecha.

## Actualización

El archivo local de trabajo se abre desde `data/tableau/PricePulse - Three-Store Price Comparison - Private.twbx`. Sustituyó al libro anterior de dos tiendas. Carga las capturas elegidas en PostgreSQL, revisa los pares para esas versiones, vuelve a exportar y actualiza las fuentes empaquetadas y las entradas derivadas de los gráficos. Concilia recuentos y diferencias con Desktop, actualiza las cifras visibles y guarda el nuevo paquete y las capturas. La actualización automática de Tableau sigue pendiente.
