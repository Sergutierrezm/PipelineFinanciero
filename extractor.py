# extractor.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pathlib import Path
import sqlite3

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def conectar_y_descargar_sheet(nombre_documento, nombre_pestaña):
    """Extrae absolutamente todo lo que haya en la pestaña en bruto, sin filtros."""
    ruta_json = Path("credenciales.json")
    if not ruta_json.exists():
        print(f"❌ Error: No se encuentra '{ruta_json.name}'")
        return None
    try:
        credenciales = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, SCOPES)
        cliente = gspread.authorize(credenciales)
        datos_crudos = cliente.open(nombre_documento).worksheet(nombre_pestaña).get_all_values()
        
        if not datos_crudos:
            return pd.DataFrame()
            
        # Creamos un DataFrame plano. Usamos columnas genéricas (Col_0, Col_1...) 
        # para que NADA en la estructura del Excel pueda romper la extracción.
        df = pd.DataFrame(datos_crudos)
        print(f"📥 [EXTRACT] -> '{nombre_pestaña}' descargada en bruto ({len(df)} filas).")
        return df
    except Exception as e:
        print(f"❌ Error al extraer [{nombre_pestaña}]: {e}")
        return None

def ejecutar_pipeline_extraccion():
    print("⏳ Iniciando el Motor Genérico y Agnóstico de Extracción...")
    DOCUMENTO = "Tesoreria"
    PESTAÑAS = ["20,21,22", "23,24,25", "26,27,28", "Anual"]
    
    conexion = sqlite3.connect("archivos_finanzas.db")
    for pestaña in PESTAÑAS:
        df_raw = conectar_y_descargar_sheet(DOCUMENTO, pestaña)
        if df_raw is not None and not df_raw.empty:
            # Se guarda la matriz tal cual está en la nube
            nombre_tabla = f"raw_{pestaña.replace(',', '_')}"
            df_raw.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            print(f"💾 [LOAD] -> Guardada tabla local: '{nombre_tabla}'")
    conexion.close()
    print("🏁 [EXTRACTOR] Datos en bruto guardados localmente.")

if __name__ == "__main__":
    ejecutar_pipeline_extraccion()