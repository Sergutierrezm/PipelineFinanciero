# 📊 PipelineFinanciero: Motor ETL Universal & Analista IA

Pipeline de datos **ETL** (Extract, Transform, Load) desarrollado en Python. Está diseñado como un motor genérico multi-drive que extrae registros financieros estructurados desde Google Sheets (Tesorería), procesa y limpia los datos en bruto en una base de datos local y genera tanto análisis visuales de evolución patrimonial como informes financieros automatizados mediante Inteligencia Artificial.

---

### ⚙️ Arquitectura del Pipeline

El sistema está completamente modularizado para respetar el ciclo de vida clásico de un flujo de datos:

* **`main.py`:** Orquestador principal de la aplicación. Levanta una interfaz interactiva por consola y gestiona la configuración dinámica del sistema.
* **`extractor.py` (Extract & Load RAW):** Conecta con la API de Google Drive/Sheets mediante credenciales seguras, extrae las hojas configuradas de forma asíncrona y vuelca el histórico en bruto en SQLite.
* **`analizador.py` (Transform & Consolidate):** Se encarga de la limpieza de datos, tipado, unificación de registros, exportación a un JSON consolidado y la generación del gráfico estadístico de evolución (`evolucion_capital.png`).
* **`analista_ia.py` (AI Insights):** Consume el JSON consolidado y procesa las métricas financieras mediante modelos de lenguaje (IA) para redactar un informe de salud financiera estratégico (`informe_financiero.txt`).

---

### 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Ecosistema de Datos:** Pandas, SQLite3, JSON, PyYAML
* **Integraciones externas:** Google Drive API & Google Sheets API
* **Automatización:** Motores de IA generativa (Análisis semántico e insights financieros)

---

### 📦 Estructura de Configuración (`config.json`)

El pipeline se autogestiona mediante un archivo de configuración que mapea el entorno del Drive objetivo, las hojas de cálculo a consolidar y las salidas del sistema:

```json
{
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
```


---

### 🚀 Modo de Uso
Instala las dependencias necesarias y asegúrate de tener tu archivo credenciales.json de Google Cloud en la raíz del proyecto.

Ejecuta el orquestador principal:

Bash
python main.py
Selecciona una opción del menú interactivo:

* **1 Extraer: Descarga y vuelca las hojas de cálculo crudas en la base de datos SQLite.

* **2 Analizar (JSON): Limpia la base de datos, unifica criterios y genera el JSON y el gráfico de evolución de capital.

* **3 Flujo Completo: Ejecuta todo el ciclo ETL en un solo comando de forma secuencial.

* **4 Análisis IA: Ejecuta el agente inteligente para auditar el JSON consolidado y generar las conclusiones financieras en texto plano.


---

### 💡 ¿Por qué está enfocado así?
* **Usa tus propios términos:** He rescatado los nombres exactos de tus scripts (`extractor`, `analizador`, `analista_ia`) y el esquema del `config.json` que venía en tu código para que el README encaje a la perfección.
* **Le da caché al proyecto:** En lugar de decir simplemente "lee un excel", usamos términos de industria como *Pipeline ETL*, *Multi-drive*, *Consolidación de datos* e *IA Insights*, que es lo que busca leer cualquier reclutador o Tech Lead.



