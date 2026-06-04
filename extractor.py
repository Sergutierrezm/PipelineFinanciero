import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pathlib import Path
import sqlite3

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def conectar_y_descargar_sheet(ruta_json, nombre_documento, nombre_pestaña):
    """Extrae datos de cualquier pestaña y cualquier archivo JSON de credenciales."""
    ruta = Path(ruta_json)
    if not ruta.exists():
        print(f"❌ Error: No se encuentra el archivo de credenciales '{ruta.name}'")
        return None
    try:
        credenciales = ServiceAccountCredentials.from_json_keyfile_name(ruta, SCOPES)
        cliente = gspread.authorize(credenciales)
        datos_crudos = cliente.open(nombre_documento).worksheet(nombre_pestaña).get_all_values()
        
        if not datos_crudos:
            return pd.DataFrame()
            
        df = pd.DataFrame(datos_crudos)
        print(f"📥 [EXTRACT] -> '{nombre_pestaña}' descargada en bruto ({len(df)} filas).")
        return df
    except Exception as e:
        print(f"❌ Error al extraer [{nombre_pestaña}]: {e}")
        return None

def ejecutar_pipeline_extraccion(config):
    print("⏳ Iniciando el Motor Genérico y Agnóstico de Extracción...")
    
    # Extraemos las variables desde el objeto config de manera dinámica
    ruta_credenciales = config["google_drive"]["credentials_file"]
    documento = config["google_drive"]["document_name"]
    pestañas = config["google_drive"]["sheets_to_extract"]
    db_nombre = config["database"]["db_name"]
    prefijo = config["database"]["table_prefix"]
    
    conexion = sqlite3.connect(db_nombre)
    for pestaña in pestañas:
        df_raw = conectar_y_descargar_sheet(ruta_credenciales, documento, pestaña)
        if df_raw is not None and not df_raw.empty:
            # Reemplazamos caracteres conflictivos para nombres de tablas SQL
            nombre_tabla = f"{prefijo}{pestaña.replace(',', '_').replace(' ', '_')}"
            df_raw.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            print(f"💾 [LOAD] -> Guardada tabla local: '{nombre_tabla}'")
    conexion.close()
    print("🏁 [EXTRACTOR] Datos en bruto guardados localmente.")