# Especificación de PricePulse

[English](../../PROJECT_SPEC.md) · [Inicio en español](../../README.es.md)

El proyecto transforma observaciones de listas oficiales de precios en series históricas trazables y comparaciones entre productos equivalentes. Su ámbito inicial son los supermercados y artículos del hogar en Croacia, con importes en EUR.

## Preguntas analíticas

- ¿Cuánto cambia el precio publicado de un producto verificado entre observaciones?
- ¿Qué diferencia hay entre tiendas para un producto comparable?
- ¿En qué categorías son mayores las diferencias relativas?
- ¿Qué proporción de filas tiene identificador válido, precio utilizable, unidad interpretable y procedencia trazable?
- ¿Con qué frecuencia aparecen las listas esperadas y se cargan correctamente?

La disponibilidad en tienda y el inventario quedan fuera del alcance.

## Cohorte e identidad

La primera pareja calificada fue SPAR Zagreb Jankomir 8702 y Kaufland Zagreb Antuna Šoljana 5630. Se autorizó Konzum Zagreb Velimira Škorpika 1280 como tercera fuente. Lidl quedó fuera por decisión de alcance. Cada comercio representa una tienda física. Las comparaciones entre tiendas requieren la misma fecha de lista. El historial exige mantener la identidad de la tienda entre fechas.

Se validan GTIN-8, 12, 13 y 14 y se usa una representación normalizada de 14 dígitos, conservando el valor original. Verificar marca, presentación, variante y cantidad. Las excepciones incluyen multipacks, cantidades en conflicto y peso bruto frente a escurrido. De 160 candidatos estrictos seleccionados de forma determinista, 102 tuvieron descripciones coherentes y 58 quedaron pendientes. El resultado corresponde a esa muestra y esa revisión documental.

## Contrato de datos propuesto

| Atributos | Regla |
| --- | --- |
| `source_chain`, `source_url`, `source_file_hash` | Conservar procedencia exacta. |
| `source_store_id`, `store_location` | Identificar el punto de venta físico. |
| `price_list_date`, `source_published_at`, `collected_at_utc` | Separar fecha de vigencia, hora de publicación si consta y hora de captura. |
| `retailer_product_code` | Identificador local del comercio. |
| `gtin_ean`, `title`, `brand` | Revisar validez y coherencia antes de afirmar una coincidencia. |
| `net_quantity`, `unit`, `category` | Admitir ausencia y normalizar unidades comparables. |
| `regular_price_eur`, `special_price_eur`, `effective_price_eur`, `price_origin`, `unit_price_eur` | Conservar campos originales e importes positivos en Decimal. Usar el único campo válido o el valor común. Registrar conflictos explícitos. |
| `sale_indicator`, `baseline_price_eur` | Conservar su significado por fuente. El precio de referencia carece de la fecha necesaria para incorporarlo al historial. |
| `raw_row`, `ingestion_status` | Guardar la evidencia de valores inválidos y excepciones. |

## Condiciones de aceptación

La viabilidad se revisó con HTTP 200 para índices y archivos seleccionados, 8.869 códigos con precio el mismo día, 4.155 candidatos estrictos, dos fechas para cada tienda y recuperación de promociones de SPAR. La implementación se evalúa por separado mediante adaptadores individuales, fixtures, trazabilidad, control de solicitudes y validación por campo. Consulta [validación](VALIDATION.md) y [hoja de ruta](ROADMAP.md).

El flujo prioriza Python, Scrapy, PostgreSQL y Tableau con herramientas reproducibles localmente, respetando términos, robots.txt, controles de acceso y ritmo de solicitudes. El portafolio contiene el libro de Tableau y sus capturas. Los archivos de adquisición y procesamiento permanecen locales.
