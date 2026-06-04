import json
from pathlib import Path
import extractor
import analizador

def cargar_configuracion():
    ruta_config = Path("config.json")
    if not ruta_config.exists():
        # Configuración por defecto si el archivo no existe
        print("⚠ No se encontró 'config.json'. Creando uno por defecto...")
        default_config = {
            "google_drive": {
                "credentials_file": "credenciales.json",
                "document_name": "Tesoreria",
                "sheets_to_extract": ["20,21,22", "23,24,25", "26,27,28", "Anual"]
            },
            "database": {"db_name": "archivos_finanzas.db", "table_prefix": "raw_"},
            "output": {"json_consolidated": "tesoreria_consolidada.json", "ia_report": "informe_financiero.txt"}
        }
        with open(ruta_config, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        return default_config
        
    with open(ruta_config, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = cargar_configuracion()
    db_file = config["database"]["db_name"]

    while True:
        print("\n=========================================\n   MOTOR ETL UNIVERSAL - MULTI-DRIVE\n=========================================")
        print(f" Archivo objetivo: {config['google_drive']['document_name']}")
        print(f" BD Destino:      {db_file}")
        print("-----------------------------------------")
        print("1) Extraer | 2) Analizar (JSON) | 3) Flujo Completo | 4) Análisis IA | 5) Salir")
        opcion = input("👉 Opción: ")
        
        if opcion == "1": 
            extractor.ejecutar_pipeline_extraccion(config)
        elif opcion == "2":
            if Path(db_file).exists(): 
                analizador.ejecutar_analisis_historico(config)
            else: 
                print(f"⚠ Error: La base de datos {db_file} no existe. Ejecuta extracción primero.")
        elif opcion == "3":
            extractor.ejecutar_pipeline_extraccion(config)
            analizador.ejecutar_analisis_historico(config)
        elif opcion == "4":
            # Aquí pasarías config también a tu analista_ia para que sepa qué JSON leer
            import analista_ia
            analista_ia.generar_analisis_ia(config)
        elif opcion == "5": 
            break
        input("\n⌨ Presiona INTRO para volver...")

if __name__ == "__main__":
    main()