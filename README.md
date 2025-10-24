# Informe Presupuesto vs Ejecución (Power BI)

Este proyecto prepara consultas (Power Query) y medidas (DAX) para construir un informe en Power BI con:

1) Ejecución del presupuesto vs lo proyectado en el año.
2) Ejecución del presupuesto vs lo proyectado por cada mes.
3) Ejecución del presupuesto vs lo proyectado por cada equipo.

Archivos de origen:
- `Presupuesto1.csv` (Presupuesto Equipo 1)
- `presupuesto2.csv` (Presupuesto Equipo 2)
- `Prueba de Excel y BI - Asesor de Area Empleo.csv` (Ejecución)

Carpeta con recursos listos para copiar en Power BI:
- `powerbi/queries/*.pq` (Power Query M)
- `powerbi/modeling/*.dax` (Tablas de fecha y dimensiones compartidas)
- `powerbi/measures/Measures.dax` (Medidas DAX)

---

## 1) Cargar y transformar datos (Power Query)

En Power BI Desktop:

- Inicio > Obtener datos > Texto/CSV (opcional). Alternativa recomendada: Inicio > Nueva fuente > Consulta en blanco.
- En el Editor de Power Query, para cada archivo:
  1. Inicio > Nueva consulta > Consulta en blanco > botón derecho > Editor avanzado.
  2. Pegue el contenido del archivo correspondiente:
     - Presupuesto Equipo 1: `powerbi/queries/Presupuesto_Equipo1.pq`
     - Presupuesto Equipo 2: `powerbi/queries/Presupuesto_Equipo2.pq`
     - Ejecución: `powerbi/queries/Ejecucion.pq`
  3. Asigne los nombres exactos a las consultas: `Presupuesto_Equipo1`, `Presupuesto_Equipo2`, `Ejecucion`.

- Cree una consulta adicional para unificar los presupuestos:
  1. Nueva consulta > Consulta en blanco > Editor avanzado.
  2. Pegue `powerbi/queries/Presupuesto_Append.pq`.
  3. Nombre: `Presupuesto`.

Qué hacen las transformaciones:
- Limpian moneda en español (quita `$`, puntos, espacios y maneja negativos como `-$ 21.000`).
- Desapilan (unpivot) los meses del presupuesto a filas.
- Estandarizan `Mes`, `MesNumero`, `Año` y agregan `Periodo` = primer día del mes.
- Con `Ejecucion`, parsea la fecha `Fe.contabilización` (dd/MM/yyyy), suma por campo `Importe en moneda local` como número y mantiene `Tipo de gasto` y `Equipo`.

Acepte y Cerrar & Aplicar para cargar los datos al modelo.

---

## 2) Modelado (tablas de fechas y dimensiones compartidas)

En la vista de **Modelo** de Power BI:

- Cree la tabla de período (una fila por mes): Modelado > Nueva tabla, y pegue el contenido de `powerbi/modeling/DateTable.dax` para crear `DimPeriodo`.
- Cree dimensiones compartidas para filtrar ambas tablas de hechos (presupuesto y ejecución):
  - Modelado > Nueva tabla, pegue `powerbi/modeling/SharedDimensions.dax` para crear `DimTipoGasto` y `DimEquipo`.

### Relaciones (establecer estas 1:* con filtro de unidireccional de la dimensión a los hechos)

- `DimPeriodo[Periodo]` (1) → `Presupuesto[Periodo]` (*)
- `DimPeriodo[Periodo]` (1) → `Ejecucion[Periodo]` (*)
- `DimTipoGasto[Tipo de gasto]` (1) → `Presupuesto[Tipo de gasto]` (*)
- `DimTipoGasto[Tipo de gasto]` (1) → `Ejecucion[Tipo de gasto]` (*)
- `DimEquipo[Equipo]` (1) → `Presupuesto[Equipo]` (*)
- `DimEquipo[Equipo]` (1) → `Ejecucion[Equipo]` (*)

Notas:
- Marque `DimPeriodo` como tabla de fecha si lo desea (Modelado > Marcar como tabla de fechas > Columna: Periodo).
- Configure `DimPeriodo[Mes]` para **Ordenar por** `DimPeriodo[MesNumero]`.

---

## 3) Medidas DAX

- Modelado > Nueva medida. Copie/pegue el contenido de `powerbi/measures/Measures.dax`.

Medidas incluidas:
- `Monto Presupuestado`
- `Monto Ejecutado`
- `Variación`
- `Variación %`
- Versiones "(Año)" que ignoran el filtro de mes para ver el total anual en el contexto del año/equipo seleccionados.

---

## 4) Visuales solicitados

Sugerencia: agregue segmentadores (slicers) para `DimPeriodo[Año]`, `DimTipoGasto[Tipo de gasto]` y `DimEquipo[Equipo]`.

1) Ejecución vs proyectado en el AÑO (vista general)
- 3 Tarjetas: 
  - `Monto Presupuestado (Año)`
  - `Monto Ejecutado (Año)`
  - `Variación (Año)` (formato con separador de miles, negativo en rojo)
- 1 Indicador (Gauge): 
  - Valor: `Monto Ejecutado (Año)` 
  - Objetivo: `Monto Presupuestado (Año)`

2) Ejecución vs proyectado por CADA MES
- Gráfico columnas agrupadas o columnas + línea:
  - Eje: `DimPeriodo[Mes]` (ordenar por `MesNumero`)
  - Valores (columnas): `Monto Presupuestado`, `Monto Ejecutado`
  - Opcional (línea): `Variación %`

3) Ejecución vs proyectado por CADA EQUIPO
- Matriz o tabla:
  - Filas: `DimEquipo[Equipo]`
  - Valores: `Monto Presupuestado`, `Monto Ejecutado`, `Variación`, `Variación %`
  - Opcional: agregue `DimTipoGasto[Tipo de gasto]` como nivel jerárquico para ver el detalle por categoría.

Formato recomendado:
- Mostrar unidades en pesos, separador de miles, sin decimales.
- Para `%`, formato porcentaje con 1-2 decimales.
- Resaltar negativos en rojo.

---

## 5) Consideraciones y validación

- El procesamiento de moneda remueve símbolos y puntos; maneja "-$" como negativo.
- `MesNumero` se calcula por nombre del mes en español; si aparecen meses fuera del catálogo, quedarán como `null`.
- `Periodo` (primer día del mes) permite relaciones limpias mes-a-mes entre tablas.
- Filtros de `Tipo de gasto` y `Equipo` usan dimensiones compartidas, por lo que afectan tanto Presupuesto como Ejecución.

Validación rápida sugerida:
- En una tabla, ponga `DimPeriodo[Mes]`, `Monto Presupuestado`, `Monto Ejecutado` y verifique que Enero 2023 suma los valores esperados según los CSV.
- Pruebe el filtro por `Equipo` y confirme que cambian ambos (presupuesto/ejecución).

---

## 6) Qué entregamos

Se incluyen todos los artefactos para pegar en Power BI:
- Consultas (Power Query): `powerbi/queries/*.pq`
- Tablas de modelo (DAX): `powerbi/modeling/*.dax`
- Medidas (DAX): `powerbi/measures/Measures.dax`

Con esto, puede replicar el informe pedido y extenderlo si necesita más detalles por cuenta, documento o clase de documento.
