# Script para crear un proyecto PbixProj y compilarlo a PBIX usando pbi-tools
# Requiere: pbi-tools instalado (https://pbi.tools/)
# Uso: python create_pbix.py

import json
import os
from pathlib import Path
import subprocess
import shutil

# Rutas
BASE_DIR = Path(r"c:\Users\USER\Desktop\Prueba")
PBIXPROJ_DIR = BASE_DIR / "PresupuestoAnalisis.PbixProj"
QUERIES_DIR = BASE_DIR / "powerbi" / "queries"
MODELING_DIR = BASE_DIR / "powerbi" / "modeling"
MEASURES_DIR = BASE_DIR / "powerbi" / "measures"

def create_pbixproj_structure():
    """Crea la estructura de carpetas PbixProj"""
    print("📁 Creando estructura PbixProj...")
    
    # Crear directorios principales
    (PBIXPROJ_DIR / "Model").mkdir(parents=True, exist_ok=True)
    (PBIXPROJ_DIR / "Report").mkdir(parents=True, exist_ok=True)
    
    # Crear .pbixproj.json (manifiesto del proyecto)
    manifest = {
        "version": "0.18",
        "created": "2023-01-01T00:00:00",
        "lastModified": "2023-12-31T23:59:59"
    }
    
    with open(PBIXPROJ_DIR / ".pbixproj.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Estructura creada en: {PBIXPROJ_DIR}")

def create_model_bim():
    """Crea el archivo Model/database.bim con tablas y medidas"""
    print("📊 Generando modelo de datos (BIM)...")
    
    # Leer las medidas DAX
    measures_file = MEASURES_DIR / "Measures_presupuesto_col.dax"
    with open(measures_file, "r", encoding="utf-8") as f:
        measures_dax = f.read()
    
    # Parsear las medidas (simplificado)
    measures = []
    for line in measures_dax.split("\n"):
        if " = " in line and not line.strip().startswith("--"):
            parts = line.split(" = ", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                expression = parts[1].strip()
                measures.append({
                    "name": name,
                    "expression": expression
                })
    
    # Modelo BIM básico
    bim_model = {
        "name": "PresupuestoAnalisis",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "es-CO",
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "presupuesto_col",
                    "columns": [
                        {"name": "Tipo de gasto", "dataType": "string"},
                        {"name": "Mes", "dataType": "string"},
                        {"name": "MesNumero", "dataType": "int64"},
                        {"name": "Año", "dataType": "int64"},
                        {"name": "Equipo", "dataType": "string"},
                        {"name": "Periodo", "dataType": "dateTime"},
                        {"name": "Monto Presupuestado", "dataType": "double"}
                    ],
                    "partitions": [
                        {
                            "name": "presupuesto_col",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": "let Source = presupuesto_col in Source"
                            }
                        }
                    ]
                },
                {
                    "name": "ejecucion",
                    "columns": [
                        {"name": "Tipo de gasto", "dataType": "string"},
                        {"name": "Mes", "dataType": "string"},
                        {"name": "MesNumero", "dataType": "int64"},
                        {"name": "Año", "dataType": "int64"},
                        {"name": "Equipo", "dataType": "string"},
                        {"name": "Periodo", "dataType": "dateTime"},
                        {"name": "Fe.contabilización", "dataType": "dateTime"},
                        {"name": "Monto Ejecutado", "dataType": "double"}
                    ],
                    "partitions": [
                        {
                            "name": "ejecucion",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": "let Source = ejecucion in Source"
                            }
                        }
                    ]
                },
                {
                    "name": "DimPeriodo",
                    "columns": [
                        {"name": "Periodo", "dataType": "dateTime"},
                        {"name": "Año", "dataType": "int64"},
                        {"name": "MesNumero", "dataType": "int64"},
                        {"name": "Mes", "dataType": "string"}
                    ],
                    "partitions": [
                        {
                            "name": "DimPeriodo",
                            "mode": "import",
                            "source": {
                                "type": "calculated",
                                "expression": open(MODELING_DIR / "DateTable.dax", "r", encoding="utf-8").read()
                            }
                        }
                    ]
                },
                {
                    "name": "DimTipoGasto",
                    "columns": [
                        {"name": "Tipo de gasto", "dataType": "string"}
                    ],
                    "partitions": [
                        {
                            "name": "DimTipoGasto",
                            "mode": "import",
                            "source": {
                                "type": "calculated",
                                "expression": open(MODELING_DIR / "DimTipoGasto.dax", "r", encoding="utf-8").read()
                            }
                        }
                    ]
                },
                {
                    "name": "DimEquipo",
                    "columns": [
                        {"name": "Equipo", "dataType": "string"}
                    ],
                    "partitions": [
                        {
                            "name": "DimEquipo",
                            "mode": "import",
                            "source": {
                                "type": "calculated",
                                "expression": open(MODELING_DIR / "DimEquipo.dax", "r", encoding="utf-8").read()
                            }
                        }
                    ]
                },
                {
                    "name": "Measures",
                    "measures": measures
                }
            ],
            "relationships": [
                {
                    "name": "DimPeriodo-presupuesto_col",
                    "fromTable": "presupuesto_col",
                    "fromColumn": "Periodo",
                    "toTable": "DimPeriodo",
                    "toColumn": "Periodo"
                },
                {
                    "name": "DimPeriodo-ejecucion",
                    "fromTable": "ejecucion",
                    "fromColumn": "Periodo",
                    "toTable": "DimPeriodo",
                    "toColumn": "Periodo"
                },
                {
                    "name": "DimTipoGasto-presupuesto_col",
                    "fromTable": "presupuesto_col",
                    "fromColumn": "Tipo de gasto",
                    "toTable": "DimTipoGasto",
                    "toColumn": "Tipo de gasto"
                },
                {
                    "name": "DimTipoGasto-ejecucion",
                    "fromTable": "ejecucion",
                    "fromColumn": "Tipo de gasto",
                    "toTable": "DimTipoGasto",
                    "toColumn": "Tipo de gasto"
                },
                {
                    "name": "DimEquipo-presupuesto_col",
                    "fromTable": "presupuesto_col",
                    "fromColumn": "Equipo",
                    "toTable": "DimEquipo",
                    "toColumn": "Equipo"
                },
                {
                    "name": "DimEquipo-ejecucion",
                    "fromTable": "ejecucion",
                    "fromColumn": "Equipo",
                    "toTable": "DimEquipo",
                    "toColumn": "Equipo"
                }
            ]
        }
    }
    
    with open(PBIXPROJ_DIR / "Model" / "database.bim", "w", encoding="utf-8") as f:
        json.dump(bim_model, f, indent=2, ensure_ascii=False)
    
    print("✅ Modelo BIM creado")

