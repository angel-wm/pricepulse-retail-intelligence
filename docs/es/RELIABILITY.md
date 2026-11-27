# Fiabilidad operativa local

[English](../../RELIABILITY.md) · [Inicio en español](../../README.es.md)

La fase 3 incluye capturas acotadas con evidencia, recuperación explícita y señales provisionales de calidad. Su cierre sigue pendiente de revisión.

## Registro y recuperación

Desde la raíz, ejecuta una captura para una tienda y fecha:

```powershell
uv run --locked python -m pricepulse.reliability --source spar --date 2026-11-17 --directory data/runs
```

Usa `kaufland` para 5630 o `konzum` para 1280. La disponibilidad de archivos históricos puede caducar. Cada ejecución genera un informe JSON, feed, CSV y registro Scrapy privados. El informe empieza con `running`. El éxito exige salida 0, cierre normal de Scrapy, manifiesto coherente, SHA-256 del CSV y feed completo con recuento y procedencia esperados. Un fallo detectado queda como `failed` y una interrupción controlada como `interrupted`. Si una terminación abrupta deja `running`, investiga antes de continuar. Cada reintento conserva su propia evidencia.

Para cargar un informe exitoso, configura `PRICEPULSE_DSN` y ejecuta:

```powershell
uv run --locked python -m pricepulse.recovery data/runs/<run-id>.json
```

La recuperación comprueba los hashes del CSV y el feed y registra el resultado de la carga. Si la base confirmó la transacción antes de que se actualizara el informe, puedes repetir la operación sin duplicar observaciones. El registro de adquisición puede crecer. Investiga los archivos modificados o ausentes.

Para un lote manual de las tres tiendas:

```powershell
uv run --locked python -m pricepulse.batch --date 2026-11-17 --directory data/runs
```

Sin `--date`, se usa la fecha de Zagreb. Añade `--ingest` después de configurar el DSN e [inicializar o actualizar el esquema](POSTGRESQL.md#base-de-desarrollo). Un fallo de captura o de carga solicitada deja el lote `incomplete`. El bloqueo se aplica por directorio. Si queda `batch.lock` después de una interrupción, comprueba el proceso y el informe antes de quitarlo.

## Programación en Windows

La prueba de horario calcula la próxima ejecución propuesta sin descargar archivos:

```powershell
uv run --locked python -m pricepulse.scheduling --now 2026-11-22T09:00:00+00:00
```

La tarea `PricePulse-Local-Collect` se registró el 23 de noviembre de 2026. El disparador horario solo intenta una captura por fecha de Zagreb, a partir de las 12:15 de esa zona y mientras la sesión del usuario esté iniciada. Opera en `data/scheduled` y solo recopila archivos. Comprueba un límite de **1 GiB** antes de iniciar cada lote. Un lote puede superar el límite. La tarea conserva los archivos.

Un resultado distinto de cero puede corresponder a un intento previo registrado. Revisa el marcador diario y el lote asociado. Para repetir deliberadamente en el mismo directorio tras corregir la causa, conserva el marcador original y los informes, archiva el marcador activo con la tarea inactiva y comprueba que el siguiente disparo siga dentro de la misma fecha de Zagreb. La colección genera otro marcador. El instalador protege las tareas existentes con el mismo nombre. Puedes pausar con `Disable-ScheduledTask -TaskName 'PricePulse-Local-Collect'`.

## Señales provisionales

El marcador incluye antigüedad mayor de un día, fecha futura, variación absoluta de filas superior al 30 % frente al informe exitoso anterior de la misma fuente y tienda, excepciones de precio por encima del 1 % o GTIN con dígito de control válido por debajo del 90 %. Sin referencia previa, la variación es desconocida. La edad se mide a partir de la fecha de lista. Una captura con alertas queda como `success_with_alerts` y devuelve un código distinto de cero.

```powershell
uv run --locked python -m pricepulse.monitor source --current data/runs/<run-id>.json --as-of 2026-11-23 --max-age-days 2
uv run --locked python -m pricepulse.monitor batches data/runs/<batch-id>.json
uv run --locked python -m pricepulse.monitor coverage <file-id-1> <file-id-2>
```

`source` y `batches` devuelven código 2 ante una alerta. Las métricas de lotes describen los informes aportados. `coverage` exige DSN y mide la revisión de pares elegibles encolados para los dos archivos seleccionados. Estas señales son umbrales de ingeniería provisionales. Consulta los [resultados registrados](VALIDATION.md).
