import sqlite3
import pandas as pd
import json

def limpiar_valor(celda):
    if celda is None or str(celda).strip() in ["", "none", "None", "-"]: 
        return None
    texto = str(celda).strip()
    limpio = texto.replace('€', '').replace(' ', '').replace(',', '.').strip()
    try:
        num = float(limpio)
        return int(num) if num.is_integer() else num
    except ValueError:
        return texto

def procesar_pestaña_en_bruto(df_raw):
    filas_procesadas = []
    for _, fila in df_raw.iterrows():
        valores_limpios = [limpiar_valor(c) for c in fila]
        concepto = next((v for v in valores_limpios if isinstance(v, str)), None)
        
        if concepto:
            # Si el concepto existe, agrupamos el resto de valores numéricos de la fila
            datos = [v if v is not None else 0 for v in valores_limpios if v != concepto]
            filas_procesadas.append({'CONCEPTO': concepto, 'DATOS': datos})
    return pd.DataFrame(filas_procesadas)

def ejecutar_analisis_historico(config):
    db_nombre = config["database"]["db_name"]
    prefijo = config["database"]["table_prefix"]
    archivo_salida = config["output"]["json_consolidated"]

    conexion = sqlite3.connect(db_nombre)
    # Buscamos dinámicamente las tablas que empiecen por el prefijo configurado
    tablas = [f[0] for f in conexion.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{prefijo}%'")]
    
    reporte_maestro = {}
    for tabla in tablas:
        df_raw = pd.read_sql(f"SELECT * FROM {tabla}", conexion)
        if not df_raw.empty:
            df_informe = procesar_pestaña_en_bruto(df_raw)
            reporte_maestro[tabla] = df_informe.to_dict(orient='records')
            print(f"✅ Procesada {tabla}")
    
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(reporte_maestro, f, indent=4, ensure_ascii=False)
    print(f"\n💾 [ÉXITO] Datos guardados en '{archivo_salida}'")
    conexion.close()