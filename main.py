import copy
import json
from pathlib import Path
from typing import Any

import extractor
import analizador
import analista_ia


CONFIG_PATH = Path("config.json")

DEFAULT_CONFIG = {
    "google_drive": {
        "credentials_file": "credenciales.json",
        "document_name": "Tesoreria",
        "sheets_to_extract": [
            "20,21,22",
            "23,24,25",
            "26,27,28",
            "Anual",
        ],
    },
    "database": {
        "db_name": "archivos_finanzas.db",
        "table_prefix": "raw_",
    },
    "output": {
        "json_consolidated": "tesoreria_consolidada.json",
        "ia_report": "informe_financiero.txt",
    },
}


def fusionar_configuracion(
    configuracion_base: dict[str, Any],
    configuracion_personalizada: dict[str, Any],
) -> dict[str, Any]:
    """Combina la configuración personalizada con los valores por defecto."""
    configuracion = copy.deepcopy(configuracion_base)

    for seccion, valores in configuracion_personalizada.items():
        if isinstance(valores, dict) and isinstance(configuracion.get(seccion), dict):
            configuracion[seccion].update(valores)
        else:
            configuracion[seccion] = valores

    return configuracion


def guardar_configuracion_por_defecto(ruta_config: Path) -> None:
    """Guarda la configuración inicial si es posible."""
    try:
        with ruta_config.open("w", encoding="utf-8") as archivo:
            json.dump(DEFAULT_CONFIG, archivo, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"⚠ Error al guardar la configuración por defecto: {error}")


def cargar_configuracion(ruta_config: Path = CONFIG_PATH) -> dict[str, Any]:
    """Carga la configuración y completa las claves ausentes con valores por defecto."""
    if not ruta_config.exists():
        print(
            f"⚠ No se encontró '{ruta_config.name}'. "
            "Creando configuración por defecto..."
        )
        guardar_configuracion_por_defecto(ruta_config)
        return copy.deepcopy(DEFAULT_CONFIG)

    try:
        with ruta_config.open("r", encoding="utf-8") as archivo:
            configuracion_personalizada = json.load(archivo)

        if not isinstance(configuracion_personalizada, dict):
            raise ValueError("La configuración debe contener un objeto JSON.")

        return fusionar_configuracion(DEFAULT_CONFIG, configuracion_personalizada)

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(
            f"⚠ Error al leer '{ruta_config.name}': {error}. "
            "Usando configuración por defecto."
        )
        return copy.deepcopy(DEFAULT_CONFIG)


def mostrar_encabezado(config: dict[str, Any]) -> None:
    """Imprime el menú principal en la consola."""
    doc_name = config["google_drive"]["document_name"]
    db_file = config["database"]["db_name"]

    print("\n=========================================")
    print("   MOTOR ETL UNIVERSAL - MULTI-DRIVE")
    print("=========================================")
    print(f" Archivo objetivo: {doc_name}")
    print(f" BD Destino:      {db_file}")
    print("-----------------------------------------")
    print("1) Extraer")
    print("2) Analizar (JSON)")
    print("3) Flujo completo")
    print("4) Análisis IA")
    print("5) Salir")


def pausar_menu() -> None:
    """Pausa el menú sin generar errores si la entrada se interrumpe."""
    try:
        input("\n⌨ Presiona INTRO para volver...")
    except (EOFError, KeyboardInterrupt):
        print()


def ejecutar_opcion(opcion: str, config: dict[str, Any]) -> bool:
    """
    Ejecuta una opción del menú.

    Devuelve False cuando se debe salir del programa y True cuando
    se debe continuar mostrando el menú.
    """
    db_file = Path(config["database"]["db_name"])
    json_file = Path(config["output"]["json_consolidated"])

    if opcion == "1":
        extractor.ejecutar_pipeline_extraccion(config)

    elif opcion == "2":
        if not db_file.exists():
            print(
                f"⚠ Error: La base de datos '{db_file}' no existe. "
                "Ejecuta extracción primero."
            )
        else:
            analizador.ejecutar_analisis_historico(config)

    elif opcion == "3":
        extractor.ejecutar_pipeline_extraccion(config)
        analizador.ejecutar_analisis_historico(config)

    elif opcion == "4":
        if not json_file.exists():
            print(
                f"⚠ Error: El archivo '{json_file}' no existe. "
                "Ejecuta primero la opción 2 o 3."
            )
        else:
            analista_ia.generar_analisis_ia(config)

    elif opcion == "5":
        print("👋 Saliendo del sistema ETL...")
        return False

    else:
        print("⚠ Opción no válida. Selecciona una opción entre 1 y 5.")

    return True


def main() -> None:
    config = cargar_configuracion()

    while True:
        mostrar_encabezado(config)

        try:
            opcion = input("👉 Opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Saliendo del sistema ETL...")
            break

        try:
            continuar = ejecutar_opcion(opcion, config)
        except Exception as error:
            print(f"❌ Se produjo un error durante la operación: {error}")

        else:
            if not continuar:
                break

        if opcion != "5":
            pausar_menu()


if __name__ == "__main__":
    main()