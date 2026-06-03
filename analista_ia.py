import json
import ollama

def generar_analisis_ia():
    # 1. Cargamos tu fuente de verdad
    try:
        with open("tesoreria_consolidada.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        print("❌ Error: Primero debes ejecutar la opción 2 para generar el JSON.")
        return

    # 2. Preparamos el contexto para Ollama
    contexto = json.dumps(datos, ensure_ascii=False)
    
    prompt = f"""
    Actúa como un experto asesor financiero personal.
    Analiza los siguientes datos de mi tesorería (JSON):
    {contexto}
    
    Por favor:
    1. Identifica la tendencia de mi capital total año tras año.
    2. Detecta en qué meses suelo tener mayor ahorro.
    3. Dame 3 consejos concretos para mejorar mi salud financiera basándote en mi historial.
    4. Sé directo, breve y utiliza un tono motivador.
    """

    print("🧠 [ANALISTA AI] Procesando tus datos financieros...")
    
    # 3. Llamada al cerebro
    respuesta = ollama.chat(model='llama3.2:3b', messages=[
        {'role': 'user', 'content': prompt}
    ])

    # 4. Resultado
    analisis = respuesta['message']['content']
    
    print("\n--- INFORME FINANCIERO IA ---\n")
    print(analisis)
    
    # Guardamos el informe por si lo quieres leer luego
    with open("informe_financiero.txt", "w", encoding="utf-8") as f:
        f.write(analisis)
    print("\n💾 Informe guardado en 'informe_financiero.txt'")

if __name__ == "__main__":
    generar_analisis_ia()