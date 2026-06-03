from extractor import ejecutar_pipeline_extraccion
from analizador import ejecutar_analisis_historico
from pathlib import Path

def main():
    while True:
        print("\n=========================================\n   MOTOR ETL - TESORERÍA SERGIO\n=========================================")
        print("1) Extraer | 2) Analizar (JSON) | 3) Flujo Completo | 4) Análisis IA | 5) Salir")
        opcion = input("👉 Opción: ")
        
        if opcion == "1": ejecutar_pipeline_extraccion()
        elif opcion == "2":
            if Path("archivos_finanzas.db").exists(): ejecutar_analisis_historico()
            else: print("⚠ Error: Ejecuta extracción primero.")
        elif opcion == "3":
            ejecutar_pipeline_extraccion()
            ejecutar_analisis_historico()
        elif opcion == "4":
            import analista_ia
            analista_ia.generar_analisis_ia()
        elif opcion == "5": break
        input("\n⌨ Presiona INTRO para volver...")

if __name__ == "__main__":
    main()