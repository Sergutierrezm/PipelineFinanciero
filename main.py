# main.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pathlib import Path

# Permisos para conectar con Google
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

print("⏳ Iniciando el Pipeline Financiero...")


def extraer_datos_sheets(nombre_documento, nombre_pestaña):
    """Se conecta a Google Sheets y descarga los datos en un DataFrame."""
    ruta_json = Path("credenciales.json")
    
    if not ruta_json.exists():
        print("❌ Error: No se encuentra el archivo 'credenciales.json'.")
        return None
        
    try:
        credenciales = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, SCOPES)
        cliente = gspread.authorize(credenciales)
        print("🔒 Conexión segura con Google Cloud: ESTABLECIDA")
        
        documento = cliente.open(nombre_documento)
        hoja = documento.worksheet(nombre_pestaña)
        registros = hoja.get_all_records()
        
        if not registros:
            print("⚠ La pestaña está vacía.")
            return pd.DataFrame()
            
        df = pd.DataFrame(registros)
        print(f"📥 ¡Éxito! Se han descargado {len(df)} filas desde la nube.")
        return df
        
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Error: No se encontró el documento '{nombre_documento}'.")
        return None
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ Error: No se encontró la pestaña '{nombre_pestaña}'.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado en extracción: {e}")
        return None


def transformar_y_limpiar_datos(df):
    """Limpia los datos en bruto para poder operar matemáticamente."""
    df_limpio = df.copy()
    print("\n⚙ Iniciando limpieza de datos (Transform)...")
    
    # Pasamos a texto para manipular los caracteres
    df_limpio['CAPITAL Total'] = df_limpio['CAPITAL Total'].astype(str)
    
    # Limpieza de strings (Símbolos, espacios, puntos y comas)
    df_limpio['CAPITAL Total'] = df_limpio['CAPITAL Total'].str.replace('€', '', regex=False).str.strip()
    df_limpio['CAPITAL Total'] = df_limpio['CAPITAL Total'].str.replace('.', '', regex=False)
    df_limpio['CAPITAL Total'] = df_limpio['CAPITAL Total'].str.replace(',', '.', regex=False)
    
    # Conversión final a número decimal
    df_limpio['CAPITAL Total'] = pd.to_numeric(df_limpio['CAPITAL Total'], errors='coerce')
    
    print("✅ Transformación completada. Columna 'CAPITAL Total' convertida a número.")
    return df_limpio


def analizar_capital(df):
    """Realiza cálculos estadísticos y análisis sobre el capital limpio."""
    print("\n📊 --- ANALÍTICA DE DATOS ---")
    
    # Calculamos la diferencia neta año a año
    df['Crecimiento Anual'] = df['CAPITAL Total'].diff()
    
    # Calculamos el porcentaje de variación anual
    df['% Variación'] = df['CAPITAL Total'].pct_change() * 100
    
    # Mostramos la tabla formateada por consola sin índices feos
    print(df.to_string(index=False, formatters={
        'CAPITAL Total': '{:,.2f}€'.format,
        'Crecimiento Anual': '{:+,.2f}€'.format,
        '% Variación': '{:+.2f}%'.format
    }))


# --- BLOQUE PRINCIPAL DE EJECUCIÓN ---
if __name__ == "__main__":
    MI_DOCUMENTO = "Tesoreria"  
    MI_PESTAÑA = "Anual"                   
    
    # 1. Ejecutamos la Extracción
    df_bruto = extraer_datos_sheets(MI_DOCUMENTO, MI_PESTAÑA)
    
    if df_bruto is not None and not df_bruto.empty:
        # 2. Ejecutamos la Transformación
        df_procesado = transformar_y_limpiar_datos(df_bruto)
        
        # 3. Ejecutamos el Análisis
        analizar_capital(df_procesado)