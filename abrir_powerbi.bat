@echo off
REM Script para abrir Power BI Desktop e importar el proyecto

echo ============================================================
echo   ABRIR PROYECTO EN POWER BI DESKTOP
echo ============================================================
echo.
echo El proyecto PbixProj ya fue creado en:
echo   %~dp0PresupuestoAnalisis.PbixProj
echo.
echo OPCION RAPIDA: Crear manualmente en Power BI Desktop
echo --------------------------------------------------------
echo.
echo 1. Abre Power BI Desktop (busca en el menu Inicio)
echo.
echo 2. Transformar datos (Power Query Editor)
echo.
echo 3. Cargar cada consulta (Nueva consulta ^> Consulta en blanco ^> Editor avanzado):
echo    - Presupuesto_Equipo1.pq -^> nombre: Presupuesto_Equipo1
echo    - Presupuesto_Equipo2.pq -^> nombre: Presupuesto_Equipo2  
echo    - Ejecucion.pq -^> nombre: ejecucion
echo    - Presupuesto_Append.pq -^> nombre: presupuesto_col
echo.
echo 4. Cerrar y aplicar
echo.
echo 5. Modelado ^> Nueva tabla (pega cada DAX):
echo    - DateTable.dax -^> DimPeriodo
echo    - DimTipoGasto.dax -^> DimTipoGasto
echo    - DimEquipo.dax -^> DimEquipo
echo.
echo 6. Vista Modelo: Crear relaciones arrastrando:
echo    - DimPeriodo[Periodo] -^> presupuesto_col[Periodo]
echo    - DimPeriodo[Periodo] -^> ejecucion[Periodo]
echo    - DimTipoGasto[Tipo de gasto] -^> presupuesto_col[Tipo de gasto]
echo    - DimTipoGasto[Tipo de gasto] -^> ejecucion[Tipo de gasto]
echo    - DimEquipo[Equipo] -^> presupuesto_col[Equipo]
echo    - DimEquipo[Equipo] -^> ejecucion[Equipo]
echo.
echo 7. Modelado ^> Nueva medida (pega las 8 medidas de Measures_presupuesto_col.dax)
echo.
echo 8. Crear visuales:
echo    - Slicers: Anio, Tipo de gasto, Equipo
echo    - Tarjetas: Monto Presupuestado (Anio), Ejecutado (Anio), Variacion (Anio)
echo    - Grafico columnas: Eje=Mes, Valores=Presupuestado/Ejecutado
echo    - Matriz: Filas=Equipo, Valores=Presupuestado/Ejecutado/Variacion/Variacion%%
echo.
echo 9. Guardar como: PresupuestoAnalisis.pbix
echo.
echo ============================================================
echo.
echo Presiona cualquier tecla para abrir Power BI Desktop...
pause >nul

start "" "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"

echo.
echo Power BI Desktop abierto. Sigue los pasos de arriba.
echo.
echo Todos los archivos estan en: %~dp0powerbi\
echo.
pause
