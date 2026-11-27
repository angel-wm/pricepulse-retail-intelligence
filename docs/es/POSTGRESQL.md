# Historial local en PostgreSQL

[English](../../POSTGRESQL.md) · [Inicio en español](../../README.es.md)

Usa una base privada dedicada para archivos reales. Mantén en privado los CSV, resultados por fila, volcados de base de datos y credenciales.

## PostgreSQL local con Docker Compose

Desde la raíz del repositorio, usa PowerShell 7 y Docker Desktop en modo de contenedores Linux o Docker Engine con Compose. Completa primero el [inicio rápido de Python](../../README.es.md#inicio-rápido-en-windows-powershell). Compose ejecuta PostgreSQL 18.7. Python, Scrapy y Tableau se ejecutan en el equipo anfitrión.

### Base de desarrollo

```powershell
$env:PRICEPULSE_DB_PASSWORD = Read-Host 'Local PostgreSQL password' -MaskInput
docker compose up --wait db
$encodedPassword = [uri]::EscapeDataString($env:PRICEPULSE_DB_PASSWORD)
$env:PRICEPULSE_DSN = "postgresql://pricepulse:$encodedPassword@127.0.0.1:55432/pricepulse"
uv run --locked python -m pricepulse.ingest init
```

Usa una contraseña privada y no vacía. PostgreSQL inicializa la cuenta y la base una vez en el volumen `postgres-data`. Conserva la contraseña original para arranques posteriores. Ejecuta `init` en una base existente antes de cargar Konzum 1280 para aplicar la restricción actualizada sin perder los archivos y observaciones existentes.

El puerto predeterminado es `55432`, enlazado a la interfaz local IPv4. Si está ocupado, define `PRICEPULSE_DB_PORT` antes de arrancar y usa el mismo puerto en el DSN. Usa `docker compose down` para detener el servicio conservando su volumen. **Con `--volumes`, la base de desarrollo se elimina de forma permanente.** Para diagnosticar el arranque, usa `docker compose ps` o `docker compose logs db`.

### Base desechable de integración

```powershell
$env:PRICEPULSE_TEST_DB_PASSWORD = [guid]::NewGuid().ToString('N')
docker compose up --wait db-test
$env:PRICEPULSE_TEST_DSN = "postgresql://pricepulse_test:$env:PRICEPULSE_TEST_DB_PASSWORD@127.0.0.1:55433/pricepulse_test"
uv run --locked python -m pytest -q
docker compose rm --stop --force db-test
Remove-Item Env:PRICEPULSE_TEST_DSN, Env:PRICEPULSE_TEST_DB_PASSWORD
```

`db-test` activa su perfil al solicitarlo y puede funcionar en paralelo con desarrollo. Usa otra cuenta, otro puerto local y almacenamiento temporal en memoria. Al detenerlo se descartan los datos de prueba. Si cambias `PRICEPULSE_TEST_DB_PORT`, actualiza el DSN de pruebas.

## Carga inicial

Usa una base o un esquema dedicado. `init` aplica el SQL al `search_path` de la conexión. Configura `PRICEPULSE_DSN` de forma privada.

```powershell
uv sync --locked
uv run --locked python -m pricepulse.ingest init
uv run --locked python -m pricepulse.ingest load --source spar --store 8702 --date 2026-11-17 --url https://www.spar.hr/example.csv --collected-at 2026-11-22T23:00:00+00:00 --http-status 200 --csv data/private-source.csv
```

La ruta, URL, fecha y hora son ilustrativas. Usa el archivo y los metadatos de una captura permitida. El cargador calcula el SHA-256 de los bytes y comprueba HTTPS y el host aprobado. La URL, fecha, hora y estado HTTP provienen del operador.

Cada archivo se versiona por cadena, tienda, fecha y SHA-256. Cargar los mismos bytes registra otra ejecución, sin duplicar filas ni observaciones. Los bytes distintos crean otra versión. Una transacción revierte la escritura si falla la carga. `source_row.raw_row` conserva la fila original. SKU ausentes o duplicados impiden crear observaciones. GTIN inválidos o duplicados, marca o cantidad ausente y problemas de precio generan excepciones. Para una captura previa, usa la [recuperación](RELIABILITY.md#registro-y-recuperación) con el informe, el feed y el CSV archivado.

## Consultas y revisión

- `price_history` conserva las versiones. `price_changes(array_of_file_ids)` requiere como máximo una versión por tienda y fecha. Compara SKU con GTIN válido, título, marca, cantidad y unidad estables y sin excepciones.
- `source_quality` presenta recuentos por archivo.
- `pricepulse.matching.queue_candidates` encola filas con precio y GTIN normalizado común de dos archivos elegidos, conservando las decisiones previas.
- `comparison_flags` identifica descriptores, marcas y cantidades faltantes o diferentes. Las equivalencias de marca deben declararse expresamente.
- `pricepulse.matching.record_review` registra decisiones para versiones exactas. `verified_price_comparison` solo incluye pares aprobados de la misma fecha, con GTIN compartido válido, precio y sin excepciones pendientes.
- `queue_history_changes` encola cambios de GTIN o descriptores del mismo SKU entre fechas. Su revisión es independiente de `price_changes`.

La comparación entre comercios convierte cantidades de masa explícitas a kilogramos con decimales exactos. En SPAR usa `kg` o `g`. En Kaufland, la columna indica `(KG)` y se conserva la unidad original como evidencia. Piezas y volumen no se pueden comparar directamente con masa. Una misma masa no confirma variante o empaque.

## Validación

Para usar una base desechable existente, configura `PRICEPULSE_TEST_DSN` con un usuario que pueda crear y eliminar esquemas y ejecuta `uv run --locked python -m pytest -q`. Cada prueba de integración usa un esquema de nombre aleatorio. Sin esa variable, las pruebas de integración se omiten. Consulta los [resultados observados](VALIDATION.md).
