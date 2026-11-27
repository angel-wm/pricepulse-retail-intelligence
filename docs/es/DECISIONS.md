# Decisiones del proyecto

[English](../../DECISIONS.md) · [Inicio en español](../../README.es.md)

## Registro de decisiones

Cada entrada resume la decisión en el momento en que se tomó. Para su evolución posterior consulta el [estado actual](CURRENT_STATE.md).

| ID | Decisión |
| --- | --- |
| D-001 | Usar Scrapy para la adquisición inicial. Su gestión de solicitudes y descargas se adapta a listas públicas con descubrimiento específico por fuente. |
| D-002 | Usar PostgreSQL para conservar procedencia, relaciones entre productos y tiendas, cargas idempotentes e historial. |
| D-003 | Elegir Tableau para análisis y presentación de tendencias y comparaciones. La publicación depende de las condiciones de uso aplicables. |
| D-004 | Reservar Crawlee para un proyecto con otro problema. |
| D-005 | Aplicar convenciones de legibilidad y conservar documentos canónicos por tema. |
| D-006 | Mantener el nombre PricePulse y enfocar el proyecto en listas croatas de supermercados y artículos del hogar. Priorizar SPAR y Kaufland. |
| D-007 | Modelar precios publicados por tienda, producto y fecha. Aplazar métricas de existencias hasta tener evidencia con ese significado. |
| D-008 | Adquirir CSV oficiales y modelar campos regular y especial por fuente. El análisis final recuperó casos de precio especial y elevó las coincidencias con precio de 8.263 a 8.869. |
| D-009 | Calificar SPAR 8702 y Kaufland 5630 tras las pruebas acotadas. Conservar campos originales, revisar formatos y mantener Lidl fuera del alcance inicial. |
| D-010 | Cerrar fase 0 el 19 de noviembre de 2026 y mantener una autorización explícita para implementar la fase 1. |
| D-011 | Autorizar fase 1 el 19 de noviembre y solicitar PULSE-12 y sus subtareas. |
| D-012 | Cerrar fase 1 y autorizar PostgreSQL histórico de fase 2 el 22 de noviembre. |
| D-013 | Autorizar que fase 3 avance antes de revisar y cerrar fase 2. Cada cierre conserva sus condiciones. |
| D-014 | Programar una captura diaria local sin carga ni publicación automática. |
| D-015 | Cerrar fase 2 el 23 de noviembre después de revisar una versión histórica por comercio, repetir la carga sin duplicar observaciones y verificar cuatro comparaciones. |
| D-016 | Cerrar fase 4 el 23 de noviembre para el libro privado en inglés con datos reales tras conciliar SQL y verificar interacción en Desktop. |
| D-017 | Autorizar fase 5 el 23 de noviembre para validación, configuración reproducible y preparación de la entrega. |
| D-018 | Autorizar Konzum 1280 el 23 de noviembre. Su cohorte compartida con las dos cadenas existentes fue mayor y mantuvo el formato en ambas fechas. |
| D-019 | Seleccionar el libro de tres tiendas con datos reales como única entrega de Tableau el 24 de noviembre, junto a capturas de presentación en GitHub. |
| D-020 | Cerrar fase 5 el 25 de noviembre tras la revisión técnica, la instalación reproducible y la publicación. La revisión de la captura automática queda en fase 3. |
