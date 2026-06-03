import sqlite3
import pandas as pd
import json

def limpiar_valor(celda):
    if celda is None or str(celda).strip() in ["", "none", "None"]: return None
    texto = str(celda).strip()
    if any(caracter.isalpha() for caracter in texto) and '€' not in texto: return texto
    limpio = texto.replace('€', '').replace(' ', '').strip().replace(',', '.')
    try:
        num = float(limpio)
        return int(num) if num.is_integer() else num
    except: return texto

def procesar_pestaña_en_bruto(df_raw):
    filas_procesadas = []
    for _, fila in df_raw.iterrows():
        valores = [limpiar_valor(c) for c in fila if limpiar_valor(c) is not None]
        if valores:
            filas_procesadas.append({'CONCEPTO': str(valores[0]), 'DATOS': valores[1:]})
    return pd.DataFrame(filas_procesadas)

def ejecutar_analisis_historico():
    conexion = sqlite3.connect("archivos_finanzas.db")
    tablas = [f[0] for f in conexion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'raw_%'")]
    reporte_maestro = {}
    for tabla in tablas:
        df_raw = pd.read_sql(f"SELECT * FROM {tabla}", conexion)
        if not df_raw.empty:
            df_informe = procesar_pestaña_en_bruto(df_raw)
            reporte_maestro[tabla] = df_informe.to_dict(orient='records')
            print(f"✅ Procesada {tabla}")
    
    with open("tesoreria_consolidada.json", "w", encoding="utf-8") as f:
        json.dump(reporte_maestro, f, indent=4, ensure_ascii=False)
    print("\n💾 [ÉXITO] Datos guardados en 'tesoreria_consolidada.json'")
    conexion.close()