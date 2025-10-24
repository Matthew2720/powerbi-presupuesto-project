# 🚀 GUÍA RÁPIDA: Crear el PBIX en Power BI Desktop

## ✅ YA TIENES TODO LISTO
El script Python ya generó:
- ✅ Estructura PbixProj completa
- ✅ Modelo de datos con relaciones
- ✅ Consultas Power Query listas
- ✅ Medidas DAX preparadas

## 📋 PASOS FINALES (5 minutos)

### 1️⃣ Abrir Power BI Desktop
Haz doble clic en: **`abrir_powerbi.bat`**

O manualmente:
- Inicio > Power BI Desktop

### 2️⃣ Cargar Consultas (Power Query)

1. **Transformar datos** (ribbon superior)
2. Para cada consulta, haz:
   - **Inicio** > **Nueva consulta** > **Consulta en blanco**
   - Botón derecho sobre "Consulta1" > **Editor avanzado**
   - Abre y copia el contenido de:

| Archivo | Nombre en Power BI |
|---------|-------------------|
| `powerbi/queries/Presupuesto_Equipo1.pq` | `Presupuesto_Equipo1` |
| `powerbi/queries/Presupuesto_Equipo2.pq` | `Presupuesto_Equipo2` |
| `powerbi/queries/Ejecucion.pq` | `ejecucion` |
| `powerbi/queries/Presupuesto_Append.pq` | `presupuesto_col` |

3. **Cerrar y aplicar**

### 3️⃣ Crear Tablas de Dimensiones

En la pestaña **Modelado** > **Nueva tabla**, pega:

1. **DimPeriodo**: contenido de `powerbi/modeling/DateTable.dax`
2. **DimTipoGasto**: contenido de `powerbi/modeling/DimTipoGasto.dax`
3. **DimEquipo**: contenido de `powerbi/modeling/DimEquipo.dax`

### 4️⃣ Crear Relaciones

Vista de **Modelo** (icono en barra izquierda), arrastra para unir:

```
DimPeriodo[Periodo] ────┬──> presupuesto_col[Periodo]
                        └──> ejecucion[Periodo]

DimTipoGasto[Tipo de gasto] ──┬──> presupuesto_col[Tipo de gasto]
                              └──> ejecucion[Tipo de gasto]

DimEquipo[Equipo] ──┬──> presupuesto_col[Equipo]
                    └──> ejecucion[Equipo]
```

(Todas 1:* con filtro unidireccional de dimensión → hecho)

### 5️⃣ Crear Medidas

**Modelado** > **Nueva medida**, copia estas 8 medidas de `powerbi/measures/Measures_presupuesto_col.dax`:

```dax
Monto Presupuestado = SUM(presupuesto_col[Monto Presupuestado])
Monto Ejecutado = SUM(ejecucion[Monto Ejecutado])
Variación = [Monto Ejecutado] - [Monto Presupuestado]
Variación % = DIVIDE([Variación], [Monto Presupuestado])
Monto Presupuestado (Año) = CALCULATE([Monto Presupuestado], ALL(DimPeriodo[Periodo]))
Monto Ejecutado (Año) = CALCULATE([Monto Ejecutado], ALL(DimPeriodo[Periodo]))
Variación (Año) = [Monto Ejecutado (Año)] - [Monto Presupuestado (Año)]
Variación % (Año) = DIVIDE([Variación (Año)], [Monto Presupuestado (Año)])
```

### 6️⃣ Crear Visuales

#### 🎛️ Slicers (parte superior):
- `DimPeriodo[Año]`
- `DimTipoGasto[Tipo de gasto]`
- `DimEquipo[Equipo]`

#### 📊 Visual 1: RESUMEN ANUAL (pregunta 1)
- 3 **Tarjetas**:
  - `Monto Presupuestado (Año)` 
  - `Monto Ejecutado (Año)`
  - `Variación (Año)`
- 1 **Indicador** (Gauge):
  - Valor: `Monto Ejecutado (Año)`
  - Objetivo: `Monto Presupuestado (Año)`

#### 📈 Visual 2: POR MES (pregunta 2)
- **Gráfico de columnas agrupadas**:
  - Eje X: `DimPeriodo[Mes]` 
    - ⚠️ **Importante**: Ordenar por `MesNumero` (clic en "..." del visual > Ordenar eje > MesNumero)
  - Valores: `Monto Presupuestado`, `Monto Ejecutado`
  - Línea (opcional): `Variación %`

#### 📋 Visual 3: POR EQUIPO (pregunta 3)
- **Matriz**:
  - Filas: `DimEquipo[Equipo]`
  - Valores: 
    - `Monto Presupuestado`
    - `Monto Ejecutado`
    - `Variación`
    - `Variación %`
  - Opcional: Expandir con `DimTipoGasto[Tipo de gasto]` para detalle

#### 🎨 Formato sugerido:
- Moneda: formato pesos `$ #,##0`
- Porcentaje: `0.0%`
- Variaciones negativas: color rojo condicional

### 7️⃣ Guardar
**Archivo** > **Guardar como** > `PresupuestoAnalisis.pbix`

---

## 🎯 RESPUESTAS A LAS 3 PREGUNTAS

Con estos visuales ya respondes:

1. ✅ **Ejecución vs proyectado en el año**: Tarjetas + Gauge (muestra totales anuales)
2. ✅ **Ejecución vs proyectado por mes**: Gráfico de columnas con Mes en eje X
3. ✅ **Ejecución vs proyectado por equipo**: Matriz con Equipo en filas

---

## 📂 Ubicación de archivos

```
C:\Users\USER\Desktop\Prueba\
├── powerbi/
│   ├── queries/         ← Copiar desde aquí para Power Query
│   ├── modeling/        ← Copiar desde aquí para tablas DAX
│   └── measures/        ← Copiar desde aquí para medidas DAX
├── abrir_powerbi.bat    ← Ejecutar para abrir Power BI Desktop
├── create_pbix.py       ← Ya ejecutado (creó estructura PbixProj)
└── GUIA_RAPIDA.md       ← Este archivo
```

---

## ❓ Troubleshooting

### "No se encuentra el archivo CSV"
En Power Query, cambia la ruta si moviste los CSV:
```m
File.Contents("c:\\Users\\USER\\Desktop\\Prueba\\Presupuesto1.csv")
```

### "No se puede crear la relación"
- Verifica que ambas columnas tengan el mismo tipo de dato (fecha con fecha, texto con texto)
- Revisa que no haya valores nulos en las columnas clave

### "Medida da error"
- Asegúrate de que los nombres de tablas sean exactos: `presupuesto_col`, `ejecucion`, `DimPeriodo`
- Las medidas distinguen mayúsculas/minúsculas en nombres de columna

---

## 🚀 ¿Listo?

Ejecuta: **`abrir_powerbi.bat`** y sigue los pasos de arriba.

¡En 5 minutos tendrás tu reporte completo!
