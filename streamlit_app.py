import pandas as pd
import streamlit as st
import altair as alt

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# ---------------------------------------------------------
st.set_page_config(page_title="Temperatura México", page_icon="🌡️")

st.title("🌡️ Predicción de temperatura en ciudades de México")
st.write("""
Esta aplicación te permite predecir la temperatura mensual estimada 
para diversas ciudades de México usando datos históricos.
""")

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
csv_path = "AmericaTemperaturesByCity.csv"

df = pd.read_csv(csv_path, encoding="latin-1")

st.subheader("Vista general de los datos")
st.write("Columnas detectadas en el CSV:")
st.write(list(df.columns))
st.dataframe(df.head(), hide_index=True)

# ---------------------------------------------------------
# DETECCIÓN AUTOMÁTICA DE COLUMNAS CLAVE
# ---------------------------------------------------------
def detectar_columna(df, posibles_subcadenas):
    for col in df.columns:
        cl = col.lower()
        for p in posibles_subcadenas:
            if p in cl:
                return col
    return None

CITY_COL = detectar_columna(df, ["city", "ciudad"])
MONTH_COL = detectar_columna(df, ["month", "mes"])
TEMP_COL = detectar_columna(df, ["temp", "temperatura"])

if CITY_COL is None or MONTH_COL is None or TEMP_COL is None:
    st.error(
        "No pude identificar automáticamente las columnas de **ciudad**, "
        "**mes** o **temperatura**.\n\n"
        "Revisa los nombres de las columnas que aparecen arriba y asegúrate "
        "de que alguna contenga palabras como 'city/ciudad', 'month/mes' o "
        "'temp/temperatura'."
    )
    st.stop()

st.success(
    f"Usando columnas:\n\n"
    f"- Ciudad: **{CITY_COL}**\n"
    f"- Mes: **{MONTH_COL}**\n"
    f"- Temperatura: **{TEMP_COL}**"
)

st.subheader("Vista simplificada de los datos relevantes")
st.dataframe(df[[CITY_COL, MONTH_COL, TEMP_COL]].head(), hide_index=True)

# ---------------------------------------------------------
# CONTROLES DE LA INTERFAZ
# ---------------------------------------------------------
st.sidebar.header("Parámetros de predicción")

# Aseguramos que mes sea numérico (por si viene como texto)
df[MONTH_COL] = pd.to_numeric(df[MONTH_COL], errors="coerce")

# Lista de ciudades
ciudades = sorted(df[CITY_COL].dropna().unique())
ciudad_sel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# Diccionario d
