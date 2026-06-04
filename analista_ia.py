import json
import ollama

def generar_analisis_ia(config): # 👈 Añadimos 'config' aquí
    # 1. Cargamos tu fuente de verdad de manera dinámica usando la configuración
    archivo_json = config["output"]["json_consolidated"]
    archivo_informe = config["output"]["ia_report"]
    
    try:
        with open(archivo_json, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Primero debes ejecutar la opción 2 para generar el archivo '{archivo_json}'.")
        return

    # 2. Preparamos el contexto para Ollama
    contexto = json.dumps(datos, ensure_ascii=False)
    
    # 3. Prompt estructurado optimizado para Llama 3.2
    prompt = f"""
    Actúa como un experto asesor financiero personal.
    Analiza el siguiente JSON que contiene el histórico de mi tesorería (organizado por tablas de años y conceptos con sus matrices de datos numéricos):
    
    {contexto}
    
    Por favor, genera tu informe estructurado exactamente con estos puntos:
    ### 1. Evolución del Capital
    (Resume la tendencia año tras año)
    
    ### 2. Estacionalidad del Ahorro
    (Detecta qué meses o periodos muestran picos de ahorro o gasto)
    
    ### 3. Plan de Acción (3 Consejos)
    (Dame 3 pautas críticas basadas exclusivamente en mis datos para mejorar)
    
    Sé directo, conciso, estricto con los números y usa un tono profesional pero motivador.
    """

    print("🧠 [ANALISTA AI] Procesando tus datos financieros...")
    
    try:
        # 4. Llamada al cerebro local
        respuesta = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': prompt}
        ])

        # 5. Resultado
        analisis = respuesta['message']['content']
        
        print("\n--- INFORME FINANCIERO IA ---\n")
        print(analisis)
        
        # Guardamos el informe dinámicamente en la ruta configurada
        with open(archivo_informe, "w", encoding="utf-8") as f:
            f.write(analisis)
        print(f"\n💾 Informe guardado en '{archivo_informe}'")
        
    except Exception as e:
        print(f"❌ Error al conectar con Ollama: {e}")
        print("Asegúrate de que la aplicación de Ollama esté abierta y el modelo 'llama3.2:3b' descargado.")

# Modificamos el bloque final por si ejecutas este script suelto para pruebas
if __name__ == "__main__":
    # Configuración de pruebas por si se ejecuta solo
    config_prueba = {
        "output": {
            "json_consolidated": "tesoreria_consolidada.json",
            "ia_report": "informe_financiero.txt"
        }
    }
    generar_analisis_ia(config_prueba)