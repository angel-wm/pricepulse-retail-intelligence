# Adquisición acotada

[English](../../ACQUISITION.md) · [Inicio en español](../../README.es.md)

Cada spider selecciona una tienda fija y una fecha de publicación. Instala las dependencias con `uv sync --locked`, crea el directorio `data` y ejecuta desde la raíz con una fecha disponible. Los archivos y feeds contienen datos de comercios y se conservan en privado.

```powershell
uv run scrapy crawl spar -a date=2026-11-17 -O data/spar.jl
uv run scrapy crawl kaufland -a date=2026-11-17 -O data/kaufland.jl
uv run scrapy crawl konzum -a date=2026-11-17 -O data/konzum.jl
uv run python -m pytest -q
```

GitHub Actions ejecuta pruebas sintéticas con dependencias fijadas en pushes y pull requests. Las ejecuciones alojadas observadas se registran en [validación](VALIDATION.md).

## Límites y diagnóstico

Los spiders respetan robots.txt, permiten una solicitud concurrente por dominio y aplican una pausa de un segundo, un tiempo de espera de 30 segundos y hasta dos reintentos ante HTTP 408, 500, 502, 503, 504 o errores de transporte que Scrapy considera transitorios. Los códigos 403, 404 y 429 detienen la ejecución. Se rechazan redirecciones, enlaces sin HTTPS, enlaces a otro dominio y respuestas incompletas. Cuando robots.txt no responde con HTTP 200, el middleware bloquea las solicitudes y registra `pricepulse/robots_unavailable`.

Las tiendas fijas son SPAR 8702, Kaufland 5630 y Konzum 1280. Una entrada ausente, duplicada o incompatible detiene la adquisición. Fecha y tienda se extraen del nombre del archivo. La hora de descarga se registra por separado. Comprueba `finish_reason`, solicitudes, estados HTTP, reintentos, estadísticas de robots y manifiesto. Scrapy puede devolver código 0 aunque el spider haya cerrado antes de producir un resultado.

## Formatos y contratos

| Fuente | Descubrimiento y formato |
| --- | --- |
| SPAR | Índice JSON por fecha. CSV CP1250 con punto y coma. El formato anterior trae precios regular y especial separados. El observado el 25 de noviembre de 2026 coloca el indicador inmediatamente después del precio publicado. `NE` indica precio regular y `DA` indica promoción. El precio de referencia queda en la fila original y la categoría es opcional. |
| Kaufland | Índice de archivos y CSV UTF-8 con BOM y tabulaciones. En un patrón el identificador de tienda va seguido de `DDMMYYYY`. El otro incluye un descriptor y un campo numérico antes de `YYYYMMDD`, seguido de una hora de cuatro dígitos. Se exige una coincidencia inequívoca. |
| Konzum | Índice HTML por fecha y CSV UTF-8 separado por comas. Se deduplican enlaces idénticos y se exige un archivo para 1280. El precio de venta pasa al campo regular con `NE` o especial con `DA`. Otros indicadores generan excepciones. La etiqueta de promoción, precio de referencia y precio unitario se conservan en bruto. |

Cada feed JSON Lines empieza con un `manifest` que registra fuente, tienda, fecha solicitada, URL, hora UTC, estado HTTP, SHA-256, dialecto y número de filas. Se comprueba el hash de SPAR si está disponible. Las entradas `record` conservan la fila original, procedencia, número de fila, GTIN original y versión normalizada a 14 dígitos si el dígito de control es válido, además de los importes y su estado. Los decimales se representan con punto en las cadenas. Si existe un único importe válido o ambos coinciden, se registra el precio efectivo. Importes inválidos, ausentes o discrepantes quedan señalados. Encabezados obligatorios incompatibles, encabezados duplicados o filas mal formadas detienen el análisis.

Los recuentos de descubrimiento distinguen entradas del índice, archivos seleccionados y archivos descargados. El ámbito del índice varía por fuente y sus recuentos no miden cobertura de productos o tiendas. Para registrar y comprobar el feed y el CSV original, usa la [captura con registro](RELIABILITY.md#registro-y-recuperación).
