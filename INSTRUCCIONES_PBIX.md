# Guía Paso a Paso: Crear PBIX Programáticamente

Este proyecto incluye un script Python que genera automáticamente el archivo `.pbix` desde los archivos de consultas (Power Query) y modelado (DAX).

## Opción A: Script Automático (Recomendado)

### Requisitos previos

1. **Instalar pbi-tools** (herramienta CLI para Power BI):
   ```powershell
   dotnet tool install -g pbi-tools
   ```
   
   Si no tienes .NET SDK instalado, descarga pbi-tools desde: https://pbi.tools/

2. **Python 3.7+** (viene con Windows 10/11)

### Pasos

1. Abre PowerShell en la carpeta del proyecto:
   ```powershell
   cd "c:\Users\USER\Desktop\Prueba"
   ```

2. Ejecuta el script:
   ```powershell
   python create_pbix.py
   ```

3. El script hará:
   - ✅ Crear la estructura PbixProj
   - ✅ Generar el modelo de datos (tablas, columnas, relaciones)
   - ✅ Incluir todas tus consultas Power Query
   - ✅ Agregar las medidas DAX
   - ✅ Compilar todo a `PresupuestoAnalisis.pbix`

4. Abre el archivo generado en Power BI Desktop:
   ```powershell
   start PresupuestoAnalisis.pbix
   ```

---

## Opción B: Manual en Power BI Desktop (5 minutos)

Si prefieres hacerlo manualmente o el script da error:

### Paso 1: Abrir Power BI Desktop y cargar consultas

1. Abre **Power BI Desktop** → Nueva pestaña vacía
2. **Transformar datos** (Power Query Editor)

3. Cargar cada consulta:
   - Inicio > Nueva consulta > Consulta en blanco
   - Botón derecho > Editor avanzado
   - Pega el contenido de:
     - `powerbi/queries/Presupuesto_Equipo1.pq` → nombre: `Presupuesto_Equipo1`
     - `powerbi/queries/Presupuesto_Equipo2.pq` → nombre: `Presupuesto_Equipo2`
     - `powerbi/queries/Ejecucion.pq` → nombre: `ejecucion`
     - `powerbi/queries/Presupuesto_Append.pq` → nombre: `presupuesto_col`

4. **Cerrar y aplicar**

### Paso 2: Crear tablas de modelado

En la pestaña **Modelado** > **Nueva tabla**:

1. **DimPeriodo**: pega `powerbi/modeling/DateTable.dax`
2. **DimTipoGasto**: pega `powerbi/modeling/DimTipoGasto.dax`
3. **DimEquipo**: pega `powerbi/modeling/DimEquipo.dax`

### Paso 3: Crear relaciones

Vista de **Modelo** > arrastra para crear relaciones (1:*):

- `DimPeriodo[Periodo]` → `presupuesto_col[Periodo]`
- `DimPeriodo[Periodo]` → `ejecucion[Periodo]`
- `DimTipoGasto[Tipo de gasto]` → `presupuesto_col[Tipo de gasto]`
- `DimTipoGasto[Tipo de gasto]` → `ejecucion[Tipo de gasto]`
- `DimEquipo[Equipo]` → `presupuesto_col[Equipo]`
- `DimEquipo[Equipo]` → `ejecucion[Equipo]`

### Paso 4: Crear medidas

Modelado > **Nueva medida** (pega cada una de `powerbi/measures/Measures_presupuesto_col.dax`):

- `Monto Presupuestado`
- `Monto Ejecutado`
- `Variación`
- `Variación %`
- `Monto Presupuestado (Año)`
- `Monto Ejecutado (Año)`
- `Variación (Año)`
- `Variación % (Año)`

### Paso 5: Crear visuales

#### Slicers (filtros):
- `DimPeriodo[Año]`
- `DimTipoGasto[Tipo de gasto]`
- `DimEquipo[Equipo]`

#### 1. Ejecución vs Proyectado (AÑO):
- 3 **Tarjetas**:
  - `Monto Presupuestado (Año)`
  - `Monto Ejecutado (Año)`
  - `Variación (Año)`
- 1 **Indicador** (Gauge):
  - Valor: `Monto Ejecutado (Año)`
  - Objetivo: `Monto Presupuestado (Año)`

#### 2. Ejecución vs Proyectado (MES):
- **Gráfico de columnas agrupadas**:
  - Eje X: `DimPeriodo[Mes]` (ordenar por `MesNumero`)
  - Valores: `Monto Presupuestado`, `Monto Ejecutado`
  - Línea: `Variación %`

#### 3. Ejecución vs Proyectado (EQUIPO):
- **Matriz**:
  - Filas: `DimEquipo[Equipo]`
  - Valores: `Monto Presupuestado`, `Monto Ejecutado`, `Variación`, `Variación %`

### Paso 6: Guardar

**Archivo** > **Guardar como** > `PresupuestoAnalisis.pbix`

---

## Notas

- El script Python genera la estructura completa, pero **necesitas pbi-tools** para compilar a .pbix
- La opción manual es más rápida si ya tienes Power BI Desktop abierto
- Ambos métodos producen el mismo resultado final

## Troubleshooting

### Script da error "pbi-tools not found"
```powershell
dotnet tool install -g pbi-tools
# o descarga desde https://pbi.tools/
```

### Power Query: "No se encuentra el archivo CSV"
- Verifica que las rutas en los archivos .pq sean correctas:
  ```m
  File.Contents("c:\\Users\\USER\\Desktop\\Prueba\\Presupuesto1.csv")
  ```

### Relaciones no se crean automáticamente
- Asegúrate de que las columnas `Periodo`, `Tipo de gasto` y `Equipo` existan en ambas tablas
- Verifica que el tipo de dato sea el mismo (fecha con fecha, texto con texto)
