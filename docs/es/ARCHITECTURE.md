# Arquitectura

[English](../../ARCHITECTURE.md) · [Inicio en español](../../README.es.md)

Scrapy obtiene listas oficiales de tres comercios. Python comprueba el dialecto y la identidad de la fuente antes de cargar versiones de archivo en PostgreSQL. Las consultas SQL generan las métricas que se presentan en Tableau.

```text
Índices oficiales de SPAR, Kaufland y Konzum
                    │
           Adaptadores Scrapy
                    │
         CSV y manifiesto de origen
                    │
        Validación y análisis en Python
                    │
      Carga histórica en PostgreSQL
                    │
        Vistas SQL y revisión de pares
                    │
       Exportación y libro de Tableau
```

La tarea de Windows automatiza la captura. La carga, la exportación y la actualización de Tableau son pasos manuales. XML y archivos comprimidos quedan fuera de la implementación actual. Consulta el [estado de la fase 3](CURRENT_STATE.md) para la evidencia de ejecución automática.

| Componente | Responsabilidad |
| --- | --- |
| Adaptadores | Leer el JSON diario de SPAR, el índice de recursos de Kaufland y el HTML por fecha de Konzum. Aplicar límites y registrar resultados HTTP. |
| Manifiesto | Guardar URL original, fecha de la lista, tienda, hora de descarga, hash y respuesta de la fuente. |
| Análisis | Interpretar el dialecto CSV de cada fuente, los decimales locales y los campos de precio. Conservar excepciones de identificación y empaque. |
| PostgreSQL | Preservar observaciones por cadena, tienda, producto, fecha y versión del archivo. Una recarga idéntica no duplica las observaciones. |
| Revisión | Usar GTIN/EAN validado y comprobar marca, cantidad, presentación y variante. Registrar los pares ambiguos. |
| SQL y Tableau | Comparar precios dentro de una tienda en dos fechas y entre tiendas para el mismo producto y fecha. |
| Programación y pruebas | Ejecutar capturas acotadas, detectar cambios de esquema y registrar fallos y reintentos. |

## Contratos de calidad

- **Identidad y granularidad.** Una observación conserva la cadena, la tienda física, el identificador de origen, la fecha de la lista y su versión. Se guardan los códigos originales como texto y se comprueba el dígito de control.
- **Precios.** Usar decimales exactos. Si solo se informa un importe válido, se usa ese valor. Si ambos coinciden, se conserva el origen de ambos. Si discrepan, la observación requiere revisión.
- **Cantidad y presentación.** Guardar por separado la cantidad y unidad declaradas y el tamaño inferido de la descripción. Revisar paquetes múltiples, variantes y pesos escurridos. El valor `KOM` no expresa volumen físico.
- **Cobertura.** Registrar filas, GTIN válidos y campos completos por tienda y fecha. Un aumento del 47,9 % en un archivo de Kaufland durante la transición normativa ilustra la necesidad de detectar cambios de cobertura.
- **Trazabilidad.** Una URL puede reutilizarse para listas actualizadas. El hash permite distinguir versiones. El periodo de disponibilidad documentado para listas reemplazadas es de 15 días.

Consulta los [contratos y objetivos](PROJECT_SPEC.md), la [viabilidad de las fuentes](SOURCE_FEASIBILITY.md) y las [decisiones de diseño](DECISIONS.md).
