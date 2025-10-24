# Guía de implementación: Preguntas 4 a 8 (Power BI)

Esta guía explica cómo agregar medidas y construir las vistas para responder a las preguntas 4–8. No se requieren nuevas consultas; trabajaremos sobre:

- Hechos: `presupuesto_col` (presupuestado), `ejecucion` (ejecutado)
- Dimensiones: `DimPeriodo`, `DimTipoGasto`, `DimEquipo`
- Medidas base de `Measures_presupuesto_col.dax`
- Medidas avanzadas de `powerbi/measures/Measures_advanced.dax`

---

## 0) Preparación (1 minuto)

1. Modelado > Nueva medida > pega todo el contenido de `powerbi/measures/Measures_advanced.dax`.
2. Opcional: Ajusta umbrales de alerta dentro del archivo (por defecto 90% y 110%):
   - `_UmbralSubejecucion = 0.9`
   - `_UmbralSobrejecucion = 1.1`

---

## 4) Indicador de cumplimiento para la ejecución presupuestal

Medidas clave:
- `Cumplimiento %` y `Cumplimiento % (Año)`
- `Cumplimiento KPI`

Paso a paso:
1. Inserta una Tarjeta con `Cumplimiento % (Año)`.
2. Inserta un Indicador (Gauge):
   - Valor: `Monto Ejecutado (Año)`
   - Objetivo: `Monto Presupuestado (Año)`
   - Título: “Cumplimiento anual”.
3. Inserta una Tarjeta o etiqueta con `Cumplimiento KPI` para reflejar el estado (En línea, Subejecución, Sobre-ejecución).
4. Formato: porcentaje 0.0% para `Cumplimiento % (Año)`.

Validación:
- Cambia el slicer de Año/Equipo y verifica que el Gauge y la tarjeta reaccionen coherentemente.

---

## 5) Comportamiento del presupuesto según el tipo de gasto

Medidas clave:
- `Monto Presupuestado`, `Monto Ejecutado`
- `Ejecutado % del total (Tipo)`, `Presupuestado % del total (Tipo)`

Paso a paso:
1. Gráfico de columnas agrupadas:
   - Eje: `DimTipoGasto[Tipo de gasto]`
   - Valores: `Monto Presupuestado`, `Monto Ejecutado`
   - Ordena descendente por `Monto Ejecutado` para ver concentración.
2. Gráfico de barras apiladas 100% (composición):
   - Eje: `DimTipoGasto[Tipo de gasto]`
   - Valores: `Ejecutado % del total (Tipo)` y/o `Presupuestado % del total (Tipo)`
3. Slicers: Año y Equipo para analizar la composición por filtros.

Notas:
- Formato de %: 0.0%.
- Usa tooltips con `Variación` y `Cumplimiento %` para mayor contexto.

---

## 6) Alertas mensuales de sub/sobre ejecución por equipo y tipo de gasto

Medidas clave:
- `Cumplimiento %`, `Alerta Código`, `Alerta Color`, `Alerta Tooltip`, `Mostrar solo alertas`

Paso a paso (Matriz-Heatmap):
1. Matriz:
   - Filas: `DimPeriodo[Mes]` (Ordenar por `MesNumero`)
   - Columnas: `DimEquipo[Equipo]`
   - (Opcional) Agrega `DimTipoGasto[Tipo de gasto]` como nivel adicional (filas o columnas) para el drill.
   - Valores: `Cumplimiento %`
2. Formato condicional:
   - Color de fondo → “Formato basado en campo” → Selecciona `Alerta Color`.
   - Tooltip del visual: agrega la medida `Alerta Tooltip` para explicaciones.
3. Filtrar solo alertas:
   - Panel de filtros del visual: `Mostrar solo alertas` = 1.

Sugerencia de umbrales:
- Subejecución: < 90%
- En línea: 90%–110%
- Sobre-ejecución: > 110%

---

## 7) Comparación entre equipos (quién ejecuta mejor)

Medidas clave:
- `Cumplimiento Índice (cercanía a 100%)`
- `Equipo con mejor ejecución`
- `Brecha Cumplimiento % (entre equipos)`

Paso a paso:
1. Gráfico de columnas agrupadas:
   - Eje: `DimEquipo[Equipo]`
   - Valores: `Cumplimiento %`
   - Tooltip: agrega `Cumplimiento Índice (cercanía a 100%)`, `Variación`, `Cumplimiento % YTD`.
2. Tarjeta: `Equipo con mejor ejecución`.
3. Tarjeta: `Brecha Cumplimiento % (entre equipos)`.
4. (Opcional) Small multiples por `DimTipoGasto[Tipo de gasto]` para ver en qué categorías cada equipo rinde mejor.

Interpretación:
- Índice cercano a 1.0 indica mayor alineación al 100% del plan (castiga tanto sub como sobre-ejecución).

---

## 8) Métricas adicionales propuestas

A) Acumulado YTD
- Medidas: `Monto Presupuestado YTD`, `Monto Ejecutado YTD`, `Cumplimiento % YTD`, `Variación YTD`, `Brecha % YTD`.
- Visual:
  - Tarjeta: `Cumplimiento % YTD`.
  - Gráfico de líneas: eje `DimPeriodo[Mes]`; líneas `Cumplimiento %` y `Cumplimiento % YTD`.
  - Tarjeta: `Variación YTD`.

B) Volatilidad del cumplimiento (estabilidad)
- Medida: `Volatilidad Cumplimiento (STDEV)`.
- Visual:
  - Tabla por `DimEquipo[Equipo]` con: `Cumplimiento %` (promedio), `Volatilidad Cumplimiento (STDEV)`.
  - Menor STDEV = ejecución más estable.

---

## Formato y UX

- Moneda: `$ #,##0` (sin decimales).
- Porcentajes: `0.0%`.
- Resalta negativos en rojo (Variación/Variación YTD).
- Usa `Alerta Color` para heatmaps.
- Ordena `Mes` por `MesNumero` en todos los visuales temporales.

---

## Troubleshooting

- “Medida no encontrada”: verifica que has pegado primero `Measures_presupuesto_col.dax` y luego `Measures_advanced.dax`.
- “No aplica color condicional”: usa el modo “Formato basado en campo” y selecciona la medida `Alerta Color`.
- “Mes desordenado”: establece `DimPeriodo[Mes]` → “Ordenar por” → `DimPeriodo[MesNumero]`.
- “Valores en blanco”: si el presupuesto es 0, `Cumplimiento %` devuelve BLANK() para evitar división por cero.

---

## Resumen

Con estas medidas y vistas:
- (4) KPI de cumplimiento anual y por contexto.
- (5) Composición y comportamiento por tipo de gasto (montos y % participación).
- (6) Matriz de alertas por mes/equipo/tipo con colores y tooltip.
- (7) Comparación directa entre equipos y brecha de desempeño.
- (8) Visión acumulada YTD y estabilidad (volatilidad) del cumplimiento.

Si quieres, puedo crear un tema JSON con paleta (verde/naranja/rojo) y un parámetro What‑If para controlar umbrales desde el reporte. Solo dime y lo genero en la carpeta `powerbi/theme/`.
