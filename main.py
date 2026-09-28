import json
from pathlib import Path

import extractor
import analizador
import analista_ia

CONFIG_PATH = Path("config.json")

DEFAULT_CONFIG = {
    "google_drive": {
        "credentials_file": "credenciales.json",
        "document_name": "Tesoreria",
        "sheets_to_extract": ["20,21,22", "23,24,25", "26,27,28", "Anual"]
    },
    "database": {
        "db_name": "archivos_finanzas.db",
        "table_prefix": "raw_"
    },
    "output": {
        "json_consolidated": "tesoreria_consolidada.json",
        "ia_report": "informe_financiero.txt"
    }
}


def cargar_configuracion(ruta_config: Path = CONFIG_PATH) -> dict:
    """Carga la configuración desde un archivo JSON o genera una por defecto."""
    if not ruta_config.exists():
        print(f"⚠ No se encontró '{ruta_config.name}'. Creando configuración por defecto...")
        try:
            with open(ruta_config, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except OSError as error:
            print(f"⚠ Error al guardar la configuración por defecto: {error}")
        return DEFAULT_CONFIG

    try:
        with open(ruta_config, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as error:
        print(f"⚠ Error al leer '{ruta_config.name}': {error}. Usando configuración por defecto.")
        return DEFAULT_CONFIG


def mostrar_encabezado(doc_name: str, db_file: str) -> None:
    """Imprime el menú principal en la consola."""
    print("\n=========================================")
    print("   MOTOR ETL UNIVERSAL - MULTI-DRIVE")
    print("=========================================")
    print(f" Archivo objetivo: {doc_name}")
    print(f" BD Destino:      {db_file}")
    print("-----------------------------------------")
    print("1) Extraer | 2) Analizar (JSON) | 3) Flujo Completo | 4) Análisis IA | 5) Salir")


def main() -> None:
    config = cargar_configuracion()
    db_file = config["database"]["db_name"]
    doc_name = config["google_drive"]["document_name"]

    while True:
        mostrar_encabezado(doc_name, db_file)
        opcion = input("👉 Opción: ").strip()

        if opcion == "1":
            extractor.ejecutar_pipeline_extraccion(config)

        elif opcion == "2":
            if Path(db_file).exists():
                analizador.ejecutar_analisis_historico(config)
            else:
                print(f"⚠ Error: La base de datos '{db_file}' no existe. Ejecuta extracción primero.")

        elif opcion == "3":
            extractor.ejecutar_pipeline_extraccion(config)
            analizador.ejecutar_analisis_historico(config)

        elif opcion == "4":
            analista_ia.generar_analisis_ia(config)

        elif opcion == "5":
            print("👋 Saliendo del sistema ETL...")
            break

        else:
            print("⚠ Opción no válida. Por favor, selecciona una opción entre 1 y 5.")

        input("\n⌨ Presiona INTRO para volver...")


if __name__ == "__main__":
    main()