def create_mashup():
    """Crea el archivo Mashup con las consultas Power Query"""
    print("🔄 Generando Mashup (Power Query)...")
    
    # Leer consultas
    queries = {}
    for pq_file in QUERIES_DIR.glob("*.pq"):
        with open(pq_file, "r", encoding="utf-8") as f:
            queries[pq_file.stem] = f.read()
    
    # Crear Package/Formulas/Section1.m
    formulas_dir = PBIXPROJ_DIR / "Mashup" / "Package" / "Formulas"
    formulas_dir.mkdir(parents=True, exist_ok=True)
    
    section_m = "section Section1;\n\n"
    for name, code in queries.items():
        section_m += f"shared #{name} = {code};\n\n"
    
    with open(formulas_dir / "Section1.m", "w", encoding="utf-8") as f:
        f.write(section_m)
    
    print("✅ Mashup creado")

def create_report_layout():
    """Crea un layout básico del reporte"""
    print("📄 Generando layout del reporte...")
    
    # Layout JSON básico
    layout = {
        "config": json.dumps({
            "name": "Presupuesto vs Ejecución",
            "layouts": [{
                "id": 0,
                "displayName": "Page1",
                "visualContainers": []
            }]
        }, ensure_ascii=False)
    }
    
    with open(PBIXPROJ_DIR / "Report" / "layout", "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2, ensure_ascii=False)
    
    print("✅ Layout creado")

def compile_to_pbix():
    """Compila el PbixProj a PBIX usando pbi-tools"""
    print("\n🔨 Compilando a PBIX...")
    
    output_pbix = BASE_DIR / "PresupuestoAnalisis.pbix"
    
    try:
        result = subprocess.run(
            ["pbi-tools", "compile", str(PBIXPROJ_DIR), str(output_pbix), "-overwrite"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print(f"\n✅ PBIX creado exitosamente: {output_pbix}")
        return True
    except FileNotFoundError:
        print("\n❌ Error: pbi-tools no está instalado o no está en PATH")
        print("Descárgalo desde: https://pbi.tools/")
        print("\nAlternativamente, instala con:")
        print("  dotnet tool install -g pbi-tools")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al compilar: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    print("=" * 60)
    print("  GENERADOR DE PBIX - Presupuesto vs Ejecución")
    print("=" * 60)
    print()
    
    # Verificar que existan los archivos fuente
    if not QUERIES_DIR.exists():
        print(f"❌ Error: No se encuentra {QUERIES_DIR}")
        return
    
    # Crear estructura
    create_pbixproj_structure()
    create_model_bim()
    create_mashup()
    create_report_layout()
    
    # Compilar
    if compile_to_pbix():
        print("\n" + "=" * 60)
        print("  ✅ PROCESO COMPLETADO")
        print("=" * 60)
        print(f"\nAbre el archivo: {BASE_DIR / 'PresupuestoAnalisis.pbix'}")
        print("en Power BI Desktop para ver y editar el reporte.")
    else:
        print("\n" + "=" * 60)
        print("  ⚠️  PROYECTO CREADO, COMPILACIÓN PENDIENTE")
        print("=" * 60)
        print(f"\nCarpeta del proyecto: {PBIXPROJ_DIR}")
        print("\nPara compilar manualmente:")
        print(f'  pbi-tools compile "{PBIXPROJ_DIR}" "{BASE_DIR / "PresupuestoAnalisis.pbix"}" -overwrite')

if __name__ == "__main__":
    main()
